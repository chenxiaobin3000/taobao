<template>
  <div class="app-container">
    <el-form :model="listQuery" label-position="left" label-width="50px" style="width: 100%; padding: 0 1% 0 1%;">
      <el-row>
        <el-col :span="6">
          <el-form-item label="店铺:">
            <el-select v-model="listQuery.id" class="filter-item" placeholder="请选择店铺" @change="handleChange">
              <el-option v-for="item in shopList" :key="item.id" :label="item.name" :value="item.id" />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row style="font-size:small">
        <el-col :span="3">
          <div :style="{ color: expect < 0 ? 'red' : 'green' }">预估: {{ expect }}</div>
        </el-col>
        <el-col :span="3">
          <div :style="{ color: profit < 0 ? 'red' : 'green' }">利润: {{ profit }}</div>
        </el-col>
        <el-col :span="3">
          <div>未完结: {{ pending ? pending : 0 }}</div>
        </el-col>
        <el-col :span="3">
          <div>已完结: {{ settled ? settled : 0 }}</div>
        </el-col>
        <el-col :span="2">
          <div>已关闭: {{ close ? close : 0 }}</div>
        </el-col>
        <el-col :span="2">
          <div>未完采: {{ pending_procure ? pending_procure : 0 }}</div>
        </el-col>
        <el-col :span="2">
          <div>完结采: {{ settled_procure ? settled_procure : 0 }}</div>
        </el-col>
        <el-col :span="2">
          <div>关闭采: {{ close_procure ? close_procure : 0 }}</div>
        </el-col>
        <el-col :span="2">
          <div>扣费: {{ deduction ? deduction : 0 }}</div>
        </el-col>
        <el-col :span="2">
          <div>刷扣: {{ fake_deduction ? fake_deduction : 0 }}</div>
        </el-col>
      </el-row>
      <el-row style="font-size:small">
        <el-col :span="3">
          <div>成交: {{ amount }}</div>
        </el-col>
        <el-col :span="3">
          <div>推广: {{ promotion ? promotion : 0 }}</div>
        </el-col>
        <el-col :span="3">
          <div>未完退: {{ pending_refund ? pending_refund : 0 }}</div>
        </el-col>
        <el-col :span="3">
          <div>完结退: {{ settled_refund ? settled_refund : 0 }}</div>
        </el-col>
        <el-col :span="2">
          <div>关闭退: {{ close_refund ? close_refund : 0 }}</div>
        </el-col>
        <el-col :span="2">
          <div>未采退: {{ pending_refund_procure ? pending_refund_procure : 0 }}</div>
        </el-col>
        <el-col :span="2">
          <div>已采退: {{ settled_refund_procure ? settled_refund_procure : 0 }}</div>
        </el-col>
        <el-col :span="2">
          <div>关采退: {{ close_refund_procure ? close_refund_procure : 0 }}</div>
        </el-col>
        <el-col :span="2">
          <div>打款: {{ transfer ? transfer : 0 }}</div>
        </el-col>
        <el-col :span="2">
          <div>刷拥: {{ fake ? fake : 0 }}</div>
        </el-col>
      </el-row>
    </el-form>
    <el-table ref="table" v-loading="loading" :data="list" :height="tableHeight" style="width: 100%" border fit highlight-current-row :row-class-name="rowClassName" @row-click="handleRowClick">
      <el-table-column align="center" label="日期" width="90">
        <template slot-scope="scope">
          {{ scope.row.create_date }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="预估" width="70">
        <template slot-scope="scope">
          <div :style="{ color: scope.row.expect < 0 ? 'red' : 'green' }">{{ scope.row.expect }}</div>
        </template>
      </el-table-column>
      <el-table-column align="center" label="利润" width="70">
        <template slot-scope="scope">
          <div :style="{ color: scope.row.profit < 0 ? 'red' : 'green' }">{{ scope.row.profit }}</div>
        </template>
      </el-table-column>
      <el-table-column align="center" label="总金额" width="80">
        <template slot-scope="scope">
          {{ scope.row.amount }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="毛利" width="80">
        <template slot-scope="scope">
          {{ scope.row.income }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="推广" width="90">
        <template slot-scope="scope">
          <strong>{{ scope.row.promotion }}</strong>
        </template>
      </el-table-column>
      <el-table-column align="center" label="投产" width="60">
        <template slot-scope="scope">
          <div :style="{ color: scope.row.roi > 1.2 ? 'green' : 'red' }">{{ scope.row.roi }}</div>
        </template>
      </el-table-column>
      <el-table-column align="center" label="扣款" width="70">
        <template slot-scope="scope">
          {{ scope.row.deduction }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="刷单佣金" width="70">
        <template slot-scope="scope">
          {{ scope.row.fake }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="刷单扣款" width="70">
        <template slot-scope="scope">
          {{ scope.row.fake_deduction }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="未完结" width="80">
        <template slot-scope="scope">
          <strong>{{ scope.row.pending }}</strong>
        </template>
      </el-table-column>
      <el-table-column align="center" label="未完退款" width="70">
        <template slot-scope="scope">
          {{ scope.row.pending_refund }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="未完采购" width="70">
        <template slot-scope="scope">
          {{ scope.row.pending_procure }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="未完采退" width="70">
        <template slot-scope="scope">
          {{ scope.row.pending_refund_procure }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="已完结" width="90">
        <template slot-scope="scope">
          <strong>{{ scope.row.settled }}</strong>
        </template>
      </el-table-column>
      <el-table-column align="center" label="已完退款" width="70">
        <template slot-scope="scope">
          {{ scope.row.settled_refund }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="已完采购" width="80">
        <template slot-scope="scope">
          {{ scope.row.settled_procure }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="已完采退" width="70">
        <template slot-scope="scope">
          {{ scope.row.settled_refund_procure }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="已关闭" width="90">
        <template slot-scope="scope">
          <strong>{{ scope.row.close }}</strong>
        </template>
      </el-table-column>
      <el-table-column align="center" label="关闭退款" width="80">
        <template slot-scope="scope">
          {{ scope.row.close_refund }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="关闭采购" width="70">
        <template slot-scope="scope">
          {{ scope.row.close_procure }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="关闭采退" width="70">
        <template slot-scope="scope">
          {{ scope.row.close_refund_procure }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="打款" width="70">
        <template slot-scope="scope">
          {{ scope.row.transfer }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="杂项" width="70">
        <template slot-scope="scope">
          {{ scope.row.misc }}
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
import { getDayReport } from '@/api/report/dayReport'
import { getOwnShopList } from '@/api/system/shop'

export default {
  data() {
    return {
      userdata: {},
      tableHeight: 600,
      list: null,
      expect: 0, // 预估
      income: 0, // 毛利
      profit: 0, // 利润
      amount: 0, // 成交
      pending: 0, // 未结算
      pending_refund: 0, // 未结算退款
      pending_procure: 0, // 未结算采购
      pending_refund_procure: 0, // 未结算采购退款
      settled: 0, // 已结算
      settled_refund: 0, // 已结算退款
      settled_procure: 0, // 已结算采购
      settled_refund_procure: 0, // 已结算采购退款
      close: 0, // 关闭
      close_refund: 0, // 关闭退款
      close_procure: 0, // 关闭采购
      close_refund_procure: 0, // 关闭采购退款
      transfer: 0, // 打款
      deduction: 0, // 扣款
      promotion: 0, // 推广
      fake: 0, // 刷单
      fake_deduction: 0, // 刷单扣款
      misc: 0, // 杂项
      loading: false,
      shopList: [], // 本公司所有店铺列表
      listQuery: {
        id: 0
      },
      dayReportCache: {}
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
        this.tableHeight = window.innerHeight - this.$refs.table.$el.offsetTop - 20
      }
    }, 1000)
  },
  created() {
    this.userdata = this.$store.getters.userdata
    this.listQuery.id = this.$store.getters.shop
    this.getOwnShopList()
  },
  methods: {
    getYearReport() {
      this.loading = true
      getYearReport(
        this.listQuery
      ).then(response => {
        this.pending = response.data.data.pending
        this.pending_refund = response.data.data.pending_refund
        this.pending_procure = response.data.data.pending_procure
        this.pending_refund_procure = response.data.data.pending_refund_procure
        this.settled = response.data.data.settled
        this.settled_refund = response.data.data.settled_refund
        this.settled_procure = response.data.data.settled_procure
        this.settled_refund_procure = response.data.data.settled_refund_procure
        this.close = response.data.data.close
        this.close_refund = response.data.data.close_refund
        this.close_procure = response.data.data.close_procure
        this.close_refund_procure = response.data.data.close_refund_procure
        this.transfer = response.data.data.transfer
        this.deduction = response.data.data.deduction
        this.promotion = response.data.data.promotion
        this.fake = response.data.data.fake
        this.fake_deduction = response.data.data.fake_deduction
        this.misc = response.data.data.misc
        // 成交
        this.amount = parseFloat(this.pending) + parseFloat(this.settled) + parseFloat(this.close)
        // 毛利
        this.income = parseFloat(this.pending) - parseFloat(this.pending_procure) + parseFloat(this.settled) - parseFloat(this.settled_procure)
        // 利润
        this.profit = parseFloat(this.settled) - parseFloat(this.settled_refund) - parseFloat(this.settled_procure) + parseFloat(this.settled_refund_procure) - parseFloat(this.promotion) - parseFloat(this.transfer) - parseFloat(this.deduction) - parseFloat(this.fake) - parseFloat(this.fake_deduction) - parseFloat(this.misc)
        // 预估
        this.expect = parseFloat(this.pending) - parseFloat(this.pending_refund) - parseFloat(this.pending_procure) + parseFloat(this.pending_refund_procure) + this.profit
        this.amount = this.amount.toFixed(1)
        this.income = this.income.toFixed(1)
        this.profit = this.profit.toFixed(1)
        this.expect = this.expect.toFixed(1)

        this.dayReportCache = {}

        // 预处理数据
        const data = response.data.data.list
        Object.entries(data).forEach(([k, v]) => {
          this.buildReportRow(v)
        })

        // 按年份统计插入数据
        this.list = []
        const currentYear = new Date().getFullYear()
        const currentMonth = new Date().getMonth()
        for (let y = 2025; y <= currentYear; ++y) {
          let pending = 0
          let pending_refund = 0
          let pending_procure = 0
          let pending_refund_procure = 0
          let settled = 0
          let settled_refund = 0
          let settled_procure = 0
          let settled_refund_procure = 0
          let close = 0
          let close_refund = 0
          let close_procure = 0
          let close_refund_procure = 0
          let transfer = 0
          let deduction = 0
          let promotion = 0
          let fake = 0
          let fake_deduction = 0
          let misc = 0
          for (let m = 0; m < 12; ++m) {
            if (y === currentYear && m > currentMonth) {
              break
            }
            // 插入月数据
            let key = ''
            if (m > 8) {
              key = y + '-' + (m + 1)
            } else {
              key = y + '-0' + (m + 1)
            }
            const temp = data[key]
            temp.create_date = y + '年' + (m + 1) + '月'
            temp.is_show = 0
            temp.report_type = 'month'
            temp.year_key = String(y)
            temp.month_key = key
            temp.day_loaded = false
            temp.day_expanded = false
            pending += temp.pending
            pending_refund += temp.pending_refund
            pending_procure += temp.pending_procure
            pending_refund_procure += temp.pending_refund_procure
            settled += temp.settled
            settled_refund += temp.settled_refund
            settled_procure += temp.settled_procure
            settled_refund_procure += temp.settled_refund_procure
            close += temp.close
            close_refund += temp.close_refund
            close_procure += temp.close_procure
            close_refund_procure += temp.close_refund_procure
            transfer += temp.transfer
            deduction += temp.deduction
            promotion += temp.promotion
            fake += temp.fake
            fake_deduction += temp.fake_deduction
            misc += temp.misc
            this.list.unshift(temp)
          }
          // 插入年数据
          const amount = pending + settled + close
          const income = pending + settled
          const profit = settled - settled_refund - settled_procure + settled_refund_procure - promotion - transfer - deduction - fake - fake_deduction - misc
          const expect = pending - pending_refund - pending_procure + pending_refund_procure + profit
          const roi = promotion === 0 ? '0.00' : (income / promotion).toFixed(2)
          this.list.unshift({
            create_date: y + '年',
            amount: amount.toFixed(1),
            income: income.toFixed(1),
            profit: profit.toFixed(1),
            expect: expect.toFixed(1),
            roi,
            pending: pending.toFixed(1),
            pending_refund: pending_refund.toFixed(1),
            pending_procure: pending_procure.toFixed(1),
            pending_refund_procure: pending_refund_procure.toFixed(1),
            settled: settled.toFixed(1),
            settled_refund: settled_refund.toFixed(1),
            settled_procure: settled_procure.toFixed(1),
            settled_refund_procure: settled_refund_procure.toFixed(1),
            close: close.toFixed(1),
            close_refund: close_refund.toFixed(1),
            close_procure: close_procure.toFixed(1),
            close_refund_procure: close_refund_procure.toFixed(1),
            transfer: transfer.toFixed(1),
            deduction: deduction.toFixed(1),
            promotion: promotion.toFixed(1),
            fake: fake.toFixed(1),
            fake_deduction: fake_deduction.toFixed(1),
            misc: misc.toFixed(1),
            is_show: 1,
            report_type: 'year',
            year_key: String(y)
          })
        }
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
        this.getYearReport()
      })
    },
    rowClassName({ row, rowIndex }) {
      if (row.is_show === 0) {
        return 'hidden-row'
      }
      if (row.report_type === 'year') {
        return 'year-row'
      }
      if (row.report_type === 'month') {
        return 'month-row'
      }
      if (row.report_type === 'day') {
        return 'day-row'
      }
    },
    handleChange() {
      this.$store.commit('header/SET_HEADER_SHOP', this.listQuery.id)
      this.getYearReport()
    },
    handleRowClick(row, column, event) {
      if (row.report_type === 'year') {
        this.toggleMonthRows(row)
      } else if (row.report_type === 'month') {
        this.toggleDayRows(row)
      }
    },
    toggleMonthRows(row) {
      const months = this.list.filter(v => v.report_type === 'month' && v.year_key === row.year_key)
      const isShow = months.some(v => v.is_show === 0)
      this.list.forEach(v => {
        if (v.year_key !== row.year_key) {
          return
        }
        if (v.report_type === 'month') {
          v.is_show = isShow ? 1 : 0
        } else if (v.report_type === 'day') {
          const month = months.find(item => item.month_key === v.month_key)
          v.is_show = isShow && month && month.day_expanded ? 1 : 0
        }
      })
    },
    toggleDayRows(row) {
      if (row.day_loaded) {
        row.day_expanded = !row.day_expanded
        this.setDayRowsVisible(row.month_key, row.day_expanded ? 1 : 0)
        return
      }
      this.loading = true
      getDayReport({
        id: this.listQuery.id,
        sdate: `${row.month_key}-01`,
        edate: this.getNextMonth(row.month_key)
      }).then(response => {
        const dayRows = (response.data.data.list || []).map(item => {
          this.buildReportRow(item)
          item.is_show = 1
          item.report_type = 'day'
          item.year_key = row.year_key
          item.month_key = row.month_key
          return item
        })
        this.dayReportCache[row.month_key] = dayRows
        row.day_loaded = true
        row.day_expanded = true
        const index = this.list.indexOf(row)
        this.list.splice(index + 1, 0, ...dayRows)
        this.loading = false
      }).catch(error => {
        this.loading = false
        Promise.reject(error)
      })
    },
    setDayRowsVisible(monthKey, isShow) {
      this.list.forEach(v => {
        if (v.report_type === 'day' && v.month_key === monthKey) {
          v.is_show = isShow
        }
      })
    },
    buildReportRow(row) {
      row.misc = row.misc || 0
      row.amount = parseFloat(row.pending) + parseFloat(row.settled) + parseFloat(row.close)
      row.income = parseFloat(row.pending) - parseFloat(row.pending_refund) + parseFloat(row.settled) - parseFloat(row.settled_procure)
      row.profit = parseFloat(row.settled) - parseFloat(row.settled_refund) - parseFloat(row.settled_procure) + parseFloat(row.settled_refund_procure) - parseFloat(row.promotion) - parseFloat(row.transfer) - parseFloat(row.deduction) - parseFloat(row.fake) - parseFloat(row.fake_deduction) - parseFloat(row.misc || 0)
      row.expect = parseFloat(row.pending) - parseFloat(row.pending_refund) - parseFloat(row.pending_procure) + parseFloat(row.pending_refund_procure) + row.profit
      row.roi = parseFloat(row.promotion) === 0 ? '0.00' : (row.income / parseFloat(row.promotion)).toFixed(2)
      row.amount = row.amount.toFixed(1)
      row.income = row.income.toFixed(1)
      row.profit = row.profit.toFixed(1)
      row.expect = row.expect.toFixed(1)
      return row
    },
    getNextMonth(monthKey) {
      const parts = monthKey.split('-')
      let year = parseInt(parts[0])
      let month = parseInt(parts[1]) + 1
      if (month > 12) {
        year += 1
        month = 1
      }
      return `${year}-${month > 9 ? month : '0' + month}-01`
    }
  }
}
</script>

<style lang="scss">
.el-table .year-row {
  background-color: rgba(180, 180, 180, 0.3);
}

.el-table .month-row {
  background-color: rgba(235, 235, 235, 0.3);
}

.el-table .day-row {
  background-color: rgba(250, 250, 250, 0.3);
}

.el-table .hidden-row {
  display: none;
}
</style>
