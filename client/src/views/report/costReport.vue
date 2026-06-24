<template>
  <div class="app-container">
    <el-form label-position="left" label-width="50px" style="width: 100%; padding: 0 1% 0 1%;">
      <el-row>
        <el-col :span="12">
          <el-checkbox-group v-model="checkedShops" @change="handleChange">
            <el-checkbox v-for="item in shopList" :key="item.id" :label="item.name" :value="item.id" class="myCheckBox">
              <div style="font-size:small">{{ item.name }}</div>
            </el-checkbox>
          </el-checkbox-group>
        </el-col>
        <el-col :span="6">
          <el-form-item label="开始日期:" label-width="80px" style="float:right;margin-left:10px;">
            <el-date-picker v-model="listQuery.sdate" type="date" value-format="yyyy-MM-dd" class="filter-item" style="width: 150px;" @change="handleSelect" />
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item label="结束日期:" label-width="80px" style="float:right;margin-left:10px;">
            <el-date-picker v-model="listQuery.edate" type="date" value-format="yyyy-MM-dd" class="filter-item" style="width: 150px;" @change="handleSelect" />
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>
    <el-table ref="table" v-loading="loading" :data="list" :height="tableHeight" style="width: 100%" border fit highlight-current-row :row-class-name="rowClassName" @row-click="handleRowClick">
      <el-table-column align="center" label="日期" width="140">
        <template slot-scope="scope">{{ scope.row.create_date }}</template>
      </el-table-column>
      <el-table-column align="center" label="店铺" width="140">
        <template slot-scope="scope">{{ scope.row.name }}</template>
      </el-table-column>
      <el-table-column align="center" label="总成本" width="120">
        <template slot-scope="scope">{{ scope.row.total_cost }}</template>
      </el-table-column>
      <el-table-column align="center" label="推广" width="120">
        <template slot-scope="scope">{{ scope.row.promotion }}</template>
      </el-table-column>
      <el-table-column align="center" label="采购" width="120">
        <template slot-scope="scope">{{ scope.row.purchase }}</template>
      </el-table-column>
      <el-table-column align="center" label="待结算" width="120">
        <template slot-scope="scope">{{ scope.row.pending }}</template>
      </el-table-column>
      <el-table-column align="center" label="备注">
        <div><br></div>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import { getCostReport } from '@/api/report/costReport'
import { getOwnShopList } from '@/api/system/shop'

export default {
  data() {
    return {
      userdata: {},
      tableHeight: 600,
      list: [],
      loading: false,
      checkedShops: [],
      shopList: [],
      listQuery: {
        sdate: null,
        edate: null
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
      this.$message({ type: 'error', message: '不支持搜索' })
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
    this.initDate()
    this.getOwnShopList()
  },
  methods: {
    getCostReport() {
      const ids = []
      this.shopList.forEach(v => {
        if (this.checkedShops.includes(v.name)) {
          ids.push(v.id)
        }
      })
      if (ids.length === 0) {
        this.$message({ type: 'error', message: '至少要选中一个店铺' })
        return
      }
      this.loading = true
      getCostReport({
        ids: ids,
        sdate: this.listQuery.sdate,
        edate: this.listQuery.edate
      }).then(response => {
        const data = response.data.data
        this.buildList(data.list)
        this.loading = false
      }).catch(error => {
        this.loading = false
        Promise.reject(error)
      })
    },
    buildList(data) {
      this.list = []
      Object.keys(data).forEach(date => {
        const summary = data[date].summary
        summary.name = '合计'
        summary.is_summary = 1
        summary.is_show = 1
        this.list.push(summary)
        this.shopList.forEach(shop => {
          if (!this.checkedShops.includes(shop.name)) {
            return
          }
          const row = data[date][shop.id]
          if (!row) {
            return
          }
          row.name = shop.name
          row.is_summary = 0
          row.is_show = 0
          this.list.push(row)
        })
      })
    },
    initDate() {
      const endDate = new Date()
      const startDate = new Date()
      startDate.setTime(startDate.getTime() - 1000 * 60 * 60 * 24 * 29)
      this.listQuery.sdate = this.formatDate(startDate)
      this.listQuery.edate = this.formatDate(endDate)
    },
    formatDate(date) {
      const year = date.getFullYear()
      const month = date.getMonth() + 1
      const day = date.getDate()
      return year + '-' + (month > 9 ? month : '0' + month) + '-' + (day > 9 ? day : '0' + day)
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
        this.getCostReport()
      })
    },
    rowClassName({ row, rowIndex }) {
      if (row.is_summary === 1) {
        return 'summary-row'
      }
      if (row.is_show === 0) {
        return 'hidden-row'
      }
      return ''
    },
    handleChange(value) {
      this.checkedShops = value
      this.getCostReport()
    },
    handleSelect() {
      this.getCostReport()
    },
    handleRowClick(row, column, event) {
      if (row.is_summary !== 1) {
        return
      }
      this.list.forEach(v => {
        if (v.is_summary !== 1 && v.create_date === row.create_date) {
          v.is_show = v.is_show === 0 ? 1 : 0
        }
      })
    }
  }
}
</script>

<style lang="scss">
.el-table .summary-row {
  background-color: rgba(235, 235, 235, 0.5);
  font-weight: bold;
}

.el-table .hidden-row {
  display: none;
}

.myCheckBox.is-bordered.is-checked {
  border-color: #888888;
}

.myCheckBox .el-checkbox__input.is-checked+.el-checkbox__label {
  color: #000000;
}

.myCheckBox .el-checkbox__input.is-checked .el-checkbox__inner, .myCheckBox .el-checkbox__input.is-indeterminate .el-checkbox__inner {
  border-color: #888888;
  background-color:#888888;
}

.myCheckBox .el-checkbox__input.is-focus .el-checkbox__inner{
  border-color: #888888;
}

.myCheckBox .el-checkbox__inner:hover{
  border-color: #888888;
}
</style>
