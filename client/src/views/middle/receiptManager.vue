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
        <el-col :span="4">
          <quick-date :query="listQuery" @change="handleSelect" />
        </el-col>
      </el-row>
    </el-form>

    <el-table ref="table" v-loading="loading" :data="list" :height="tableHeight" style="width: 100%" border fit highlight-current-row>
      <el-table-column align="left" header-align="center" label="出项">
        <template slot-scope="scope">
          {{ scope.row.to_text }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="数量" width="80px">
        <template slot-scope="scope">
          {{ scope.row.to_num }}
        </template>
      </el-table-column>
      <el-table-column align="left" header-align="center" label="进项">
        <template slot-scope="scope">
          {{ scope.row.from_text }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="数量" width="80px">
        <template slot-scope="scope">
          {{ scope.row.from_num }}
        </template>
      </el-table-column>
      <el-table-column align="left" header-align="center" label="校验" width="180px">
        <template slot-scope="scope">
          <span :style="{ color: scope.row.check_success ? 'green' : 'red' }">{{ scope.row.check_text }}</span>
        </template>
      </el-table-column>
      <el-table-column align="left" header-align="center" label="备注">
        <template slot-scope="scope">
          {{ scope.row.receipt_note }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="操作（关联）" width="120px">
        <template slot-scope="{row}">
          <el-button v-if="row.has_from && !row.has_to" type="primary" size="mini" @click="handleRelate(row)">关联</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog title="关联发票项目" :visible.sync="mapDialog.visible" width="420px">
      <el-form label-width="80px">
        <el-form-item label="进项项目">
          <span>{{ mapDialog.itemName }}</span>
        </el-form-item>
        <el-form-item label="关联出项">
          <el-select v-model="mapDialog.mapId" placeholder="请选择出项项目" style="width: 100%;">
            <el-option
              v-for="item in relateOptions"
              :key="item.project_id"
              :label="relateOptionLabel(item)"
              :value="item.project_id"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button @click="mapDialog.visible = false">取消</el-button>
        <el-button type="primary" :loading="mapDialog.loading" @click="confirmRelate">确认</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { getReceiptManagerList, setReceiptMap } from '@/api/middle/receiptManager'

export default {
  data() {
    return {
      tableHeight: 600,
      list: [],
      total: 0,
      loading: false,
      mapDialog: {
        visible: false,
        loading: false,
        itemId: 0,
        itemName: '',
        mapId: ''
      },
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
        this.loading = false
      }).catch(error => {
        this.loading = false
        Promise.reject(error)
      })
    },
    handleRelate(row) {
      this.mapDialog = {
        visible: true,
        loading: false,
        itemId: row.project_id,
        itemName: row.from_text,
        mapId: ''
      }
    },
    relateOptionLabel(row) {
      if (row.check_success) {
        return row.to_text
      }
      return `${row.to_text}（${row.check_text}）`
    },
    confirmRelate() {
      if (!this.mapDialog.mapId) {
        this.$message({ type: 'warning', message: '请选择出项项目' })
        return
      }
      this.mapDialog.loading = true
      setReceiptMap({
        item_id: this.mapDialog.itemId,
        map_id: this.mapDialog.mapId
      }).then(() => {
        this.$message({ type: 'success', message: '关联成功' })
        this.mapDialog.visible = false
        this.getInvoiceList()
      }).finally(() => {
        this.mapDialog.loading = false
      })
    }
  },
  computed: {
    relateOptions() {
      return this.list.filter(item => {
        return item.has_to && (!item.has_from || !item.check_success) && item.project_id !== this.mapDialog.itemId
      })
    }
  }
}
</script>

<style scoped>
</style>
