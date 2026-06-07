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
          <div>成交: {{ deal ? deal : 0 }}</div>
        </el-col>
        <el-col :span="3">
          <div>成交税: {{ deal_tax ? deal_tax : 0 }}</div>
        </el-col>
        <el-col :span="3">
          <div>推广: {{ promotion ? promotion : 0 }}</div>
        </el-col>
        <el-col :span="3">
          <div>报税: {{ tax ? tax : 0 }}</div>
        </el-col>
        <el-col :span="3">
          <div>扣款: {{ deduction ? deduction : 0 }}</div>
        </el-col>
      </el-row>
    </el-form>
    <el-table ref="table" v-loading="loading" :data="list" :height="tableHeight" style="width: 100%" border fit highlight-current-row :row-class-name="rowClassName" @row-click="handleRowClick">
      <el-table-column align="center" label="日期" width="120">
        <template slot-scope="scope">
          {{ scope.row.create_date }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="店铺" width="100">
        <template slot-scope="scope">
          {{ scope.row.name }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="成交" width="80">
        <template slot-scope="scope">
          {{ scope.row.deal }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="成交税" width="80">
        <template slot-scope="scope">
          {{ scope.row.deal_tax }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="推广" width="80">
        <template slot-scope="scope">
          {{ scope.row.promotion }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="报税" width="80">
        <template slot-scope="scope">
          {{ scope.row.tax }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="扣款" width="70">
        <template slot-scope="scope">
          {{ scope.row.deduction }}
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
import { getTaxReport } from '@/api/report/taxReport'
import { getOwnShopList } from '@/api/system/shop'

export default {
  data() {
    return {
      userdata: {},
      tableHeight: 600,
      list: null,
      deal: 0, // 成交
      deal_tax: 0, // 成交报税
      tax: 0, // 报税
      deduction: 0, // 扣款
      promotion: 0, // 推广
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
    getTaxReport() {
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
      getTaxReport({
        ids: ids
      }).then(response => {
        this.deal = response.data.data.deal
        this.deal_tax = response.data.data.deal_tax
        this.tax = response.data.data.tax
        this.deduction = response.data.data.deduction
        this.promotion = response.data.data.promotion
        this.buildList(response.data.data.list)
        this.loading = false
      }).catch(error => {
        this.loading = false
        Promise.reject(error)
      })
    },
    buildList(data) {
      this.list = []
      const currentYear = new Date().getFullYear()
      const currentMonth = new Date().getMonth()
      for (let y = 2025; y <= currentYear; ++y) {
        const yearTotal = this.initTotal()
        const monthRows = []
        const monthTotals = []
        for (let m = 0; m < 12; ++m) {
          if (y === currentYear && m > currentMonth) {
            break
          }
          const key = m > 8 ? y + '-' + (m + 1) : y + '-0' + (m + 1)
          const monthTotal = this.initTotal()
          const shopRows = []
          this.shopList.forEach(v => {
            if (!this.checkedShops.includes(v.name)) {
              return
            }
            const temp = data[key][v.id]
            temp.name = v.name
            temp.create_date = y + '年' + (m + 1) + '月'
            temp.is_show = 0
            temp.row_type = 'shop'
            temp.year_key = y
            temp.month_key = y + '年' + (m + 1) + '月'
            this.addTotal(yearTotal, temp)
            this.addTotal(monthTotal, temp)
            shopRows.push(temp)
          })
          monthTotals[m] = monthTotal
          monthRows[m] = [
            this.buildTotalRow(y + '年' + (m + 1) + '月汇总', monthTotal, 0, 'month', y, y + '年' + (m + 1) + '月'),
            ...shopRows
          ]
        }
        const yearRows = []
        for (let m = monthRows.length - 1; m >= 0; --m) {
          yearRows.push(...monthRows[m])
          if (m === 0) {
            yearRows.push(...this.buildQuarterRows(y, 1, monthTotals, data, 0, 2))
          } else if (m === 3) {
            yearRows.push(...this.buildQuarterRows(y, 2, monthTotals, data, 3, 5))
          }
        }
        this.list.unshift(this.buildTotalRow(y + '年汇总', yearTotal, 1, 'year', y), ...yearRows)
      }
    },
    initTotal() {
      return {
        deal: 0,
        deal_tax: 0,
        tax: 0,
        deduction: 0,
        promotion: 0
      }
    },
    addTotal(total, item) {
      total.deal += item.deal
      total.deal_tax += item.deal_tax
      total.tax += item.tax
      total.deduction += item.deduction
      total.promotion += item.promotion
    },
    buildQuarterTotal(monthTotals, start, end) {
      const total = this.initTotal()
      for (let i = start; i <= end; ++i) {
        if (monthTotals[i]) {
          this.addTotal(total, monthTotals[i])
        }
      }
      return total
    },
    buildQuarterRows(year, quarter, monthTotals, data, start, end) {
      const quarterKey = year + '年' + quarter + '季度'
      const rows = [
        this.buildTotalRow(quarterKey, this.buildQuarterTotal(monthTotals, start, end), 0, 'quarter', year, null, quarterKey)
      ]
      this.shopList.forEach(v => {
        if (!this.checkedShops.includes(v.name)) {
          return
        }
        const total = this.initTotal()
        for (let i = start; i <= end; ++i) {
          const key = i > 8 ? year + '-' + (i + 1) : year + '-0' + (i + 1)
          if (data[key] && data[key][v.id]) {
            this.addTotal(total, data[key][v.id])
          }
        }
        rows.push(this.buildTotalRow(quarterKey, total, 0, 'quarter_shop', year, null, quarterKey, v.name))
      })
      return rows
    },
    buildTotalRow(createDate, total, isShow, rowType, yearKey, monthKey, quarterKey, name) {
      return {
        create_date: createDate,
        name: name,
        deal: total.deal.toFixed(1),
        deal_tax: total.deal_tax.toFixed(1),
        tax: total.tax.toFixed(1),
        deduction: total.deduction.toFixed(1),
        promotion: total.promotion.toFixed(1),
        is_show: isShow,
        row_type: rowType,
        year_key: yearKey,
        month_key: monthKey,
        quarter_key: quarterKey
      }
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
        this.getTaxReport()
      })
    },
    rowClassName({ row, rowIndex }) {
      if (row.is_show !== 0) {
        if (row.row_type === 'year') {
          return 'year-row'
        }
        if (row.row_type === 'month' || row.row_type === 'quarter') {
          return 'month-row'
        }
      } else {
        return 'hidden-row'
      }
    },
    handleChange(value) {
      this.checkedShops = value
      this.getTaxReport()
    },
    handleRowClick(row, column, event) {
      if (row.row_type === 'year') {
        this.list.forEach(v => {
          if ((v.row_type === 'month' || v.row_type === 'quarter') && v.year_key === row.year_key) {
            v.is_show = v.is_show === 0 ? 1 : 0
          } else if (v.row_type !== 'year') {
            v.is_show = 0
          }
        })
      } else if (row.row_type === 'month') {
        this.list.forEach(v => {
          if (v.row_type === 'shop' && v.month_key === row.month_key) {
            v.is_show = v.is_show === 0 ? 1 : 0
          }
        })
      } else if (row.row_type === 'quarter') {
        this.list.forEach(v => {
          if (v.row_type === 'quarter_shop' && v.quarter_key === row.quarter_key) {
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
