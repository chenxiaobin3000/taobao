<template>
  <div class="app-container">
    <el-form :model="listQuery" label-position="left" label-width="70px" style="width: 100%; padding: 0 1% 0 1%;">
      <el-form-item label="店铺:" prop="shopName">
        <el-select v-model="listQuery.id" class="filter-item" placeholder="请选择店铺" @change="handleChange">
          <el-option v-for="item in shopList" :key="item.id" :label="item.name" :value="item.id" />
        </el-select>
      </el-form-item>
    </el-form>
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
          {{ scope.row.user_id }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="备注" width="160px">
        <template slot-scope="scope">
          {{ scope.row.misc_note }}
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

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.num" @pagination="getUserList" />

    <!-- 杂项信息编辑 -->
    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogVisible">
      <el-form :model="temp" label-position="left" label-width="70px" style="width: 100%; padding: 0 4% 0 4%;">
        <el-form-item label="项目名称">
          <el-input v-model="temp.project_name" />
        </el-form-item>
        <el-form-item label="金额">
          <el-input v-model="temp.amount" />
        </el-form-item>
        <el-form-item label="负责人">
          <el-select v-model="temp.user_id" class="filter-item" placeholder="请选择负责人">
            <el-option v-for="item in userList" :key="item.id" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="temp.misc_note" />
        </el-form-item>
        <el-form-item label="日期">
          <div>{{ temp.create_date }}</div>
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
import { mapState } from 'vuex'
import Pagination from '@/components/Pagination'
import { getShopList } from '@/api/system/shop'
import { getUserList } from '@/api/system/user'
import { getMiscList, addMisc, setMisc, delMisc } from '@/api/middle/miscellaneous'

export default {
  components: { Pagination },
  data() {
    return {
      userdata: {},
      tableHeight: 600,
      list: null,
      total: 0,
      loading: false,
      shopList: null, // 本公司所有店铺列表
      userList: null, // 本公司所有用户列表
      listQuery: {
        id: 0,
        page: 1,
        num: 10,
        search: null
      },
      temp: {},
      dialogVisible: false,
      dialogStatus: '',
      textMap: {
        update: '修改杂项信息',
        create: '新增杂项'
      }
    }
  },
  computed: {
    ...mapState({
      search: state => state.header.search,
      create: state => state.header.create
    })
  },
  watch: {
    search(newVal, oldVal) {
      this.listQuery.search = newVal
      this.getShopList()
    },
    create() {
      this.resetTemp()
      this.temp.user_id = this.userList[0].id
      this.dialogStatus = 'create'
      this.dialogVisible = true
    }
  },
  mounted: function() {
    setTimeout(() => {
      this.tableHeight = window.innerHeight - this.$refs.table.$el.offsetTop - 78
    }, 1000)
  },
  created() {
    this.userdata = this.$store.getters.userdata
    this.listQuery.id = 0
    this.resetTemp()
    this.getShopList()
  },
  methods: {
    resetTemp() {
      this.temp = {
        id: 0,
        marketId: 0,
        name: ''
      }
    },
    getMiscList() {
      this.loading = true
      getMiscList(
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
    getShopList() {
      getShopList({
        id: this.userdata.company.id,
        page: 1,
        num: 1000
      }).then(response => {
        this.shopList = response.data.data.list
        this.listQuery.id = this.shopList[0].id
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
        this.getMiscList()
      })
    },
    handleChange() {
      this.getMiscList()
    },
    createData() {
      addMisc({
        name: this.temp.name,
        cid: this.userdata.company.id,
        mid: this.temp.marketId
      }).then(() => {
        this.$message({ type: 'success', message: '新增成功!' })
        this.getShopList()
        this.dialogVisible = false
      })
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row)
      this.dialogStatus = 'update'
      this.dialogVisible = true
    },
    updateData() {
      setMisc({
        id: this.temp.id,
        name: this.temp.name
      }).then(() => {
        this.$message({ type: 'success', message: '修改成功!' })
        this.getUserList()
        this.dialogVisible = false
      })
    },
    handleDelete(row) {
      this.$confirm('确定要删除吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        delMisc({
          id: row.id
        }).then(() => {
          this.$message({ type: 'success', message: '删除成功!' })
          this.getRoles()
        })
      })
    }
  }
}
</script>
