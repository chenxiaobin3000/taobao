<template>
  <div class="app-container">
    <el-form :model="listQuery" label-position="left" label-width="50px" style="width: 100%; padding: 0 1% 0 1%;">
      <el-row>
        <el-col :span="4">
          <el-form-item label="来源:">
            <el-select v-model="listQuery.uid" class="filter-item" placeholder="请选择来源" @change="handleChangeUser">
              <el-option v-for="item in userList" :key="'U' + item.id" :label="item.name" :value="item.id" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="5">
          <el-form-item label="开始日期:" label-width="80px">
            <el-date-picker v-model="listQuery.sdate" type="date" value-format="yyyy-MM-dd" class="filter-item" style="width: 150px;" />
          </el-form-item>
        </el-col>
        <el-col :span="5">
          <el-form-item label="结束日期:" label-width="80px">
            <el-date-picker v-model="listQuery.edate" type="date" value-format="yyyy-MM-dd" class="filter-item" style="width: 150px;" />
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-button type="primary" size="mini" style="float:right;width:60px" @click="handleMerge()">合并</el-button>
          <el-button type="primary" size="mini" style="float:right;width:60px;margin-right:10px;" @click="handleSelect()">查询</el-button>
        </el-col>
      </el-row>
    </el-form>
    <el-table ref="table" v-loading="loading" :data="list" :height="tableHeight" style="width: 100%" border fit highlight-current-row>
      <el-table-column align="center" label="采购编号" width="160">
        <template slot-scope="scope">
          {{ scope.row.purchase_id }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="采购账号" width="120">
        <template slot-scope="scope">
          {{ scope.row.purchase_account }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="金额" width="60">
        <template slot-scope="scope">
          {{ scope.row.payment }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="运费" width="60">
        <template slot-scope="scope">
          {{ scope.row.freight }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="总计" width="60">
        <template slot-scope="scope">
          {{ scope.row.total }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="订单状态" width="80">
        <template slot-scope="scope">
          {{ num2type(scope.row.order_status) }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="时间" width="160">
        <template slot-scope="scope">
          {{ scope.row.create_time }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="商品名称">
        <template slot-scope="scope">
          {{ scope.row.product_name }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="备注" width="60">
        <template slot-scope="scope">
          {{ scope.row.purchase_note }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="操作" width="80">
        <template slot-scope="{row}">
          <el-button type="danger" size="mini" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.num" @pagination="handlePage" />
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Pagination from '@/components/Pagination'
import { PurchaseStatus } from '@/utils/const'
import { getPurchaseList, mergePurchase, delPurchase } from '@/api/trunk/purchase'
import { getUserPurchaseList } from '@/api/original/purchase'
import { getUserList } from '@/api/system/user'

export default {
  components: { Pagination },
  data() {
    return {
      userdata: {},
      tableHeight: 600,
      list: null,
      total: 0,
      loading: false,
      userList: [],
      listQuery: {
        uid: 0,
        page: 1,
        num: 10,
        search: null,
        sdate: 0,
        edate: 0
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
      this.listQuery.page = 1
      this.handleSelect()
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
    this.listQuery.sdate = new Date()
    this.listQuery.edate = new Date().toLocaleDateString().replace(/\//g, '-')
    const seconds = this.listQuery.sdate.getTime() - 1000 * 60 * 60 * 24 * 180
    this.listQuery.sdate.setTime(seconds)
    this.listQuery.sdate = this.listQuery.sdate.toLocaleDateString().replace(/\//g, '-')
    this.getUserList()
  },
  methods: {
    getPurchaseList() {
      this.loading = true
      getPurchaseList(
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
        this.userList = response.data.data.list || []
        const currentUser = this.userList.find(v => v.id === this.userdata.user.id)
        this.listQuery.uid = currentUser ? currentUser.id : 0
        this.userList.unshift({ id: 0, name: '☆ 主干 ☆' })
        this.handlePage()
      })
    },
    getUserPurchaseList() {
      this.loading = true
      getUserPurchaseList(
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
    num2type(num) {
      return PurchaseStatus.num2text(num)
    },
    handleChangeUser() {
      this.listQuery.page = 1
      this.handleSelect()
    },
    handleSelect() {
      this.listQuery.page = 1
      this.handlePage()
    },
    handlePage() {
      if (this.listQuery.uid === 0) {
        this.getPurchaseList()
      } else {
        this.getUserPurchaseList()
      }
    },
    handleMerge() {
      if (this.listQuery.uid === 0) {
        this.$message({ type: 'error', message: '不能合并主干!' })
        return
      }
      this.$confirm('确定要合并数据吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        mergePurchase({
          uid: this.listQuery.uid
        }).then(() => {
          this.$message({ type: 'success', message: '合并成功!' })
          this.listQuery.uid = 0
          this.getPurchaseList()
        })
      })
    },
    handleDelete(row) {
      this.$confirm('确定要删除吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        delPurchase({
          id: row.id
        }).then(() => {
          this.$message({ type: 'success', message: '删除成功!' })
          this.getPurchaseList()
        })
      })
    }
  }
}
</script>
