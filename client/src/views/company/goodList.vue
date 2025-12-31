<template>
  <div class="app-container">
    <el-form-item label="店铺" prop="shopName">
      <el-select v-model="temp.shopId" class="filter-item" placeholder="请选择店铺">
        <el-option v-for="item in shopList" :key="item.id" :label="item.name" :value="item.id" />
      </el-select>
    </el-form-item>
    <el-table ref="table" v-loading="loading" :data="list" style="width: 100%;" border highlight-current-row>
      <el-table-column align="center" label="角色名称" width="220">
        <template slot-scope="scope">
          {{ scope.row.name }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="操作" width="220">
        <template slot-scope="scope">
          <el-button type="primary" size="small" @click="handleUpdate(scope)">编辑</el-button>
          <el-button type="danger" size="small" @click="handleDelete(scope)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogVisible">
      <el-form :model="temp" label-width="80px" label-position="left">
        <el-form-item label="角色名称">
          <el-input v-model="temp.name" />
        </el-form-item>
        <el-form-item label="权限">
          <el-tree ref="tree" :check-strictly="checkStrictly" :data="routes" :props="defaultProps" show-checkbox node-key="path" class="permission-tree" />
        </el-form-item>
      </el-form>
      <div style="text-align:right;">
        <el-button type="danger" @click="dialogVisible=false">取消</el-button>
        <el-button type="primary" @click="dialogStatus==='create'?createData():updateData()">确定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import { deepClone } from '@/utils'
import { MyRoleData } from '@/utils/role-data'
import { treeGenerate } from '@/utils/tree'
import { getRoleList, addRole, delRole, setRole, getRole } from '@/api/role'

export default {
  data() {
    return {
      userdata: {},
      tableHeight: 600,
      list: null,
      total: 0,
      loading: false,
      shopList: [], // 本公司所有店铺列表
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
        update: '修改商品信息',
        create: '新建商品'
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
      this.getGoodList()
    },
    create() {
      this.resetTemp()
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
        gid: '',
        name: '',
        sname: '',
      }
    },
    getGoodList() {
      this.loading = true
      getGoodList(
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
        this.getGoodList()
      })
    },
    createData() {
      addGood({
        id: this.temp.id,
        gid: this.temp.gid,
        name: this.temp.name,
        sname: this.temp.sname
      }).then(() => {
        this.$message({ type: 'success', message: '新增成功!' })
        this.getGoodList()
        this.dialogVisible = false
      })
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row)
      this.temp.roleId = row.role_id
      this.temp.roleName = row.role
      this.dialogStatus = 'update'
      this.dialogVisible = true
    },
    updateData() {
      const checkedKeys = this.$refs.tree.getCheckedKeys()
      this.temp.routes = treeGenerate.generateTree(MyRoleData, '/', checkedKeys)
      setRole({
        id: this.userdata.user.id,
        rid: this.temp.id,
        name: this.temp.name,
        permissions: this.temp.routes
      }).then(() => {
        this.$message({ type: 'success', message: '修改成功!' })
        this.getRoles()
        this.dialogVisible = false
      })
      // 清除缓存路由，下次展示直接从服务器获取数据
      this.list.forEach(role => {
        if (role.id === this.temp.id) {
          role.routes = null
        }
      })
    },
    handleDelete({ $index, row }) {
      this.$confirm('确定要删除吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        delRole({
          id: this.userdata.user.id,
          rid: row.id
        }).then(() => {
          this.$message({ type: 'success', message: '删除成功!' })
          this.getRoles()
        })
      })
    }
  }
}
</script>
