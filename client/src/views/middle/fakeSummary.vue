<template>
  <div class="app-container">
    <el-form :model="listQuery" label-position="left" label-width="50px" style="width: 100%; padding: 0 1% 0 1%;">
      <el-row>
        <el-col :span="6">
          <el-form-item label="店铺:" prop="shopName">
            <el-select v-model="listQuery.id" class="filter-item" placeholder="请选择店铺" @change="handleChange">
              <el-option v-for="item in shopList" :key="item.id" :label="item.name" :value="item.id" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item label="开始日期:" prop="startDate" label-width="80px">
            <el-date-picker v-model="start_date" type="date" value-format="yyyy-MM-dd" class="filter-item" style="width: 150px;" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-button type="primary" size="mini" style="float:right;width:60px" @click="handleFlush()">刷新</el-button>
          <el-button type="danger" size="mini" style="float:right;width:80px;margin-right:10px;" @click="batchData()">批量填入</el-button>
        </el-col>
      </el-row>
    </el-form>
    <el-table ref="table" v-loading="loading" :data="list" :height="tableHeight" style="width: 100%" border fit highlight-current-row>
      <el-table-column align="center" label="日期" width="90">
        <template slot-scope="scope">
          {{ scope.row.create_date }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="真实订单数" width="90">
        <template slot-scope="scope">
          {{ scope.row.order_num }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="真实金额" width="90">
        <template slot-scope="scope">
          {{ scope.row.order_amount }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="刷单订单数" width="90">
        <template slot-scope="scope">
          {{ scope.row.fake_num }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="总金额" width="90">
        <template slot-scope="scope">
          <div :style="{ color: scope.row.commission < 0.01 ? 'red' : 'green' }">{{ scope.row.fake_amount }}</div>
        </template>
      </el-table-column>
      <el-table-column align="center" label="总佣金" width="90">
        <template slot-scope="scope">
          <div :style="{ color: scope.row.commission < 0.01 ? 'red' : 'green' }">{{ scope.row.commission }}</div>
        </template>
      </el-table-column>
      <el-table-column align="center" label="总运费" width="90">
        <template slot-scope="scope">
          <div :style="{ color: scope.row.commission < 0.01 ? 'red' : 'green' }">{{ scope.row.freight }}</div>
        </template>
      </el-table-column>
      <el-table-column align="center" label="备注">
        <template slot-scope="scope">
          {{ scope.row.fake_note }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="操作" width="80">
        <template slot-scope="{row}">
          <el-button type="primary" size="mini" @click="handleUpdate(row)">设置</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.num" @pagination="getFakeSummaryList" />

    <!-- 刷单信息编辑 -->
    <el-dialog title="修改刷单信息" :visible.sync="dialogVisible">
      <el-form :model="temp" label-position="left" label-width="70px" style="width: 100%; padding: 0 4% 0 4%;">
        <el-form-item label="真实数据">
          <div style="color:rgba(255,0,0,0.5)">金额: {{ temp.order_amount }} ( {{ 5 * temp.order_num }} ) | 订单数: {{ temp.order_num }}</div>
        </el-form-item>
        <el-form-item label="总金额">
          <el-input v-model="temp.fake_amount" />
          <div style="color:rgba(255,0,0,0.5)">5元: {{ 5 * temp.fake_num }}</div>
        </el-form-item>
        <el-form-item label="订单数">
          <el-input v-model="temp.fake_num" />
        </el-form-item>
        <el-form-item label="总佣金">
          <el-input v-model="temp.commission" />
          <div style="color:rgba(255,0,0,0.5)">3元: {{ 3 * temp.fake_num }}</div>
        </el-form-item>
        <el-form-item label="总运费">
          <el-input v-model="temp.freight" />
          <div style="color:rgba(255,0,0,0.5)">2元: {{ 2 * temp.fake_num }}</div>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="temp.fake_note" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" style="float:left" @click="autoData()">自动填入</el-button>
        <el-button type="danger" @click="dialogVisible=false">取消</el-button>
        <el-button type="primary" @click="updateData()">确定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Pagination from '@/components/Pagination'
import { getFakeSummaryList, flushFakeSummary, setFakeSummary, batchFakeSummary } from '@/api/middle/fakeSummary'
import { getOwnShopList } from '@/api/system/shop'

export default {
  components: { Pagination },
  data() {
    return {
      userdata: {},
      tableHeight: 600,
      list: null,
      total: 0,
      loading: false,
      shopList: [], // 本公司所有店铺列表
      start_date: 0,
      listQuery: {
        id: 0,
        page: 1,
        num: 10,
        search: null
      },
      temp: {},
      dialogVisible: false
    }
  },
  computed: {
    ...mapState({
      search: state => state.header.search
    })
  },
  watch: {
    search(newVal, oldVal) {
      this.$message({ type: 'error', message: '不支持搜索!' })
    }
  },
  mounted: function() {
    setTimeout(() => {
      if (this.$refs.table) {
        this.tableHeight = window.innerHeight - this.$refs.table.$el.offsetTop - 78
      }
    }, 1000)
  },
  created() {
    this.userdata = this.$store.getters.userdata
    this.listQuery.id = this.$store.getters.shop
    this.start_date = new Date().toLocaleDateString().replace(/\//g, '-')
    this.resetTemp()
    this.getOwnShopList()
  },
  methods: {
    resetTemp() {
      this.temp = {
        id: 0,
        fake_amount: 0,
        fake_num: 0,
        commission: 0,
        freight: 0,
        fake_note: ''
      }
    },
    getFakeSummaryList() {
      this.loading = true
      getFakeSummaryList(
        this.listQuery
      ).then(response => {
        this.total = response.data.data.total
        this.list = response.data.data.list
        this.loading = false
      }).catch(error => {
        this.loading = false
        Promise.reject(error)
      })
    },
    getOwnShopList() {
      getOwnShopList({
        id: this.userdata.company.id,
        uid: this.userdata.user.id
      }).then(response => {
        this.shopList = response.data.data
        if (this.listQuery.id === 0) {
          this.listQuery.id = this.shopList[0].id
        }
        this.getFakeSummaryList()
      })
    },
    handleChange() {
      this.$store.commit('header/SET_HEADER_SHOP', this.listQuery.id)
      this.getFakeSummaryList()
    },
    handleFlush() {
      flushFakeSummary({
        id: this.listQuery.id,
        sdate: this.start_date
      }).then(() => {
        this.$message({ type: 'success', message: '刷新成功!' })
        this.getFakeSummaryList()
      })
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row)
      this.dialogVisible = true
    },
    autoData() {
      this.temp.fake_amount = this.temp.order_amount
      this.temp.fake_num = this.temp.order_num
      this.temp.commission = this.temp.order_num * 3
      this.temp.freight = this.temp.order_num * 2
    },
    updateData() {
      setFakeSummary({
        id: this.temp.id,
        amount: this.temp.fake_amount,
        num: this.temp.fake_num,
        comm: this.temp.commission,
        freight: this.temp.freight,
        note: this.temp.fake_note
      }).then(() => {
        this.$message({ type: 'success', message: '修改成功!' })
        this.getFakeSummaryList()
        this.dialogVisible = false
      })
    },
    batchData() {
      this.$confirm('确定要批量填入吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        batchFakeSummary({
          id: this.listQuery.id,
          sdate: this.start_date
        }).then(() => {
          this.$message({ type: 'success', message: '修改成功!' })
          this.getFakeSummaryList()
        })
      })
    }
  }
}
</script>
