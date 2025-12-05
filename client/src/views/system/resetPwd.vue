<template>
  <div class="app-container">
    <el-table v-loading="loading" :data="list" style="width: 100%" border fit highlight-current-row>
      <el-table-column label="用户名称" width="200px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.name }}</span>
        </template>
      </el-table-column>
      <el-table-column label="手机号" align="center">
        <template slot-scope="{row}">
          <span>{{ row.phone }}</span>
        </template>
      </el-table-column>
      <el-table-column label="部门" width="200px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.depart.name }}</span>
        </template>
      </el-table-column>
      <el-table-column label="角色" width="200px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.role.name }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" width="180" class-name="small-padding fixed-width">
        <template slot-scope="{row}">
          <el-button type="primary" size="mini" @click="handleResetPwd(row)">重置密码</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getUserList" />
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Pagination from '@/components/Pagination'
import { getUserList } from '@/api/user'
import { resetPwd } from '@/api/account'

export default {
  components: { Pagination },
  data() {
    return {
      list: null,
      total: 0,
      loading: false,
      listQuery: {
        id: 0,
        page: 1,
        limit: 10,
        search: null
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
      this.$message({ type: 'error', message: '该页面不支持新增用户，请到用户列表页面操作!' })
    }
  },
  created() {
    this.listQuery.id = this.$store.getters.userdata.user.id
    this.getUserList()
  },
  methods: {
    getUserList() {
      this.loading = true
      getUserList(
        this.listQuery
      ).then(response => {
        this.total = response.data.data.total
        this.list = response.data.data.list
        this.list.forEach(v => {
          if (v.depart == null) {
            v.depart = {
              name: ''
            }
          }
          if (v.role == null) {
            v.role = {
              id: 0,
              name: ''
            }
          }
        })
        this.loading = false
      }).catch(error => {
        this.loading = false
        Promise.reject(error)
      })
    },
    handleResetPwd(row) {
      this.$confirm('确定要重置密码吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        resetPwd({
          id: this.listQuery.id,
          uid: row.id
        }).then(() => {
          this.$message({ type: 'success', message: '重置成功!' })
        })
      })
    }
  }
}
</script>
