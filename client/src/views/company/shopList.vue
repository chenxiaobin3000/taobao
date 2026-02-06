<template>
  <div class="app-container">
    <el-table ref="table" v-loading="loading" :data="list" :height="tableHeight" style="width: 100%" border fit highlight-current-row>
      <el-table-column align="center" label="店铺名称">
        <template slot-scope="scope">
          {{ scope.row.name }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="平台" width="80px">
        <template slot-scope="scope">
          {{ scope.row.market_name }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="保证金" width="80px">
        <template slot-scope="scope">
          {{ scope.row.deposit }}
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

    <!-- 店铺信息编辑 -->
    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogVisible">
      <el-form :model="temp" label-position="left" label-width="70px" style="width: 100%; padding: 0 4% 0 4%;">
        <el-form-item label="店铺名称">
          <el-input v-model="temp.name" />
        </el-form-item>
        <el-form-item label="保证金">
          <el-input v-model="temp.deposit" />
        </el-form-item>
        <el-form-item v-if="isNew" label="平台">
          <el-select v-model="temp.marketId" class="filter-item" placeholder="请选择平台">
            <el-option v-for="item in marketList" :key="item.id" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item v-else label="管理员">
          <el-tree ref="tree" :data="routes" node-key="id" show-checkbox @check="handleUserChange" />
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
import { getShopList, addShop, delShop, setShop } from '@/api/system/shop'
import { getUserList } from '@/api/system/user'
import { addUserShop, delUserShop } from '@/api/system/userShop'
import { getMarketList } from '@/api/system/market'

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
      userList: null, // 本公司所有用户列表
      listQuery: {
        id: 0,
        page: 1,
        num: 10,
        search: null
      },
      isNew: false,
      temp: {},
      dialogVisible: false,
      dialogStatus: '',
      textMap: {
        update: '修改店铺信息',
        create: '新增店铺'
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
      this.temp.marketId = this.marketList[0].id
      // 生成用户列表
      this.routes = []
      for (let i = 0; i < this.userList.length; ++i) {
        const tmp = this.userList[i]
        this.routes.push({
          id: tmp.id,
          label: tmp.name
        })
      }
      this.isNew = true
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
    this.getUserList()
  },
  methods: {
    resetTemp() {
      this.temp = {
        id: 0,
        marketId: 0,
        name: '',
        deposit: 0
      }
    },
    getShopList() {
      this.loading = true
      getShopList(
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
    getUserList() {
      getUserList({
        id: this.userdata.company.id,
        page: 1,
        num: 1000
      }).then(response => {
        this.userList = response.data.data.list
        this.getMarketList()
      })
    },
    getMarketList() {
      getMarketList({
        id: this.userdata.company.id,
        page: 1,
        num: 1000
      }).then(response => {
        this.marketList = response.data.data.list
        this.getShopList()
      })
    },
    createData() {
      addShop({
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

      // 生成用户列表
      this.routes = []
      for (let i = 0; i < this.userList.length; ++i) {
        const tmp = this.userList[i]
        this.routes.push({
          id: tmp.id,
          label: tmp.name
        })
      }

      // 生成选中列表
      this.$nextTick(() => {
        const checkedKeys = []
        for (let i = 0; i < row.users.length; ++i) {
          checkedKeys.push(row.users[i].user_id)
        }
        this.$refs.tree.setCheckedKeys(checkedKeys)
      })
      this.isNew = false
      this.dialogStatus = 'update'
      this.dialogVisible = true
    },
    updateData() {
      setShop({
        id: this.temp.id,
        name: this.temp.name,
        deposit: this.temp.deposit
      }).then(() => {
        this.$message({ type: 'success', message: '修改成功!' })
        this.getUserList()
        this.dialogVisible = false
      })
    },
    handleUserChange(data, obj) {
      if (obj.checkedKeys.includes(data.id)) {
        addUserShop({
          uid: data.id,
          sid: this.temp.id
        }).then(() => {
          this.getUserList()
        })
      } else {
        delUserShop({
          uid: data.id,
          sid: this.temp.id
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
        delShop({
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
