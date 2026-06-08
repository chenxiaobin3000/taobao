<template>
  <div class="app-container">
    <el-form :model="listQuery" label-position="left" label-width="80px" style="width: 100%; padding: 0 1% 0 1%;">
      <el-row>
        <el-col :span="6">
          <el-form-item label="开始日期:">
            <el-date-picker v-model="listQuery.sdate" type="date" value-format="yyyy-MM-dd" class="filter-item" style="width: 150px;" @change="handleSelect" />
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item label="结束日期:">
            <el-date-picker v-model="listQuery.edate" type="date" value-format="yyyy-MM-dd" class="filter-item" style="width: 150px;" @change="handleSelect" />
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>

    <div class="missing-summary">
      <span>缺失: </span><span :style="{ color: missing ? 'red' : 'green' }">{{ missing || '无' }}</span>
    </div>

    <el-table ref="table" v-loading="loading" :data="list" :height="tableHeight" style="width: 100%" border fit highlight-current-row>
      <el-table-column align="center" label="日期" width="140px">
        <template slot-scope="scope">
          {{ scope.row.create_date }}
        </template>
      </el-table-column>
      <el-table-column align="left" header-align="center" label="进项">
        <template slot-scope="scope">
          {{ scope.row.from_text }}
        </template>
      </el-table-column>
      <el-table-column align="left" header-align="center" label="出项">
        <template slot-scope="scope">
          {{ scope.row.to_text }}
        </template>
      </el-table-column>
      <el-table-column align="left" header-align="center" label="校验" width="180px">
        <template slot-scope="scope">
          <span v-for="(item, index) in scope.row.check_items" :key="index">
            <span :style="{ color: item.success ? 'green' : 'red' }">{{ item.text }}</span><span v-if="index < scope.row.check_items.length - 1">;</span>
          </span>
        </template>
      </el-table-column>
      <el-table-column align="center" label="操作" width="100px">
        <template slot-scope="{row}">
          <el-button v-if="row.has_to" type="primary" size="mini" @click="handleRelate(row)">关联</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { getReceiptManagerList } from '@/api/middle/receiptManager'

export default {
  data() {
    return {
      tableHeight: 600,
      list: [],
      total: 0,
      missing: '',
      loading: false,
      listQuery: {
        sdate: '',
        edate: ''
      }
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
    this.initDate()
    this.getInvoiceList()
  },
  methods: {
    initDate() {
      const endDate = new Date()
      const startDate = new Date()
      startDate.setMonth(startDate.getMonth() - 6)
      this.listQuery.edate = this.formatDate(endDate)
      this.listQuery.sdate = this.formatDate(startDate)
    },
    formatDate(date) {
      const year = date.getFullYear()
      const month = `${date.getMonth() + 1}`.padStart(2, '0')
      const day = `${date.getDate()}`.padStart(2, '0')
      return `${year}-${month}-${day}`
    },
    handleSelect() {
      this.getInvoiceList()
    },
    getInvoiceList() {
      this.loading = true
      getReceiptManagerList(
        this.listQuery
      ).then(response => {
        this.total = response.data.data.total
        this.list = response.data.data.list || []
        this.missing = response.data.data.missing || ''
        this.loading = false
      }).catch(error => {
        this.loading = false
        Promise.reject(error)
      })
    },
    handleRelate(row) {
    }
  }
}
</script>

<style scoped>
.missing-summary {
  padding: 0 1% 8px 1%;
  font-size: 13px;
}
</style>
