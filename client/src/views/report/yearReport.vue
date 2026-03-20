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
      </el-row>
      <el-row>
        <el-col :span="4">
          <div :style="{ color: expect < 0 ? 'red' : 'green' }">预估: {{ expect }} 元 </div>
        </el-col>
        <el-col :span="4">
          <div :style="{ color: profit < 0 ? 'red' : 'green' }">利润: {{ profit }} 元 </div>
        </el-col>
        <el-col :span="4">
          <div>成交: {{ amount }} 元 </div>
        </el-col>
        <el-col :span="4">
          <div>未完结: {{ pending ? pending : 0 }} 元 </div>
        </el-col>
        <el-col :span="4">
          <div>已完结: {{ settled ? settled : 0 }} 元 </div>
        </el-col>
        <el-col :span="4">
          <div>退款: {{ refund ? refund : 0 }} 元</div>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="4">
          <div>推广: {{ promotion ? promotion : 0 }} 元</div>
        </el-col>
        <el-col :span="4">
          <div>采购: {{ procure ? procure : 0 }} 元 </div>
        </el-col>
        <el-col :span="4">
          <div>采购退: {{ refund_procure ? refund_procure : 0 }} 元 </div>
        </el-col>
        <el-col :span="4">
          <div>打款: {{ transfer ? transfer : 0 }} 元</div>
        </el-col>
        <el-col :span="4">
          <div>扣费: {{ deduction ? deduction : 0 }} 元</div>
        </el-col>
        <el-col :span="4">
          <div>刷单: {{ fake ? fake : 0 }} 元</div>
        </el-col>
      </el-row>
    </el-form>
    <el-table ref="table" v-loading="loading" :data="list" :height="tableHeight" style="width: 100%" border fit highlight-current-row>
      <el-table-column align="center" label="日期" width="90">
        <template slot-scope="scope">
          {{ scope.row.create_date }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="利润" width="100">
        <template slot-scope="scope">
          <div :style="{ color: scope.row.profit < 0 ? 'red' : 'green' }">{{ scope.row.profit }}</div>
        </template>
      </el-table-column>
      <el-table-column align="center" label="预估" width="100">
        <template slot-scope="scope">
          <div :style="{ color: scope.row.expect < 0 ? 'red' : 'green' }">{{ scope.row.expect }}</div>
        </template>
      </el-table-column>
      <el-table-column align="center" label="总金额" width="100">
        <template slot-scope="scope">
          {{ scope.row.amount }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="未完结" width="100">
        <template slot-scope="scope">
          {{ scope.row.pending }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="已完结" width="100">
        <template slot-scope="scope">
          {{ scope.row.settled }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="退款" width="100">
        <template slot-scope="scope">
          {{ scope.row.refund }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="采购" width="100">
        <template slot-scope="scope">
          {{ scope.row.procure }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="采购退款" width="100">
        <template slot-scope="scope">
          {{ scope.row.refund_procure }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="打款" width="100">
        <template slot-scope="scope">
          {{ scope.row.transfer }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="扣款" width="100">
        <template slot-scope="scope">
          {{ scope.row.deduction }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="推广" width="100">
        <template slot-scope="scope">
          {{ scope.row.promotion }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="刷单" width="100">
        <template slot-scope="scope">
          {{ scope.row.fake }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="备注">
        <div><br></div>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import { getYearReport } from '@/api/report/yearReport'
import { getShopList } from '@/api/system/shop'

export default {
  data() {
    return {
      userdata: {},
      tableHeight: 600,
      list: null,
      expect: 0, // 预估
      profit: 0, // 利润
      amount: 0, // 成交
      pending: 0, // 未结算
      settled: 0, // 已结算
      refund: 0, // 退款
      procure: 0, // 采购
      refund_procure: 0, // 采购退款
      transfer: 0, // 打款
      deduction: 0, // 扣款
      promotion: 0, // 推广
      fake: 0, // 刷单
      loading: false,
      shopList: [], // 本公司所有店铺列表
      listQuery: {
        id: 0
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
        this.tableHeight = window.innerHeight - this.$refs.table.$el.offsetTop - 10
      }
    }, 1000)
  },
  created() {
    this.userdata = this.$store.getters.userdata
    this.listQuery.id = this.$store.getters.shop
    this.listQuery.sdate = new Date()
    this.listQuery.edate = new Date().toLocaleDateString().replace(/\//g, '-')
    const seconds = this.listQuery.sdate.getTime() - 1000 * 60 * 60 * 24 * 31
    this.listQuery.sdate.setTime(seconds)
    this.listQuery.sdate = this.listQuery.sdate.toLocaleDateString().replace(/\//g, '-')
    this.getShopList()
  },
  methods: {
    getYearReport() {
      this.loading = true
      getYearReport(
        this.listQuery
      ).then(response => {
        this.pending = response.data.data.pending
        this.settled = response.data.data.settled
        this.refund = response.data.data.refund
        this.procure = response.data.data.procure
        this.refund_procure = response.data.data.refund_procure
        this.transfer = response.data.data.transfer
        this.deduction = response.data.data.deduction
        this.promotion = response.data.data.promotion
        this.fake = response.data.data.fake
        this.amount = parseFloat(this.pending) + parseFloat(this.settled) + parseFloat(this.refund)
        this.profit = parseFloat(this.settled) - parseFloat(this.refund) - parseFloat(this.procure) + parseFloat(this.refund_procure) - parseFloat(this.promotion) - parseFloat(this.transfer) - parseFloat(this.deduction) - parseFloat(this.fake)
        this.expect = parseFloat(this.pending) + this.profit
        this.amount = this.amount.toFixed(2)
        this.profit = this.profit.toFixed(2)
        this.expect = this.expect.toFixed(2)

        this.list = response.data.data.list
        this.list.forEach(v => {
          v.amount = parseFloat(v.pending) + parseFloat(v.settled) + parseFloat(v.refund)
          v.profit = parseFloat(v.settled) - parseFloat(v.refund) - parseFloat(v.procure) + parseFloat(v.refund_procure) - parseFloat(v.promotion) - parseFloat(v.transfer) - parseFloat(v.deduction) - parseFloat(v.fake)
          v.expect = parseFloat(v.pending) + v.profit
          v.amount = v.amount.toFixed(2)
          v.profit = v.profit.toFixed(2)
          v.expect = v.expect.toFixed(2)
        })
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
        this.getYearReport()
      })
    },
    handleChange() {
      this.$store.commit('header/SET_HEADER_SHOP', this.listQuery.id)
      this.getYearReport()
    }
  }
}
</script>
