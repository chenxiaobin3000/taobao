<template>
  <div class="app-container">
    <el-form :model="listQuery" label-position="left" label-width="50px" style="width: 100%; padding: 0 1% 0 1%;">
      <el-form-item>
        <el-button type="primary" size="mini" style="float:right;width:60px" @click="handleCreate()">新建</el-button>
      </el-form-item>
    </el-form>

    <el-table ref="table" v-loading="loading" :data="list" :height="tableHeight" style="width: 100%" border fit highlight-current-row>
      <el-table-column align="center" label="项目名称" width="300">
        <template slot-scope="scope">
          {{ scope.row.project_name }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="备注">
        <template slot-scope="scope">
          {{ scope.row.project_note }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="操作" width="160">
        <template slot-scope="{row}">
          <el-button type="primary" size="mini" @click="handleUpdate(row)">编辑</el-button>
          <el-button type="danger" size="mini" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.num" @pagination="getReceiptItemList" />

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogVisible">
      <el-form :model="temp" label-position="left" label-width="70px" style="width: 100%; padding: 0 4% 0 4%;">
        <el-form-item label="项目名称">
          <el-input v-model="temp.project_name" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="temp.project_note" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="danger" @click="dialogVisible=false">取消</el-button>
        <el-button type="primary" @click="dialogStatus==='create'?createData():updateData()">确定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import Pagination from '@/components/Pagination'
import { addReceiptItem, setReceiptItem, delReceiptItem, getReceiptItemList } from '@/api/middle/receiptItem'

export default {
  components: { Pagination },
  data() {
    return {
      tableHeight: 600,
      list: null,
      total: 0,
      loading: false,
      listQuery: {
        page: 1,
        num: 10
      },
      temp: {},
      dialogVisible: false,
      dialogStatus: '',
      textMap: {
        update: '修改发票项',
        create: '新增发票项'
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
    this.resetTemp()
    this.getReceiptItemList()
  },
  methods: {
    resetTemp() {
      this.temp = {
        id: 0,
        project_name: '',
        project_note: ''
      }
    },
    getReceiptItemList() {
      this.loading = true
      getReceiptItemList(
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
    handleCreate() {
      this.resetTemp()
      this.dialogStatus = 'create'
      this.dialogVisible = true
    },
    createData() {
      addReceiptItem({
        name: this.temp.project_name,
        note: this.temp.project_note
      }).then(() => {
        this.$message({ type: 'success', message: '新增成功!' })
        this.getReceiptItemList()
        this.dialogVisible = false
      })
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row)
      this.dialogStatus = 'update'
      this.dialogVisible = true
    },
    updateData() {
      setReceiptItem({
        id: this.temp.id,
        name: this.temp.project_name,
        note: this.temp.project_note
      }).then(() => {
        this.$message({ type: 'success', message: '修改成功!' })
        this.getReceiptItemList()
        this.dialogVisible = false
      })
    },
    handleDelete(row) {
      this.$confirm('确定要删除吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        delReceiptItem({
          id: row.id
        }).then(() => {
          this.$message({ type: 'success', message: '删除成功!' })
          this.getReceiptItemList()
        })
      })
    }
  }
}
</script>
