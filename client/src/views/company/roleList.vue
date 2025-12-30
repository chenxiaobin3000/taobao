<template>
  <div class="app-container">
    <el-table ref="table" v-loading="loading" :data="list" style="width: 100%;" border highlight-current-row>
      <el-table-column align="center" label="角色名称">
        <template slot-scope="scope">
          {{ scope.row.name }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="操作" width="220">
        <template slot-scope="{row}">
          <el-button type="primary" size="small" @click="handleUpdate(row)">编辑</el-button>
          <el-button type="danger" size="small" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogVisible">
      <el-form :model="temp" label-width="80px" label-position="left">
        <el-form-item label="角色名称">
          <el-input v-model="temp.name" />
        </el-form-item>
        <el-form-item label="权限">
          <el-tree ref="tree" :data="routes" node-key="id" show-checkbox check-strictly @check="handleRoleChange" />
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
import { MyRoleData } from '@/utils/role-data'
import { getRoleList, addRole, delRole, setRole } from '@/api/role'

export default {
  data() {
    return {
      userdata: {},
      routes: [],
      tableHeight: 600,
      list: null,
      loading: false,
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
      this.getRoleList()
    },
    create() {
      this.resetTemp()
      this.$nextTick(() => {
        this.$refs.tree.setCheckedKeys([])
      })
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
    this.listQuery.id = this.userdata.company.id
    this.routes = MyRoleData
    this.getRoleList()
  },
  methods: {
    resetTemp() {
      this.temp = {
        id: 0,
        name: ''
      }
    },
    getRoleList() {
      this.loading = true
      getRoleList(
        this.listQuery
      ).then(response => {
        this.list = response.data.data.list
        this.loading = false
      }).catch(error => {
        this.loading = false
        Promise.reject(error)
      })
    },
    createData() {
      var checkedKeys = this.$refs.tree.getCheckedKeys()
      addRole({
        id: this.userdata.company.id,
        name: this.temp.name,
        p: checkedKeys
      }).then(() => {
        this.$message({ type: 'success', message: '新增成功!' })
        this.getRoleList()
        this.dialogVisible = false
      })
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row)
      this.temp.id = row.id
      this.temp.name = row.name
      this.$nextTick(() => {
        this.$refs.tree.setCheckedKeys(row.p)
      })
      this.dialogStatus = 'update'
      this.dialogVisible = true
    },
    updateData() {
      var checkedKeys = this.$refs.tree.getCheckedKeys()
      setRole({
        id: this.temp.id,
        name: this.temp.name,
        permissions: checkedKeys
      }).then(() => {
        this.$message({ type: 'success', message: '修改成功!' })
        this.getRoleList()
        this.dialogVisible = false
      })
    },
    handleRoleChange(data, obj) {
      var checkedKeys = this.$refs.tree.getCheckedKeys()
      console.log(checkedKeys)
      console.log(data)
      console.log(obj)
      // 判断是否存在子节点，子节点全选或反选
      if (data.children) {
        var check = false
        if (obj.checkedKeys.includes(data.id)) {
          check = true
        }
      }

      // 选中子节点，就选中父节点
      var pid = parseInt(data.id / 100) * 100
      if (!obj.checkedKeys.includes(pid)) {
        checkedKeys.push(pid)
      }
      this.$refs.tree.setCheckedKeys(checkedKeys)
    },
    handleDelete({ $index, row }) {
      this.$confirm('确定要删除吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        delRole({
          id: row.id
        }).then(() => {
          this.$message({ type: 'success', message: '删除成功!' })
          this.getRoleList()
        })
      })
    }
  }
}
</script>
