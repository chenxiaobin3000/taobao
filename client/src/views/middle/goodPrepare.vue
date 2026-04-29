<template>
  <div class="app-container">
    <el-form :model="listQuery" label-position="left" label-width="50px" style="width: 100%; padding: 0 1% 0 1%;">
      <el-form-item label="店铺:" prop="shopName">
        <el-select v-model="listQuery.id" class="filter-item" placeholder="请选择店铺" @change="handleChange">
          <el-option v-for="item in shopList" :key="item.id" :label="item.name" :value="item.id" />
        </el-select>
        <el-button type="primary" size="mini" style="float:right;width:60px" @click="handleCreate()">新建</el-button>
        <el-button type="danger" size="mini" style="float:right;width:60px;margin-right:10px;" @click="handleFlush()">刷新</el-button>
      </el-form-item>
    </el-form>
    <el-table ref="table" v-loading="loading" :data="list" :height="tableHeight" style="width: 100%" border fit highlight-current-row>
      <el-table-column align="center" label="商品名称" width="100">
        <template slot-scope="scope">
          {{ scope.row.name }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="外部编码" width="120">
        <template slot-scope="scope">
          <a :href="handleJumpOrigin(scope.row.origin, scope.row.origin_type)" target="_blank">{{ scope.row.origin }}</a>
        </template>
      </el-table-column>
      <el-table-column align="center" label="外部类型" width="70">
        <template slot-scope="scope">
          {{ num2OriginType(scope.row.origin_type) }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="进货编码" width="120">
        <template slot-scope="scope">
          <a :href="handleJumpStock(scope.row.stock, scope.row.stock_type)" target="_blank">{{ scope.row.stock }}</a>
        </template>
      </el-table-column>
      <el-table-column align="center" label="进货类型" width="70">
        <template slot-scope="scope">
          {{ num2StockType(scope.row.stock_type) }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="创建时间" width="160">
        <template slot-scope="scope">
          {{ scope.row.ctime }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="上品时间" width="90">
        <template slot-scope="scope">
          {{ scope.row.join_date }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="备注">
        <template slot-scope="scope">
          {{ scope.row.good_note }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="操作" width="80">
        <template slot-scope="{row}">
          <el-button type="danger" size="mini" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.num" @pagination="getGoodPrepareList" />

    <!-- 商品信息编辑 -->
    <el-dialog title="新增商品信息" :visible.sync="dialogVisible">
      <el-form :model="temp" label-position="left" label-width="70px" style="width: 100%; padding: 0 4% 0 4%;">
        <el-form-item label="商品名称">
          <el-input v-model="temp.name" />
        </el-form-item>
        <el-form-item label="外部编码">
          <el-input v-model="temp.origin" />
        </el-form-item>
        <el-form-item label="外部类型">
          <el-select v-model="temp.origin_type" class="filter-item" placeholder="请选择类型">
            <el-option v-for="item in originList" :key="item.id" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="进货编码">
          <el-input v-model="temp.stock" />
        </el-form-item>
        <el-form-item label="进货类型">
          <el-select v-model="temp.stock_type" class="filter-item" placeholder="请选择类型">
            <el-option v-for="item in stockList" :key="item.id" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="temp.good_note" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="danger" @click="dialogVisible=false">取消</el-button>
        <el-button type="primary" @click="createData()">确定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Pagination from '@/components/Pagination'
import { GoodOriginType, GoodStockType } from '@/utils/const'
import { getGoodPrepareList, addGoodPrepare, delGoodPrepare, flushGoodPrepare } from '@/api/middle/goodPrepare'
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
      originList: [], // 商品类型列表
      stockList: [], // 商品类型列表
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
      search: state => state.header.search
    })
  },
  watch: {
    search(newVal, oldVal) {
      this.listQuery.search = newVal
      this.getGoodPrepareList()
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
    this.originList = GoodOriginType.getList()
    this.stockList = GoodStockType.getList()
    this.resetTemp()
    this.getOwnShopList()
  },
  methods: {
    resetTemp() {
      this.temp = {
        id: 0,
        name: '',
        origin: '',
        origin_type: 1,
        stock: '',
        stock_type: 1,
        good_note: ''
      }
    },
    getGoodPrepareList() {
      this.loading = true
      getGoodPrepareList(
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
        this.getGoodPrepareList()
      })
    },
    num2OriginType(num) {
      return GoodOriginType.num2text(num)
    },
    num2StockType(num) {
      return GoodStockType.num2text(num)
    },
    handleJumpOrigin(id, type) {
      return GoodOriginType.getUrl(id, type)
    },
    handleJumpStock(id, type) {
      return GoodStockType.getUrl(id, type)
    },
    handleChange() {
      this.$store.commit('header/SET_HEADER_SHOP', this.listQuery.id)
      this.getGoodPrepareList()
    },
    handleCreate() {
      this.resetTemp()
      this.dialogVisible = true
    },
    createData() {
      addGoodPrepare({
        id: this.listQuery.id,
        name: this.temp.name,
        origin: this.temp.origin,
        origin_type: this.temp.origin_type,
        stock: this.temp.stock,
        stock_type: this.temp.stock_type,
        note: this.temp.good_note
      }).then(() => {
        this.$message({ type: 'success', message: '新增成功!' })
        this.getGoodPrepareList()
        this.dialogVisible = false
      })
    },
    handleFlush() {
      flushGoodPrepare({
        id: this.listQuery.id
      }).then(() => {
        this.$message({ type: 'success', message: '刷新成功!' })
        this.getGoodPrepareList()
      })
    },
    handleDelete(row) {
      this.$confirm('确定要删除吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        delGoodPrepare({
          id: row.id
        }).then(() => {
          this.$message({ type: 'success', message: '删除成功!' })
          this.getGoodPrepareList()
        })
      })
    }
  }
}
</script>
