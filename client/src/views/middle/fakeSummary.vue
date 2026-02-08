<template>
  <div class="app-container">
    <el-form :model="listQuery" label-position="left" label-width="80px">
      <el-row>
        <el-col :span="8">
          <el-form-item label="店铺:" prop="shopName">
            <el-select v-model="listQuery.id" class="filter-item" placeholder="请选择店铺" @change="handleChange">
              <el-option v-for="item in shopList" :key="item.id" :label="item.name" :value="item.id" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="开始日期:" prop="startDate">
            <el-date-picker v-model="temp.start_date" type="date" value-format="yyyy-MM-dd" class="filter-item" style="width: 150px;" />
            <el-button type="primary" size="mini" style="float:right;width:60px" @click="handleFlush()">刷新</el-button>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>
    <el-table ref="table" v-loading="loading" :data="list" :height="tableHeight" style="width: 100%" border fit highlight-current-row>
      <el-table-column align="center" label="日期" width="160">
        <template slot-scope="scope">
          {{ scope.row.create_date }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="真实订单数" width="160">
        <template slot-scope="scope">
          {{ scope.row.order_num }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="真实金额" width="160">
        <template slot-scope="scope">
          {{ scope.row.order_amount }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="刷单订单数" width="160">
        <template slot-scope="scope">
          {{ scope.row.fake_num }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="总金额" width="160">
        <template slot-scope="scope">
          {{ scope.row.fake_amount }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="总佣金" width="160">
        <template slot-scope="scope">
          {{ scope.row.commission }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="总运费" width="160">
        <template slot-scope="scope">
          {{ scope.row.freight }}
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
          <div>金额: {{ temp.order_amount }}, 订单数: {{ temp.order_num }}</div>
        </el-form-item>
        <el-form-item label="刷单总金额">
          <el-input v-model="temp.fake_amount" />
        </el-form-item>
        <el-form-item label="刷单订单数">
          <el-input v-model="temp.fake_num" />
        </el-form-item>
        <el-form-item label="总佣金">
          <el-input v-model="temp.commission" />
          <div>校验: 3 x {{ temp.fake_num }} = {{ 3 * temp.fake_num }}</div>
        </el-form-item>
        <el-form-item label="总运费">
          <el-input v-model="temp.freight" />
          <div>校验: 2 x {{ temp.fake_num }} = {{ 2 * temp.fake_num }}</div>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="temp.fake_note" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="danger" @click="dialogVisible=false">取消</el-button>
        <el-button type="primary" @click="updateData()">确定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Pagination from '@/components/Pagination'
import { getFakeSummaryList, flushFakeSummary, setFakeSummary } from '@/api/middle/fakeSummary'
import { getShopList } from '@/api/system/shop'

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
      search: state => state.header.search,
      create: state => state.header.create
    })
  },
  watch: {
    search(newVal, oldVal) {
      this.$message({ type: 'error', message: '不支持搜索!' })
    },
    create() {
      this.$message({ type: 'error', message: '不支持新建!' })
    }
  },
  mounted: function() {
    setTimeout(() => {
      this.tableHeight = window.innerHeight - this.$refs.table.$el.offsetTop - 78
    }, 1000)
  },
  created() {
    this.userdata = this.$store.getters.userdata
    this.listQuery.id = 0
    this.resetTemp()
    this.getShopList()
  },
  methods: {
    resetTemp() {
      this.temp = {
        id: 0,
        fake_amount: 0,
        fake_num: 0,
        commission: 0,
        freight: 0,
        fake_note: '',
        start_date: new Date().toLocaleDateString().replace(/\//g, '-')
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
    getShopList() {
      getShopList({
        id: this.userdata.company.id,
        page: 1,
        num: 1000
      }).then(response => {
        this.shopList = response.data.data.list
        this.listQuery.id = this.shopList[0].id
        this.getFakeSummaryList()
      })
    },
    handleChange() {
      this.getFakeSummaryList()
    },
    handleFlush() {
      flushFakeSummary({
        id: this.listQuery.id,
        sdate: this.temp.start_date
      }).then(() => {
        this.$message({ type: 'success', message: '刷新成功!' })
        this.getFakeSummaryList()
      })
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row)
      this.dialogVisible = true
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
    }
  }
}
</script>
