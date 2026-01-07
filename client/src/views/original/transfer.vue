<template>
  <div class="app-container">
    <el-form :model="listQuery" label-position="left" label-width="70px" style="width: 100%; padding: 0 1% 0 1%;">
      <el-form-item label="店铺:" prop="shopName">
        <el-select v-model="listQuery.id" class="filter-item" placeholder="请选择店铺">
          <el-option v-for="item in shopList" :key="item.id" :label="item.name" :value="item.id" />
        </el-select>
        <el-button type="primary" size="mini" style="float:right;width:60px" @click="handleExcel()">导入</el-button>
      </el-form-item>
    </el-form>
    <el-table ref="table" v-loading="loading" :data="list" :height="tableHeight" style="width: 100%" border fit highlight-current-row>
      <el-table-column align="center" label="打款人" width="160">
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
      <el-table-column align="center" label="打款金额" width="160">
        <template slot-scope="scope">
          {{ scope.row.amount }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="打款时间" width="160">
        <template slot-scope="scope">
          {{ scope.row.create_time }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="打款时间">
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

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getTransferList" />

    <el-dialog title="导入Excel" :visible.sync="dialogVisible">
      <upload-excel-component :on-success="handleSuccess" width="90%" line-height="300px" height="300px" />
    </el-dialog>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Pagination from '@/components/Pagination'
import UploadExcelComponent from '@/components/UploadExcel'
import { getTransferList, addTransferList, delTransfer } from '@/api/original/transfer'
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
      this.getTransferList()
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
        this.listQuery.id = this.shopList[0].id
        this.getTransferList()
      })
    },
    handleExcel() {
      this.dialogVisible = true
    },
    handleSuccess({ results, header }) {
      const user_name = header[0]
      const payee_name = header[1]
      const order_id = header[7]
      const amount = header[4]
      const create_time = header[5]
      const transfer_note = header[9]
      const t = []
      results.forEach(v => {
        const date = new Date((v[create_time] - 2) * 24 * 3600000 + 1 - 8 * 3600000)
        const Y = (date.getFullYear() - 70) + '-'
        const M = (date.getMonth() + 1) + '-'
        const D = date.getDate() + ' '
        const h = date.getHours() + ':'
        const m = date.getMinutes() + ':'
        const s = date.getSeconds()
        t.push({
          n: v[user_name],
          p: v[payee_name],
          o: v[order_id],
          a: v[amount],
          c: Y + M + D + h + m + s,
          tn: v[transfer_note]
        })
      })
      addTransferList({
        id: this.listQuery.id,
        t: t
      }).then(() => {
        this.$message({ type: 'success', message: '导入成功!' })
        this.getTransferList()
        this.dialogVisible = false
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
