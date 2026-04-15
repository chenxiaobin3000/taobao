<template>
  <div class="app-container">
    <el-form label-position="left" label-width="50px" style="width: 100%; padding: 0 1% 0 1%;">
      <el-row>
        <el-col :span="24">
          <el-checkbox-group v-model="checkedShops" @change="handleChange">
            <el-checkbox v-for="item in shopList" :key="item.id" :label="item.name" :value="item.id" class="myCheckBox">
              <div style="font-size:small">{{ item.name }}</div>
            </el-checkbox>
          </el-checkbox-group>
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
      <el-table-column align="center" label="店铺" width="100">
        <template slot-scope="scope">
          {{ scope.row.name }}
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
      <el-table-column align="center" label="推广" width="80">
        <template slot-scope="scope">
          {{ scope.row.promotion }}
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
      <el-table-column align="center" label="未完结" width="70">
        <template slot-scope="scope">
          {{ scope.row.pending }}
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
      <el-table-column align="center" label="已完结" width="80">
        <template slot-scope="scope">
          {{ scope.row.settled }}
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
      <el-table-column align="center" label="已关闭" width="80">
        <template slot-scope="scope">
          {{ scope.row.close }}
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
      <el-table-column align="center" label="备注">
        <div><br></div>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import { getBoardReport } from '@/api/report/boardReport'
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
      loading: false,
      checkedShops: [], // 选中的店铺
      shopList: [] // 本公司所有店铺列表
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
    this.getOwnShopList()
  },
  methods: {
    getBoardReport() {
      const ids = []
      this.shopList.forEach(v => {
        if (this.checkedShops.includes(v.name)) {
          ids.push(v.id)
        }
      })
      if (ids.length === 0) {
        this.$message({ type: 'error', message: '至少要选中一个店铺!' })
        return
      }
      this.loading = true
      getBoardReport({
        ids: ids
      }).then(response => {
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
        // 成交
        this.amount = parseFloat(this.pending) + parseFloat(this.settled) + parseFloat(this.close)
        // 毛利
        this.income = parseFloat(this.pending) - parseFloat(this.pending_procure) + parseFloat(this.settled) - parseFloat(this.settled_procure)
        // 利润
        this.profit = parseFloat(this.settled) - parseFloat(this.settled_refund) - parseFloat(this.settled_procure) + parseFloat(this.settled_refund_procure) - parseFloat(this.promotion) - parseFloat(this.transfer) - parseFloat(this.deduction) - parseFloat(this.fake) - parseFloat(this.fake_deduction)
        // 预估
        this.expect = parseFloat(this.pending) - parseFloat(this.pending_refund) - parseFloat(this.pending_procure) + parseFloat(this.pending_refund_procure) + this.profit
        this.amount = this.amount.toFixed(1)
        this.income = this.income.toFixed(1)
        this.profit = this.profit.toFixed(1)
        this.expect = this.expect.toFixed(1)

        // 预处理数据
        const data = response.data.data.list
        Object.values(data).forEach(tmp => {
          Object.values(tmp).forEach(v => {
            v.amount = parseFloat(v.pending) + parseFloat(v.settled) + parseFloat(v.close)
            v.income = parseFloat(v.pending) - parseFloat(v.pending_refund) + parseFloat(v.settled) - parseFloat(v.settled_procure)
            v.profit = parseFloat(v.settled) - parseFloat(v.settled_refund) - parseFloat(v.settled_procure) + parseFloat(v.settled_refund_procure) - parseFloat(v.promotion) - parseFloat(v.transfer) - parseFloat(v.deduction) - parseFloat(v.fake) - parseFloat(v.fake_deduction)
            v.expect = parseFloat(v.pending) - parseFloat(v.pending_refund) - parseFloat(v.pending_procure) + parseFloat(v.pending_refund_procure) + v.profit
            v.amount = v.amount.toFixed(1)
            v.income = v.income.toFixed(1)
            v.profit = v.profit.toFixed(1)
            v.expect = v.expect.toFixed(1)
          })
        })

        // 按年份统计插入数据
        this.list = []
        const currentYear = new Date().getFullYear()
        const currentMonth = new Date().getMonth()
        for (let y = 2025; y <= currentYear; ++y) {
          // 全年所有店铺数据
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
            // 当月所有店铺数据
            let month_pending = 0
            let month_pending_refund = 0
            let month_pending_procure = 0
            let month_pending_refund_procure = 0
            let month_settled = 0
            let month_settled_refund = 0
            let month_settled_procure = 0
            let month_settled_refund_procure = 0
            let month_close = 0
            let month_close_refund = 0
            let month_close_procure = 0
            let month_close_refund_procure = 0
            let month_transfer = 0
            let month_deduction = 0
            let month_promotion = 0
            let month_fake = 0
            let month_fake_deduction = 0
            this.shopList.forEach(v => {
              if (!this.checkedShops.includes(v.name)) {
                return
              }
              const temp = data[key][v.id]
              temp.name = v.name
              temp.create_date = y + '年' + (m + 1) + '月'
              temp.is_show = 0
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

              month_pending += temp.pending
              month_pending_refund += temp.pending_refund
              month_pending_procure += temp.pending_procure
              month_pending_refund_procure += temp.pending_refund_procure
              month_settled += temp.settled
              month_settled_refund += temp.settled_refund
              month_settled_procure += temp.settled_procure
              month_settled_refund_procure += temp.settled_refund_procure
              month_close += temp.close
              month_close_refund += temp.close_refund
              month_close_procure += temp.close_procure
              month_close_refund_procure += temp.close_refund_procure
              month_transfer += temp.transfer
              month_deduction += temp.deduction
              month_promotion += temp.promotion
              month_fake += temp.fake
              month_fake_deduction += temp.fake_deduction
              this.list.unshift(temp)
            })
            // 插入月汇总数据
            const amount = month_pending + month_settled + month_close
            const income = month_pending + month_settled
            const profit = month_settled - month_settled_refund - month_settled_procure + month_settled_refund_procure - month_promotion - month_transfer - month_deduction - month_fake - month_fake_deduction
            const expect = month_pending - month_pending_refund - month_pending_procure + month_pending_refund_procure + profit
            this.list.unshift({
              create_date: y + '年' + (m + 1) + '月汇总',
              amount: amount.toFixed(1),
              income: income.toFixed(1),
              profit: profit.toFixed(1),
              expect: expect.toFixed(1),
              pending: month_pending.toFixed(1),
              pending_refund: month_pending_refund.toFixed(1),
              pending_procure: month_pending_procure.toFixed(1),
              pending_refund_procure: month_pending_refund_procure.toFixed(1),
              settled: month_settled.toFixed(1),
              settled_refund: month_settled_refund.toFixed(1),
              settled_procure: month_settled_procure.toFixed(1),
              settled_refund_procure: month_settled_refund_procure.toFixed(1),
              close: month_close.toFixed(1),
              close_refund: month_close_refund.toFixed(1),
              close_procure: month_close_procure.toFixed(1),
              close_refund_procure: month_close_refund_procure.toFixed(1),
              transfer: month_transfer.toFixed(1),
              deduction: month_deduction.toFixed(1),
              promotion: month_promotion.toFixed(1),
              fake: month_fake.toFixed(1),
              fake_deduction: month_fake_deduction.toFixed(1),
              is_show: 0
            })
          }
          // 插入年数据
          const amount = pending + settled + close
          const income = pending + settled
          const profit = settled - settled_refund - settled_procure + settled_refund_procure - promotion - transfer - deduction - fake - fake_deduction
          const expect = pending - pending_refund - pending_procure + pending_refund_procure + profit
          this.list.unshift({
            create_date: y + '年汇总',
            amount: amount.toFixed(1),
            income: income.toFixed(1),
            profit: profit.toFixed(1),
            expect: expect.toFixed(1),
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
            is_show: 1
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
        this.shopList.forEach(v => {
          this.checkedShops.push(v.name)
          v.checked = true
        })
        this.getBoardReport()
      })
    },
    rowClassName({ row, rowIndex }) {
      if (row.is_show !== 0) {
        if (row.create_date.indexOf('年汇总') !== -1) {
          return 'year-row'
        }
        if (row.create_date.indexOf('月汇总') !== -1) {
          return 'month-row'
        }
      } else {
        return 'hidden-row'
      }
    },
    handleChange(value) {
      this.checkedShops = value
      this.getBoardReport()
    },
    handleRowClick(row, column, event) {
      if (row.create_date.indexOf('年汇总') !== -1) {
        // 处理年汇总
        const year = row.create_date.substring(0, 5)
        this.list.forEach(v => {
          if (v.create_date.indexOf('月汇总') !== -1 && v.create_date.indexOf(year) !== -1) {
            v.is_show = v.is_show === 0 ? 1 : 0
          } else if (v.create_date.indexOf('年汇总') === -1) {
            v.is_show = 0
          }
        })
      } else if (row.create_date.indexOf('月汇总') !== -1) {
        // 处理月汇总
        const month = row.create_date.substring(0, 7)
        this.list.forEach(v => {
          if (v.create_date.indexOf('月汇总') === -1 && v.create_date.indexOf(month) !== -1) {
            v.is_show = v.is_show === 0 ? 1 : 0
          }
        })
      }
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

.el-table .hidden-row {
  display: none;
}

/* 设置带边框的checkbox，选中后边框的颜色 */
.myCheckBox.is-bordered.is-checked {
  border-color: #888888;
}

/* 设置选中后的文字颜色 */
.myCheckBox .el-checkbox__input.is-checked+.el-checkbox__label {
  color: #000000;
}

/* 设置选中后对勾框的边框和背景颜色 */
.myCheckBox .el-checkbox__input.is-checked .el-checkbox__inner, .myCheckBox .el-checkbox__input.is-indeterminate .el-checkbox__inner {
  border-color: #888888;
  background-color:#888888;
}

/* 设置checkbox获得焦点后，对勾框的边框颜色 */
.myCheckBox .el-checkbox__input.is-focus .el-checkbox__inner{
  border-color: #888888;
}

/* 设置鼠标经过对勾框，对勾框边框的颜色 */
.myCheckBox .el-checkbox__inner:hover{
  border-color: #888888;
}
</style>
