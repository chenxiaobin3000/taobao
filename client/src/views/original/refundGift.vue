<template>
  <div class="app-container">
    <el-form :model="listQuery" label-position="left" label-width="50px" style="width: 100%; padding: 0 1% 0 1%;">
      <el-form-item label="店铺:" prop="shopName">
        <el-select v-model="listQuery.id" class="filter-item" placeholder="请选择店铺" @change="handleChange">
          <el-option v-for="item in shopList" :key="item.id" :label="item.name" :value="item.id" />
        </el-select>
        <el-button type="danger" size="mini" style="float:right;width:60px" @click="handleDeleteAll()">清空</el-button>
      </el-form-item>
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

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.num" @pagination="getUserRefundGiftList" />
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Pagination from '@/components/Pagination'
import { NoneTime, RefundStatus, RefundType } from '@/utils/const'
import { getUserRefundGiftList, delUserRefundGift, delAllUserRefundGift } from '@/api/original/refundGift'
import { getOwnShopList } from '@/api/system/shop'

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
      this.getUserRefundGiftList()
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
    this.listQuery.uid = this.userdata.user.id
    this.getOwnShopList()
  },
  methods: {
    getUserRefundGiftList() {
      this.loading = true
      getUserRefundGiftList(
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
    getOwnShopList() {
      getOwnShopList({
        id: this.userdata.company.id,
        uid: this.userdata.user.id
      }).then(response => {
        this.shopList = response.data.data
        if (this.listQuery.id === 0) {
          this.listQuery.id = this.shopList[0].id
        }
        this.getUserRefundGiftList()
      })
    },
    num2type(num) {
      return RefundType.num2text(num)
    },
    num2status(num) {
      return RefundStatus.num2text(num)
    },
    handleChange() {
      this.$store.commit('header/SET_HEADER_SHOP', this.listQuery.id)
      this.getUserRefundGiftList()
    },
    handleDelete(row) {
      this.$confirm('确定要删除吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        delUserRefundGift({
          id: row.id
        }).then(() => {
          this.$message({ type: 'success', message: '删除成功!' })
          this.getUserRefundGiftList()
        })
      })
    },
    handleDeleteAll() {
      this.$confirm('确定要清空数据吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        delAllUserRefundGift({
          id: this.listQuery.id,
          uid: this.userdata.user.id
        }).then(() => {
          this.$message({ type: 'success', message: '删除成功!' })
          this.getUserRefundGiftList()
        })
      })
    }
  }
}
</script>
