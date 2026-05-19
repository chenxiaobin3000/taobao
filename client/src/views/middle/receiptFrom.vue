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
        <el-col :span="18">
          <el-button type="primary" size="mini" style="float:right;width:60px" @click="handleCreate()">新建</el-button>
        </el-col>
      </el-row>
    </el-form>

    <el-table ref="table" v-loading="loading" :data="list" :height="tableHeight" style="width: 100%" border fit highlight-current-row>
      <el-table-column align="center" label="项目名称" width="300px">
        <template slot-scope="scope">
          {{ projectId2Name(scope.row.project_id) }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="数量" width="80px">
        <template slot-scope="scope">
          {{ scope.row.project_num }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="填报人" width="80px">
        <template slot-scope="scope">
          {{ userId2Name(scope.row.user_id) }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="备注">
        <template slot-scope="scope">
          {{ scope.row.receipt_note }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="日期" width="160px">
        <template slot-scope="scope">
          {{ scope.row.create_date }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="操作" width="160">
        <template slot-scope="{row}">
          <el-button type="primary" size="mini" @click="handleUpdate(row)">编辑</el-button>
          <el-button type="danger" size="mini" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.num" @pagination="getReceiptFromList" />

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogVisible">
      <el-form :model="temp" label-position="left" label-width="70px" style="width: 100%; padding: 0 4% 0 4%;">
        <el-form-item label="项目名称">
          <el-select v-model="temp.project_id" class="filter-item" placeholder="请选择项目">
            <el-option v-for="item in projectList" :key="item.id" :label="item.project_name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="数量">
          <el-input v-model="temp.project_num" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="temp.receipt_note" />
        </el-form-item>
        <el-form-item label="日期">
          <el-date-picker v-model="temp.create_date" type="date" value-format="yyyy-MM-dd" class="filter-item" style="width: 150px;" />
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
import { getOwnShopList } from '@/api/system/shop'
import { getUserList } from '@/api/system/user'
import { getReceiptItemList } from '@/api/middle/receiptItem'
import { addReceiptFrom, setReceiptFrom, delReceiptFrom, getReceiptFromList } from '@/api/middle/receiptFrom'

export default {
  components: { Pagination },
  data() {
    return {
      userdata: {},
      tableHeight: 600,
      list: null,
      total: 0,
      loading: false,
      shopList: [],
      userList: [],
      projectList: [],
      listQuery: {
        id: 0,
        page: 1,
        num: 10
      },
      temp: {},
      dialogVisible: false,
      dialogStatus: '',
      textMap: {
        update: '修改进项',
        create: '新增进项'
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
    this.userdata = this.$store.getters.userdata
    this.listQuery.id = this.$store.getters.shop
    this.resetTemp()
    this.getOwnShopList()
  },
  methods: {
    resetTemp() {
      this.temp = {
        id: 0,
        create_date: new Date().toLocaleDateString().replace(/\//g, '-'),
        project_id: 0,
        project_num: 1,
        receipt_note: ''
      }
    },
    getReceiptFromList() {
      this.loading = true
      getReceiptFromList(
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
    getOwnShopList() {
      getOwnShopList({
        id: this.userdata.company.id,
        uid: this.userdata.user.id
      }).then(response => {
        this.shopList = response.data.data
        if (this.listQuery.id === 0 && this.shopList.length > 0) {
          this.listQuery.id = this.shopList[0].id
        }
        this.getUserList()
      })
    },
    getUserList() {
      getUserList({
        id: this.userdata.company.id,
        page: 1,
        num: 1000
      }).then(response => {
        this.userList = response.data.data.list
        this.loadReceiptItemList()
      })
    },
    loadReceiptItemList() {
      getReceiptItemList({
        page: 1,
        num: 1000
      }).then(response => {
        this.projectList = response.data.data.list || []
        this.getReceiptFromList()
      })
    },
    userId2Name(id) {
      for (let i = 0; i < this.userList.length; ++i) {
        if (this.userList[i].id === id) {
          return this.userList[i].name
        }
      }
      return '异常'
    },
    projectId2Name(id) {
      for (let i = 0; i < this.projectList.length; ++i) {
        if (this.projectList[i].id === id) {
          return this.projectList[i].project_name
        }
      }
      return '异常'
    },
    handleChange() {
      this.listQuery.page = 1
      this.$store.commit('header/SET_HEADER_SHOP', this.listQuery.id)
      this.getReceiptFromList()
    },
    handleCreate() {
      this.resetTemp()
      if (this.projectList.length > 0) {
        this.temp.project_id = this.projectList[0].id
      }
      this.dialogStatus = 'create'
      this.dialogVisible = true
    },
    createData() {
      addReceiptFrom({
        id: this.listQuery.id,
        cdate: this.temp.create_date,
        name: this.temp.project_id,
        num: this.temp.project_num,
        note: this.temp.receipt_note
      }).then(() => {
        this.$message({ type: 'success', message: '新增成功!' })
        this.getReceiptFromList()
        this.dialogVisible = false
      })
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row)
      this.dialogStatus = 'update'
      this.dialogVisible = true
    },
    updateData() {
      setReceiptFrom({
        id: this.temp.id,
        cdate: this.temp.create_date,
        name: this.temp.project_id,
        num: this.temp.project_num,
        note: this.temp.receipt_note
      }).then(() => {
        this.$message({ type: 'success', message: '修改成功!' })
        this.getReceiptFromList()
        this.dialogVisible = false
      })
    },
    handleDelete(row) {
      this.$confirm('确定要删除吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        delReceiptFrom({
          id: row.id
        }).then(() => {
          this.$message({ type: 'success', message: '删除成功!' })
          this.getReceiptFromList()
        })
      })
    }
  }
}
</script>
