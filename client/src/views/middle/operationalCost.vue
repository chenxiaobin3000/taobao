<template>
  <div class="app-container">
    <div class="excel-import-row">
      <upload-excel-component :on-success="handleSuccess" width="100%" line-height="32px" height="36px" />
      <div v-if="uploading || uploadProgress > 0" class="excel-import-progress">
        <el-progress :percentage="uploadProgress" />
        <span>{{ uploadProgressText }}</span>
      </div>
    </div>

    <el-row class="toolbar-row">
      <el-col :span="24">
        <el-button type="primary" size="mini" class="create-button" @click="handleCreate">新建</el-button>
      </el-col>
    </el-row>

    <el-table ref="table" v-loading="loading" :data="list" :height="tableHeight" style="width: 100%" border fit highlight-current-row>
      <el-table-column align="center" label="项目名称">
        <template slot-scope="scope">
          {{ scope.row.project_name }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="金额" width="160px">
        <template slot-scope="scope">
          {{ scope.row.amount }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="负责人" width="160px">
        <template slot-scope="scope">
          {{ userId2Name(scope.row.user_id) }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="备注" width="200px">
        <template slot-scope="scope">
          {{ scope.row.cost_note }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="日期" width="160px">
        <template slot-scope="scope">
          {{ scope.row.create_date }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="操作" width="160px">
        <template slot-scope="{row}">
          <el-button type="primary" size="mini" @click="handleUpdate(row)">编辑</el-button>
          <el-button type="danger" size="mini" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total > 0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.num" @pagination="getCostList" />

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogVisible">
      <el-form :model="temp" label-position="left" label-width="70px" style="width: 100%; padding: 0 4%;">
        <el-form-item label="项目名称">
          <el-input v-model="temp.project_name" />
        </el-form-item>
        <el-form-item label="金额">
          <el-input-number v-model="temp.amount" :precision="2" :step="1" :min="0" controls-position="right" style="width: 100%;" />
        </el-form-item>
        <el-form-item label="负责人">
          <el-select v-model="temp.user_id" class="filter-item" placeholder="请选择负责人" style="width: 100%;">
            <el-option v-for="item in userList" :key="item.id" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="temp.cost_note" />
        </el-form-item>
        <el-form-item label="日期">
          <el-date-picker v-model="temp.create_date" type="date" value-format="yyyy-MM-dd" class="filter-item" style="width: 150px;" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="dialogStatus === 'create' ? createData() : updateData()">确定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import Pagination from '@/components/Pagination'
import UploadExcelComponent from '@/components/UploadExcel'
import { excelDateToText } from '@/utils/excel'
import { getUserList } from '@/api/system/user'
import {
  addOperationalCost,
  addOperationalCostList,
  delOperationalCost,
  getOperationalCostList,
  setOperationalCost
} from '@/api/middle/operationalCost'

export default {
  components: { Pagination, UploadExcelComponent },
  data() {
    return {
      userdata: {},
      tableHeight: 600,
      list: [],
      total: 0,
      loading: false,
      uploading: false,
      uploadProgress: 0,
      uploadProgressText: '',
      userList: [],
      listQuery: {
        page: 1,
        num: 10
      },
      temp: {},
      dialogVisible: false,
      dialogStatus: '',
      textMap: {
        update: '修改运营成本',
        create: '新增运营成本'
      }
    }
  },
  mounted() {
    setTimeout(() => {
      if (this.$refs.table) {
        this.tableHeight = window.innerHeight - this.$refs.table.$el.offsetTop - 78
      }
    }, 1000)
  },
  created() {
    this.userdata = this.$store.getters.userdata
    this.resetTemp()
    this.loadUserList()
  },
  methods: {
    formatDate(date) {
      const year = date.getFullYear()
      const month = `${date.getMonth() + 1}`.padStart(2, '0')
      const day = `${date.getDate()}`.padStart(2, '0')
      return `${year}-${month}-${day}`
    },
    resetTemp() {
      this.temp = {
        id: 0,
        project_name: '',
        create_date: this.formatDate(new Date()),
        user_id: 0,
        amount: 0,
        cost_note: ''
      }
    },
    loadUserList() {
      getUserList({
        id: this.userdata.company.id,
        page: 1,
        num: 1000
      }).then(response => {
        this.userList = response.data.data.list || []
        this.getCostList()
      })
    },
    getCostList() {
      this.loading = true
      getOperationalCostList(this.listQuery).then(response => {
        this.total = response.data.data.total
        this.list = response.data.data.list || []
      }).finally(() => {
        this.loading = false
      })
    },
    userId2Name(id) {
      const user = this.userList.find(item => item.id === id)
      return user ? user.name : '异常'
    },
    userName2Id(name) {
      const user = this.userList.find(item => item.name === name)
      return user ? user.id : -1
    },
    handleSuccess({ results, header }) {
      this.uploadProgress = 0
      this.uploadProgressText = ''
      const createDate = header[0]
      const userName = header[1]
      const projectName = header[2]
      const amount = header[3]
      const note = header[4]
      const costs = []
      for (let i = 0; i < results.length; i++) {
        const row = results[i]
        const userId = this.userName2Id(row[userName])
        if (userId === -1) {
          this.$message({ type: 'error', message: `第${i + 1}行，负责人不存在` })
          return
        }
        costs.push({
          cdate: excelDateToText(row[createDate], 'yyyy-MM-dd'),
          uid: userId,
          name: row[projectName],
          amount: row[amount],
          note: row[note] || ''
        })
      }
      this.uploading = true
      this.uploadProgressText = `上传中 0/${costs.length}`
      addOperationalCostList({ m: costs }).then(() => {
        this.uploadProgress = 100
        this.uploadProgressText = `已导入 ${costs.length}/${costs.length}`
        this.$message({ type: 'success', message: '导入成功!' })
        this.getCostList()
      }).finally(() => {
        this.uploading = false
      })
    },
    handleCreate() {
      this.resetTemp()
      if (this.userList.length > 0) {
        this.temp.user_id = this.userList[0].id
      }
      this.dialogStatus = 'create'
      this.dialogVisible = true
    },
    createData() {
      addOperationalCost({
        cdate: this.temp.create_date,
        uid: this.temp.user_id,
        name: this.temp.project_name,
        amount: this.temp.amount,
        note: this.temp.cost_note
      }).then(() => {
        this.$message({ type: 'success', message: '新增成功!' })
        this.dialogVisible = false
        this.getCostList()
      })
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row)
      this.dialogStatus = 'update'
      this.dialogVisible = true
    },
    updateData() {
      setOperationalCost({
        id: this.temp.id,
        cdate: this.temp.create_date,
        uid: this.temp.user_id,
        name: this.temp.project_name,
        amount: this.temp.amount,
        note: this.temp.cost_note
      }).then(() => {
        this.$message({ type: 'success', message: '修改成功!' })
        this.dialogVisible = false
        this.getCostList()
      })
    },
    handleDelete(row) {
      this.$confirm('确定要删除吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        delOperationalCost({ id: row.id }).then(() => {
          this.$message({ type: 'success', message: '删除成功!' })
          this.getCostList()
        })
      })
    }
  }
}
</script>

<style scoped>
.excel-import-row {
  position: sticky;
  top: 0;
  z-index: 9;
  display: flex;
  align-items: center;
  gap: 16px;
  min-height: 48px;
  padding: 6px 1%;
  margin-bottom: 8px;
  background: #fff;
  border-bottom: 1px solid #d8dce5;
}

.excel-import-row > div:first-of-type {
  flex: 1 1 auto;
  min-width: 0;
}

.excel-import-row ::v-deep .drop {
  margin: 0;
  font-size: 13px;
  border-width: 1px;
}

.excel-import-progress {
  order: -1;
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1 1 auto;
  min-width: 240px;
  font-size: 13px;
  color: #606266;
}

.excel-import-progress ::v-deep .el-progress {
  flex: 1 1 auto;
}

.toolbar-row {
  min-height: 44px;
  padding: 0 1%;
}

.create-button {
  float: right;
  width: 60px;
}
</style>
