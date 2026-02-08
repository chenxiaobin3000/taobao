<template>
  <div class="app-container">
    <el-table ref="table" v-loading="loading" :data="list" :height="tableHeight" style="width: 100%" border fit highlight-current-row>
      <el-table-column label="用户名称" width="160px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.name }}</span>
        </template>
      </el-table-column>
      <el-table-column label="账号名称" width="160px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.account }}</span>
        </template>
      </el-table-column>
      <el-table-column label="手机号" width="160px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.phone }}</span>
        </template>
      </el-table-column>
      <el-table-column label="角色" width="80px" align="center">
        <template slot-scope="{row}">
          <span>{{ num2role(row.role_id) }}</span>
        </template>
      </el-table-column>
      <el-table-column label="店铺" align="center">
        <template slot-scope="{row}">
          <span>{{ row.shopList }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" fixed="right" width="160" class-name="small-padding fixed-width">
        <template slot-scope="{row}">
          <el-button type="primary" size="mini" @click="handleUpdate(row)">编辑</el-button>
          <el-button type="danger" size="mini" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.num" @pagination="getUserList" />

    <!-- 用户信息编辑 -->
    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogVisible">
      <el-form :model="temp" label-position="left" label-width="70px" style="width: 100%; padding: 0 4% 0 4%;">
        <el-form-item v-if="dialogStatus==='create'" label="账号">
          <el-input v-model="temp.account" />
        </el-form-item>
        <el-form-item label="用户名">
          <el-input v-model="temp.name" />
        </el-form-item>
        <el-form-item label="手机号">
          <el-input v-model="temp.phone" />
        </el-form-item>
        <el-form-item label="角色">
          <el-select v-model="temp.role_id" class="filter-item" placeholder="请选择角色">
            <el-option v-for="item in roleList" :key="item.id" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item v-if="dialogStatus!=='create'" label="店铺">
          <el-tree ref="tree" :data="routes" node-key="id" show-checkbox @check="handleShopChange" />
        </el-form-item>
        <el-form-item v-if="dialogStatus==='create'" label="说明">
          <div style="width: 240px">新用户注册后，默认密码为: 123456</div>
        </el-form-item>
        <el-form-item v-else label="说明">
          <div style="width: 220px">修改用户名只影响系统内部显示，登陆账号不会变化</div>
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
import { getUserList, addUser, setUser, delUser } from '@/api/system/user'
import { addUserShop, delUserShop } from '@/api/system/userShop'
import { getShopList } from '@/api/system/shop'
import { getRoleList } from '@/api/system/role'

export default {
  components: { Pagination },
  data() {
    return {
      userdata: {},
      routes: [],
      tableHeight: 600,
      list: null,
      total: 0,
      loading: false,
      roleList: null, // 本公司所有角色列表
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
      this.temp.id = this.userdata.user.id

      // 默认角色
      this.temp.role_id = this.roleList[0].id

      // 生成店铺列表
      this.routes = []
      for (let i = 0; i < this.shopList.length; ++i) {
        const tmp = this.shopList[i]
        this.routes.push({
          id: tmp.id,
          label: tmp.name
        })
      }

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
    this.resetTemp()
    this.getShopList()
  },
  methods: {
    resetTemp() {
      this.temp = {
        id: 0,
        account: '',
        name: '',
        phone: '',
        role_id: 0,
        shops: null
      }
    },
    getUserList() {
      this.loading = true
      getUserList(
        this.listQuery
      ).then(response => {
        this.total = response.data.data.total
        this.list = response.data.data.list
        // 展开店铺名称
        for (let i = 0; i < this.list.length; ++i) {
          const tmp = this.list[i]
          tmp.shopList = ''
          for (let j = 0; j < tmp.shops.length; ++j) {
            tmp.shopList = tmp.shopList + tmp.shops[j].name + ', '
          }
        }
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
        this.getRoleList()
      })
    },
    getRoleList() {
      getRoleList({
        id: this.userdata.company.id,
        page: 1,
        num: 1000
      }).then(response => {
        this.roleList = response.data.data.list
        this.getUserList()
      })
    },
    num2role(num) {
      for (let i = 0; i < this.roleList.length; ++i) {
        if (this.roleList[i].id === num) {
          return this.roleList[i].name
        }
      }
      return '异常'
    },
    createData() {
      addUser({
        account: this.temp.account,
        name: this.temp.name,
        phone: this.temp.phone,
        cid: this.userdata.company.id,
        rid: this.temp.role_id
      }).then(() => {
        this.$message({ type: 'success', message: '新增成功!' })
        this.getUserList()
        this.dialogVisible = false
      })
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row)

      // 生成店铺列表
      this.routes = []
      for (let i = 0; i < this.shopList.length; ++i) {
        const tmp = this.shopList[i]
        this.routes.push({
          id: tmp.id,
          label: tmp.name
        })
      }

      // 生成选中列表
      this.$nextTick(() => {
        const checkedKeys = []
        for (let i = 0; i < this.temp.shops.length; ++i) {
          checkedKeys.push(this.temp.shops[i].id)
        }
        this.$refs.tree.setCheckedKeys(checkedKeys)
      })
      this.dialogStatus = 'update'
      this.dialogVisible = true
    },
    updateData() {
      setUser({
        id: this.temp.id,
        name: this.temp.name,
        phone: this.temp.phone,
        rid: this.temp.role_id
      }).then(() => {
        this.$message({ type: 'success', message: '修改成功!' })
        this.getUserList()
        this.dialogVisible = false
      })
    },
    handleShopChange(data, obj) {
      if (obj.checkedKeys.includes(data.id)) {
        addUserShop({
          uid: this.temp.id,
          sid: data.id
        }).then(() => {
          this.getUserList()
        })
      } else {
        delUserShop({
          uid: this.temp.id,
          sid: data.id
        }).then(() => {
          this.getUserList()
        })
      }
    },
    handleDelete(row) {
      this.$confirm('确定要删除吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        delUser({
          id: row.id
        }).then(() => {
          this.$message({ type: 'success', message: '删除成功!' })
          this.getUserList()
        })
      })
    }
  }
}
</script>
