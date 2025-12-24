<template>
  <div class="app-container">
    <el-table v-loading="loading" :data="list" style="width: 100%;" border highlight-current-row>
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
      routes: [],
      list: [],
      loading: false,
      listQuery: {
        id: 0,
        gid: 0,
        search: null
      },
      temp: {},
      checkStrictly: false,
      defaultProps: {
        children: 'children',
        label: 'title'
      },
      dialogVisible: false,
      dialogStatus: '',
      textMap: {
        update: '修改角色信息',
        create: '新建角色'
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
      this.getRoles()
    },
    create() {
      this.resetTemp()
      if (this.$refs.tree) {
        this.$refs.tree.setCheckedNodes([])
      }
      this.dialogStatus = 'create'
      this.dialogVisible = true
    }
  },
  created() {
    this.userdata = this.$store.getters.userdata
    this.listQuery.id = this.userdata.user.id
    this.routes = treeGenerate.generateRoutes(MyRoleData)
    this.getRoles()
  },
  methods: {
    resetTemp() {
      this.temp = {
        id: 0,
        name: '',
        routes: []
      }
    },
    getRoles() {
      this.loading = true
      getRoleList(
        this.listQuery
      ).then(response => {
        this.list = response.data.data.roles
        this.list.forEach(role => {
          // 角色列表没有包含权限信息
          role.routes = null
        })
        this.loading = false
      }).catch(error => {
        this.loading = false
        Promise.reject(error)
      })
    },
    createData() {
      const checkedKeys = this.$refs.tree.getCheckedKeys()
      this.temp.routes = treeGenerate.generateTree(MyRoleData, '/', checkedKeys)
      addRole({
        id: this.userdata.user.id,
        name: this.temp.name,
        permissions: this.temp.routes
      }).then(() => {
        this.$message({ type: 'success', message: '新增成功!' })
        this.getRoles()
        this.dialogVisible = false
      })
    },
    handleUpdate(scope) {
      this.dialogStatus = 'update'
      this.dialogVisible = true
      this.temp = deepClone(scope.row)
      if (this.temp.routes) {
        this.checkStrictly = true // 保护父子节点不相互影响
        this.$nextTick(() => {
          const routes = treeGenerate.filterAsyncRoutes(MyRoleData, this.temp.routes)
          this.$refs.tree.setCheckedNodes(treeGenerate.generateArr(routes))
          this.checkStrictly = false
        })
      } else {
        getRole({
          id: this.userdata.user.id,
          rid: this.temp.id
        }).then(response => {
          this.temp.routes = response.data.data.permissions
          scope.row.routes = this.temp.routes
          this.checkStrictly = true // 保护父子节点不相互影响
          this.$nextTick(() => {
            const routes = treeGenerate.filterAsyncRoutes(MyRoleData, this.temp.routes)
            this.$refs.tree.setCheckedNodes(treeGenerate.generateArr(routes))
            this.checkStrictly = false
          })
        })
      }
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

<style lang="scss" scoped>
.app-container {
  .roles-table {
    margin-top: 30px;
  }
  .permission-tree {
    margin-bottom: 30px;
  }
}
</style>
