<template>
  <div class="app-container">
    <el-table ref="table" v-loading="loading" :data="list" :height="tableHeight" style="width: 100%" border fit highlight-current-row>
      <el-table-column label="用户名称" width="160px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.name }}</span>
        </template>
      </el-table-column>
      <el-table-column label="手机号" align="center">
        <template slot-scope="{row}">
          <span>{{ row.phone }}</span>
        </template>
      </el-table-column>
      <el-table-column label="部门" width="140px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.depart ? row.depart.name : '' }}</span>
        </template>
      </el-table-column>
      <el-table-column label="公司角色" width="160px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.role.name }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" fixed="right" width="160" class-name="small-padding fixed-width">
        <template slot-scope="{row}">
          <el-button type="primary" size="mini" @click="handleUpdate(row)">编辑</el-button>
          <el-button type="danger" size="mini" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getUserList" />

    <!-- 用户信息编辑 -->
    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogVisible">
      <el-form :model="temp" label-position="left" label-width="70px" style="width: 100%; padding: 0 4% 0 4%;">
        <el-form-item label="用户名" prop="name">
          <el-input v-model="temp.name" />
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="temp.phone" />
        </el-form-item>
        <el-form-item label="部门" prop="department">
          <el-select v-model="temp.depart.id" class="filter-item" placeholder="请选择部门">
            <el-option v-for="item in departmentList" :key="item.id" :label="item.label" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select v-model="temp.role.id" class="filter-item" placeholder="请选择角色">
            <el-option v-for="item in grouproles" :key="item.id" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item v-if="dialogStatus==='create'" label="说明" prop="role">
          <div style="width: 240px">新用户注册后，使用"用户名"做为账号进行登陆，默认密码为: 123456</div>
        </el-form-item>
        <el-form-item v-else label="说明" prop="role">
          <div style="width: 220px">修改用户名只影响系统内部显示，登陆账号不会变化</div>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="dialogStatus==='create'?createData():updateData()">确定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Pagination from '@/components/Pagination'
import { getUserList, addUser, setUser, delUser } from '@/api/user'
import { getGroupDepartmentTree, setUserDepartment } from '@/api/department'
import { getRoleList, setUserRole } from '@/api/role'

export default {
  components: { Pagination },
  data() {
    return {
      tableHeight: 600,
      grouproles: null, // 本公司所有角色列表
      list: null,
      total: 0,
      loading: false,
      departmentList: [],
      oldRole: '', // 保存修改界面的旧角色id
      listQuery: {
        id: 0,
        page: 1,
        limit: 10,
        search: null
      },
      temp: {},
      dialogVisible: false,
      dialogStatus: '',
      textMap: {
        update: '修改用户信息',
        create: '新增用户'
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
      this.getUserList()
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
    this.listQuery.id = this.userdata.user.id
    this.resetTemp()
    this.getDepartmentList()
  },
  methods: {
    resetTemp() {
      this.temp = {
        id: 0,
        name: '',
        phone: '',
        depart: { id: null, name: '' },
        role: { id: null, name: '' }
      }
    },
    getUserList() {
      this.loading = true
      getUserList(
        this.listQuery
      ).then(response => {
        this.total = response.data.data.total
        this.list = response.data.data.list
        this.list.forEach(v => {
          if (v.role == null) {
            v.role = { id: 0, name: '无' }
          }
        })
        this.loading = false
      }).catch(error => {
        this.loading = false
        Promise.reject(error)
      })
    },
    getDepartmentList() {
      getGroupDepartmentTree({
        id: this.userdata.user.id
      }).then(response => {
        this.generator(response.data.data.list)
        this.getRoleList()
      })
    },
    generator(tree) {
      tree.forEach(v => {
        this.departmentList.push(v)
        if (v.children != null) {
          this.generator(v.children)
        }
      })
    },
    getRoleList() {
      getRoleList({
        id: this.userdata.user.id
      }).then(response => {
        this.grouproles = response.data.data.roles
        this.getUserList()
      })
    },
    createData() {
      addUser({
        id: this.userdata.user.id,
        account: this.temp.name,
        phone: this.temp.phone,
        rid: this.temp.role.id
      }).then(response => {
        setUserDepartment({
          id: this.userdata.user.id,
          uid: response.data.data.id,
          did: this.temp.depart.id
        }).then(() => {})
        this.$message({ type: 'success', message: '新增成功!' })
        this.getUserList()
        this.dialogVisible = false
      })
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row)
      if (this.temp.depart == null) {
        this.temp.depart = { id: null, name: '' }
      }
      this.oldRole = this.temp.role.id
      this.dialogStatus = 'update'
      this.dialogVisible = true
    },
    updateData() {
      if (this.oldRole !== this.temp.role.id) {
        setUserRole({
          id: this.userdata.user.id,
          uid: this.temp.id,
          rid: this.temp.role.id
        }).then(() => {
          this.setUser()
        })
      } else {
        this.setUser()
      }
    },
    async setUser() {
      await this.setUserDepartment()
      setUser({
        id: this.userdata.user.id,
        uid: this.temp.id,
        name: this.temp.name,
        phone: this.temp.phone
      }).then(() => {
        this.$message({ type: 'success', message: '修改成功!' })
        this.getUserList()
        this.dialogVisible = false
      })
    },
    setUserDepartment() {
      setUserDepartment({
        id: this.userdata.user.id,
        uid: this.temp.id,
        did: this.temp.depart.id
      }).then(() => {})
    },
    handleDelete(row) {
      this.$confirm('确定要删除吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        delUser({
          id: this.userdata.user.id,
          uid: row.id
        }).then(() => {
          this.$message({ type: 'success', message: '删除成功!' })
          this.getUserList()
        })
      })
    }
  }
}
</script>
