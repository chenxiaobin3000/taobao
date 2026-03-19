<template>
  <div class="app-container">
    <el-form :model="listQuery" label-position="left" label-width="50px" style="width: 100%; padding: 0 1% 0 1%;">
      <el-row>
        <el-col :span="6">
          <el-form-item label="店铺:" prop="shopName">
            <el-select v-model="listQuery.id" class="filter-item" placeholder="请选择店铺" @change="handleChangeShop">
              <el-option v-for="item in shopList" :key="'S' + item.id" :label="item.name" :value="item.id" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item label="来源:" prop="fromName">
            <el-select v-model="listQuery.uid" class="filter-item" placeholder="请选择店铺" @change="handleChangeUser">
              <el-option v-for="item in userList" :key="'U' + item.user_id" :label="item.name" :value="item.user_id" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-button type="primary" size="mini" style="float:right;width:60px" @click="handleMerge()">合并</el-button>
        </el-col>
      </el-row>
    </el-form>
    <el-table ref="table" v-loading="loading" :data="list" :height="tableHeight" style="width: 100%" border fit highlight-current-row>
      <el-table-column align="center" label="打款人" width="80">
        <template slot-scope="scope">
          {{ scope.row.user_name }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="收款人" width="160">
        <template slot-scope="scope">
          {{ scope.row.payee_name }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="订单编码" width="160">
        <template slot-scope="scope">
          {{ scope.row.order_id }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="打款金额" width="80">
        <template slot-scope="scope">
          {{ scope.row.amount }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="打款时间" width="160">
        <template slot-scope="scope">
          {{ scope.row.create_time }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="备注">
        <template slot-scope="scope">
          {{ scope.row.transfer_note }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="操作" width="80">
        <template slot-scope="{row}">
          <el-button type="danger" size="mini" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.num" @pagination="getTransferList" />
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Pagination from '@/components/Pagination'
import { getTransferList, mergeTransfer, delTransfer } from '@/api/trunk/transfer'
import { getUserTransferList } from '@/api/original/transfer'
import { getShopList } from '@/api/system/shop'
import { getUserListByShop } from '@/api/system/userShop'

export default {
  components: { Pagination },
  data() {
    return {
      userdata: {},
      tableHeight: 600,
      list: null,
      total: 0,
      loading: false,
      shopList: [], // 本公司所有店铺列表
      userList: [], // 本店铺所有负责人列表
      listQuery: {
        id: 0,
        uid: 0,
        page: 1,
        num: 10,
        search: null
      }
    }
  },
  computed: {
    ...mapState({
      search: state => state.header.search
    })
  },
  watch: {
    search(newVal, oldVal) {
      this.listQuery.search = newVal
      this.getTransferList()
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
    this.getShopList()
  },
  methods: {
    getTransferList() {
      this.loading = true
      getTransferList(
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
        if (this.listQuery.id === 0) {
          this.listQuery.id = this.shopList[0].id
        }
        this.getUserListByShop()
      })
    },
    getUserListByShop() {
      getUserListByShop(
        this.listQuery
      ).then(response => {
        this.userList = response.data.data
        this.userList.unshift({ user_id: 0, name: '☆ 主干 ☆' })
        this.getTransferList()
      })
    },
    getUserTransferList() {
      this.loading = true
      getUserTransferList(
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
    handleChangeShop() {
      this.$store.commit('header/SET_HEADER_SHOP', this.listQuery.id)
      this.listQuery.uid = 0
      this.getTransferList()
    },
    handleChangeUser() {
      if (this.listQuery.uid === 0) {
        this.getTransferList()
      } else {
        this.getUserTransferList()
      }
    },
    handleMerge() {
      this.$confirm('确定要合并数据吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        mergeTransfer({
          id: this.listQuery.id,
          uid: this.listQuery.uid
        }).then(() => {
          this.$message({ type: 'success', message: '合并成功!' })
          this.listQuery.uid = 0
          this.getTransferList()
        })
      })
    },
    handleDelete(row) {
      this.$confirm('确定要删除吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        delTransfer({
          id: row.id
        }).then(() => {
          this.$message({ type: 'success', message: '删除成功!' })
          this.getTransferList()
        })
      })
    }
  }
}
</script>
