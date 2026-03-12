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
      <el-table-column align="center" label="订单编码" width="160">
        <template slot-scope="scope">
          {{ scope.row.order_id }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="退款编码" width="160">
        <template slot-scope="scope">
          {{ scope.row.refund_id }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="商品编码" width="120">
        <template slot-scope="scope">
          {{ scope.row.product_id }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="实付" width="80">
        <template slot-scope="scope">
          {{ scope.row.actual_pay }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="退款" width="80">
        <template slot-scope="scope">
          {{ scope.row.refund_pay }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="退货类型" width="80">
        <template slot-scope="scope">
          {{ num2type(scope.row.refund_type) }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="退款状态">
        <template slot-scope="scope">
          {{ num2status(scope.row.refund_status) }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="申请时间" width="160">
        <template slot-scope="scope">
          {{ scope.row.apply_time }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="超时时间" width="160">
        <template slot-scope="scope">
          {{ scope.row.timeout_time === NoneTime ? '' : scope.row.timeout_time }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="完结时间" width="160">
        <template slot-scope="scope">
          {{ scope.row.complete_time === NoneTime ? '' : scope.row.complete_time }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="操作" width="80">
        <template slot-scope="{row}">
          <el-button type="danger" size="mini" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.num" @pagination="getRefundList" />
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Pagination from '@/components/Pagination'
import { NoneTime, RefundStatus, RefundType } from '@/utils/const'
import { getRefundList, mergeRefund, delRefund } from '@/api/trunk/refund'
import { getUserRefundList } from '@/api/original/refund'
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
      },
      NoneTime: NoneTime
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
      this.getRefundList()
    }
  },
  mounted: function() {
    setTimeout(() => {
      this.tableHeight = window.innerHeight - this.$refs.table.$el.offsetTop - 78
    }, 1000)
  },
  created() {
    this.userdata = this.$store.getters.userdata
    this.getShopList()
  },
  methods: {
    getRefundList() {
      this.loading = true
      getRefundList(
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
        this.listQuery.id = this.shopList[0].id
        this.getUserListByShop()
      })
    },
    getUserListByShop() {
      getUserListByShop(
        this.listQuery
      ).then(response => {
        this.userList = response.data.data
        this.userList.unshift({ user_id: 0, name: '☆ 主干 ☆' })
        this.getRefundList()
      })
    },
    getUserRefundList() {
      this.loading = true
      getUserRefundList(
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
      return RefundType.num2text(num)
    },
    num2status(num) {
      return RefundStatus.num2text(num)
    },
    handleChangeShop() {
      this.listQuery.uid = 0
      this.getRefundList()
    },
    handleChangeUser() {
      if (this.listQuery.uid === 0) {
        this.getRefundList()
      } else {
        this.getUserRefundList()
      }
    },
    handleMerge() {
      this.$confirm('确定要合并数据吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        mergeRefund({
          id: this.listQuery.id,
          uid: this.listQuery.uid
        }).then(() => {
          this.$message({ type: 'success', message: '合并成功!' })
          this.listQuery.uid = 0
          this.getRefundList()
        })
      })
    },
    handleDelete(row) {
      this.$confirm('确定要删除吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        delRefund({
          id: row.id
        }).then(() => {
          this.$message({ type: 'success', message: '删除成功!' })
          this.getRefundList()
        })
      })
    }
  }
}
</script>
