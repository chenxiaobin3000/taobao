<template>
  <div class="app-container">
    <el-form :model="listQuery" label-position="left" label-width="50px" style="width: 100%; padding: 0 1% 0 1%;">
      <el-row>
        <el-col :span="6">
          <el-form-item label="店铺:" prop="shopName">
            <el-select v-model="listQuery.id" class="filter-item" placeholder="请选择店铺" @change="handleChangeShop">
              <el-option v-for="item in shopList" :key="item.id" :label="item.name" :value="item.id" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item label="状态:" prop="orderStatus">
            <el-select v-model="listQuery.status" class="filter-item" placeholder="请选择状态" @change="handleChangeStatus">
              <el-option v-for="item in statusList" :key="'S' + item.id" :label="item.name" :value="item.id" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <div>1</div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="3">
          <div>付款: {{ payment ? payment : 0 }} 元 </div>
        </el-col>
        <el-col :span="3">
          <div>退款: {{ refund_customer ? refund_customer : 0 }} 元 </div>
        </el-col>
        <el-col :span="3">
          <div>退平台: {{ refund_platform ? refund_platform : 0 }} 元</div>
        </el-col>
        <el-col :span="3">
          <div>采购: {{ procure ? procure : 0 }} 元</div>
        </el-col>
        <el-col :span="3">
          <div>采购退: {{ refund_procure ? refund_procure : 0 }} 元</div>
        </el-col>
        <el-col :span="3">
          <div>打款: {{ transfer ? transfer : 0 }} 元</div>
        </el-col>
        <el-col :span="3">
          <div>扣费: {{ deduction ? deduction : 0 }} 元</div>
        </el-col>
      </el-row>
    </el-form>
    <el-table ref="table" v-loading="loading" :data="list" :height="tableHeight" style="width: 100%" border fit highlight-current-row>
      <el-table-column align="center" label="订单编码" width="160">
        <template slot-scope="scope">
          {{ scope.row.order_id }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="金额" width="80">
        <template slot-scope="scope">
          {{ scope.row.payment }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="扣费" width="80">
        <template slot-scope="scope">
          {{ scope.row.amount }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="采购" width="80">
        <template slot-scope="scope">
          {{ scope.row.procure }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="状态" width="200">
        <template slot-scope="scope">
          {{ num2type(scope.row.order_status) }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="日期" width="160">
        <template slot-scope="scope">
          {{ scope.row.create_time }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="商品" width="160">
        <template slot-scope="scope">
          {{ scope.row.good_names }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="明细">
        <template slot-scope="scope">
          {{ scope.row.deduction_detail }}
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.num" @pagination="getOrderReport" />
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Pagination from '@/components/Pagination'
import { OrderStatus } from '@/utils/const'
import { getOrderReport } from '@/api/report/orderReport'
import { getShopList } from '@/api/system/shop'

export default {
  components: { Pagination },
  data() {
    return {
      userdata: {},
      tableHeight: 600,
      list: null,
      total: 0,
      payment: 0,
      refund_customer: 0,
      refund_platform: 0,
      procure: 0,
      refund_procure: 0,
      transfer: 0,
      deduction: 0,
      loading: false,
      shopList: [], // 本公司所有店铺列表
      statusList: [], // 本订单状态列表
      listQuery: {
        id: 0,
        status: 0,
        page: 1,
        num: 10,
        search: null
      }
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
    this.statusList = OrderStatus.getList()
    this.getShopList()
  },
  methods: {
    getOrderReport() {
      this.loading = true
      getOrderReport(
        this.listQuery
      ).then(response => {
        this.total = response.data.data.total
        this.payment = response.data.data.payment
        this.refund_customer = response.data.data.refund_customer
        this.refund_platform = response.data.data.refund_platform
        this.procure = response.data.data.procure
        this.refund_procure = response.data.data.refund_procure
        this.transfer = response.data.data.transfer
        this.deduction = response.data.data.deduction
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
        if (this.listQuery.id === 0) {
          this.listQuery.id = this.shopList[0].id
        }
        this.listQuery.status = this.statusList[0].id
        this.getOrderReport()
      })
    },
    num2type(num) {
      return OrderStatus.num2text(num)
    },
    handleChangeShop() {
      this.$store.commit('header/SET_HEADER_SHOP', this.listQuery.id)
      this.getOrderReport()
    },
    handleChangeStatus() {
      this.getOrderReport()
    }
  }
}
</script>
