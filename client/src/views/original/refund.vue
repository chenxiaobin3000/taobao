<template>
  <div class="app-container">
    <el-form :model="listQuery" label-position="left" label-width="70px" style="width: 100%; padding: 0 1% 0 1%;">
      <el-form-item label="店铺:" prop="shopName">
        <el-select v-model="listQuery.id" class="filter-item" placeholder="请选择店铺" @change="handleChange">
          <el-option v-for="item in shopList" :key="item.id" :label="item.name" :value="item.id" />
        </el-select>
        <el-button type="primary" size="mini" style="float:right;width:60px" @click="handleExcel()">导入</el-button>
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
      <el-table-column align="center" label="商品编码" width="160">
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
          {{ scope.row.refund_type }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="退款状态" width="80">
        <template slot-scope="scope">
          {{ scope.row.refund_status }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="申请时间" width="160">
        <template slot-scope="scope">
          {{ scope.row.apply_time }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="超时时间" width="160">
        <template slot-scope="scope">
          {{ scope.row.timeout_time }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="完结时间">
        <template slot-scope="scope">
          {{ scope.row.complete_time }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="操作" width="80">
        <template slot-scope="{row}">
          <el-button type="danger" size="mini" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getRefundList" />

    <el-dialog title="导入Excel" :visible.sync="dialogVisible">
      <upload-excel-component :on-success="handleSuccess" width="90%" line-height="300px" height="300px" />
    </el-dialog>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Pagination from '@/components/Pagination'
import UploadExcelComponent from '@/components/UploadExcel'
import { RefundStatus, RefundType } from '@/utils/const'
import { getRefundList, addRefundList, delRefund } from '@/api/original/refund'
import { getShopList } from '@/api/system/shop'

export default {
  components: { Pagination, UploadExcelComponent },
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
        page: 1,
        num: 10,
        search: null
      },
      dialogVisible: false
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
      this.getRefundList()
    },
    create() {
      this.$message({ type: 'error', message: '不支持新建!' })
    }
  },
  mounted: function() {
    setTimeout(() => {
      this.tableHeight = window.innerHeight - this.$refs.table.$el.offsetTop - 78
    }, 1000)
  },
  created() {
    this.userdata = this.$store.getters.userdata
    this.listQuery.id = 0
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
        this.getRefundList()
      })
    },
    handleChange() {
      this.getRefundList()
    },
    handleExcel() {
      this.dialogVisible = true
    },
    handleSuccess({ results, header }) {
      const refund_id = header[1]
      const order_id = header[0]
      const product_id = header[4]
      const actual_pay = header[7]
      const refund_pay = header[9]
      const refund_type = header[11]
      const refund_status = header[14]
      const apply_time = header[12]
      const timeout_time = header[13]
      const complete_time = header[6]
      const r = []
      results.forEach(v => {
        r.push({
          uid: v[refund_id],
          oid: v[order_id],
          pid: v[product_id],
          ap: v[actual_pay],
          rp: v[refund_pay],
          rt: v[refund_type],
          rs: v[refund_status],
          at: v[apply_time],
          tt: v[timeout_time],
          ct: v[complete_time]
        })
      })
      addRefundList({
        id: this.listQuery.id,
        r: r
      }).then(() => {
        this.$message({ type: 'success', message: '导入成功!' })
        this.getRefundList()
        this.dialogVisible = false
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
