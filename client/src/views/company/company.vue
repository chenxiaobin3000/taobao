<template>
  <div class="app-container">
    <el-form>
      <el-form-item label="公司名">
        <el-input v-model="temp.name" style="width: 260px; margin-left: 40px;" />
      </el-form-item>
      <el-form-item label="负责人" prop="owner">
        <el-select v-model="temp.id" class="filter-item" placeholder="请选择负责人" style="width: 260px; margin-left: 40px;">
          <el-option v-for="item in userList" :key="item.id" :label="item.name" :value="item.id" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" style="margin-left:20px;" @click="submit">更新</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import { getUserList } from '@/api/user'
import { setCompany } from '@/api/company'

export default {
  data() {
    return {
      userdata: {},
      userList: null, // 本公司所有用户列表
      temp: {}
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
      this.$message({ type: 'error', message: '该页面不支持搜索操作!' })
    },
    create() {
      this.$message({ type: 'error', message: '该页面不支持新增操作!' })
    }
  },
  created() {
    this.userdata = this.$store.getters.userdata
    this.resetTemp()
    this.getUserList()
  },
  methods: {
    resetTemp() {
      this.temp = {
        id: this.userdata.company.user_id,
        name: this.userdata.company.name
      }
    },
    getUserList() {
      getUserList({
        id: this.userdata.company.id,
        page: 1,
        num: 1000
      }).then(response => {
        this.userList = response.data.data.list
      })
    },
    submit() {
      setCompany({
        id: this.userdata.company.id,
        name: this.temp.name,
        uid: this.temp.id
      }).then(() => {
        this.$message({ type: 'success', message: '修改成功!' })
      })
    }
  }
}
</script>
