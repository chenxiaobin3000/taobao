<template>
  <div class="app-container">
    <div class="excel-import-row">
      <upload-excel-component :on-success="handleSuccess" width="100%" line-height="32px" height="36px" />
      <div v-if="uploading || uploadProgress > 0" class="excel-import-progress">
        <el-progress :percentage="uploadProgress" />
        <span>{{ uploadProgressText }}</span>
      </div>
    </div>
    <el-form :model="listQuery" label-position="left" label-width="50px" style="width: 100%; padding: 0 1% 0 1%;">
      <el-row>
        <el-col :span="6">
          <el-form-item label="店铺:" prop="shopName">
            <el-select v-model="listQuery.id" class="filter-item" placeholder="请选择店铺" @change="handleChange">
              <el-option v-for="item in shopList" :key="item.id" :label="item.name" :value="item.id" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item label="开始日期:" prop="startDate" label-width="80px">
            <el-date-picker v-model="listQuery.sdate" type="date" value-format="yyyy-MM-dd" class="filter-item" style="width: 150px;" />
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item label="结束日期:" prop="endDate" label-width="80px">
            <el-date-picker v-model="listQuery.edate" type="date" value-format="yyyy-MM-dd" class="filter-item" style="width: 150px;" />
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-button type="danger" size="mini" style="float:right;width:60px;margin-right:10px;" @click="handleDeleteAll()">清空</el-button>
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
      <el-table-column align="center" label="订单编号" width="160">
        <template slot-scope="scope">
          {{ scope.row.order_id }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="付款金额" width="80">
        <template slot-scope="scope">
          {{ scope.row.payment }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="运费" width="80">
        <template slot-scope="scope">
          {{ scope.row.freight }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="付款总计" width="80">
        <template slot-scope="scope">
          {{ scope.row.total }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="订单状态" width="180">
        <template slot-scope="scope">
          {{ num2status(scope.row.order_status) }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="时间" width="160">
        <template slot-scope="scope">
          {{ scope.row.create_time }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="商品名称" width="180">
        <template slot-scope="scope">
          {{ scope.row.product_name }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="备注">
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

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.num" @pagination="getUserPurchaseList" />
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Pagination from '@/components/Pagination'
import UploadExcelComponent from '@/components/UploadExcel'
import { OrderStatus } from '@/utils/const'
import { getUserPurchaseList, addUserPurchaseList, delUserPurchase, delAllUserPurchase } from '@/api/original/purchase'
import { getOwnShopList } from '@/api/system/shop'

export default {
  components: { Pagination, UploadExcelComponent },
  data() {
    return {
      userdata: {},
      tableHeight: 600,
      list: null,
      total: 0,
      loading: false,
      shopList: [],
      listQuery: {
        id: 0,
        uid: 0,
        page: 1,
        num: 10,
        search: null,
        sdate: 0,
        edate: 0
      },
      uploading: false,
      uploadProgress: 0,
      uploadProgressText: ''
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
      this.getUserPurchaseList()
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
    this.listQuery.sdate = new Date()
    this.listQuery.edate = new Date().toLocaleDateString().replace(/\//g, '-')
    const seconds = this.listQuery.sdate.getTime() - 1000 * 60 * 60 * 24 * 180
    this.listQuery.sdate.setTime(seconds)
    this.listQuery.sdate = this.listQuery.sdate.toLocaleDateString().replace(/\//g, '-')
    this.getOwnShopList()
  },
  methods: {
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
    getOwnShopList() {
      getOwnShopList({
        id: this.userdata.company.id,
        uid: this.userdata.user.id
      }).then(response => {
        this.shopList = response.data.data
        if (this.listQuery.id === 0) {
          this.listQuery.id = this.shopList[0].id
        }
        this.getUserPurchaseList()
      })
    },
    num2status(num) {
      return OrderStatus.num2text(num)
    },
    handleChange() {
      this.$store.commit('header/SET_HEADER_SHOP', this.listQuery.id)
      this.listQuery.page = 1
      this.getUserPurchaseList()
    },
    handleSelect() {
      this.listQuery.page = 1
      this.getUserPurchaseList()
    },
    async handleSuccess({ results, header }) {
      this.uploading = false
      this.uploadProgress = 0
      this.uploadProgressText = ''
      const purchase_id = header[0]
      const order_id = header[1]
      const payment = header[2]
      const freight = header[3]
      const total = header[4]
      const order_status = header[5]
      const create_time = header[6]
      const product_name = header[7]
      const purchase_note = header[8]
      const purchases = []
      const errors = []
      results.forEach((v, index) => {
        const status = OrderStatus.text2num(v[order_status])
        if (status === OrderStatus.OTHER) {
          errors.push(`行号: ${index + 2}\r\n原因: 订单状态异常\r\n采购编号: ${v[purchase_id]}\r\n订单编号: ${v[order_id]}`)
        }
        purchases.push({
          pid: v[purchase_id],
          oid: v[order_id],
          payment: v[payment],
          freight: v[freight],
          total: v[total],
          status: status,
          ctime: v[create_time],
          pn: v[product_name],
          note: v[purchase_note] || ''
        })
      })
      if (errors.length > 0) {
        this.downloadImportErrors(errors)
        this.$message({ type: 'error', message: '数据异常，请查看下载的异常信息文件!' })
        return
      }
      await this.uploadPurchaseChunks(purchases)
      this.$message({ type: 'success', message: '导入成功!' })
      this.getUserPurchaseList()
    },
    async uploadPurchaseChunks(purchases) {
      const chunkSize = 1000
      const total = purchases.length
      this.uploading = true
      this.uploadProgress = 0
      this.uploadProgressText = `正在导入 0/${total}`
      try {
        for (let i = 0; i < total; i += chunkSize) {
          const chunk = purchases.slice(i, i + chunkSize)
          await addUserPurchaseList({
            id: this.listQuery.id,
            uid: this.userdata.user.id,
            p: chunk
          })
          const finished = Math.min(i + chunk.length, total)
          this.uploadProgress = Math.floor((finished / total) * 100)
          this.uploadProgressText = `正在导入 ${finished}/${total}`
        }
        this.uploadProgress = 100
        this.uploadProgressText = `导入完成 ${total}/${total}`
      } finally {
        this.uploading = false
      }
    },
    downloadImportErrors(errors) {
      const content = errors.join('\r\n\r\n')
      const blob = new Blob([content], { type: 'text/plain;charset=utf-8' })
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = 'purchase_import_errors.txt'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
    },
    handleDelete(row) {
      this.$confirm('确定要删除吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        delUserPurchase({
          id: row.id
        }).then(() => {
          this.$message({ type: 'success', message: '删除成功!' })
          this.getUserPurchaseList()
        })
      })
    },
    handleDeleteAll() {
      this.$confirm('确定要清空数据吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        delAllUserPurchase({
          id: this.listQuery.id,
          uid: this.userdata.user.id
        }).then(() => {
          this.$message({ type: 'success', message: '删除成功!' })
          this.getUserPurchaseList()
        })
      })
    }
  }
}
</script>

<style scoped>
.excel-import-row {
  position: sticky;
  top: 0;
  z-index: 9;
  display: flex;
  align-items: center;
  gap: 16px;
  min-height: 48px;
  padding: 6px 1%;
  margin-bottom: 8px;
  background: #fff;
  border-bottom: 1px solid #d8dce5;
}

.excel-import-row ::v-deep .drop {
  margin: 0;
  font-size: 13px;
  border-width: 1px;
}

.excel-import-row > div:first-child {
  flex: 1 1 auto;
  min-width: 0;
}

.excel-import-row ::v-deep .drop .el-button {
  margin-left: 10px;
}

.excel-import-progress {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1 1 auto;
  min-width: 240px;
  font-size: 13px;
  color: #606266;
}

.excel-import-progress ::v-deep .el-progress {
  flex: 1 1 auto;
}
</style>
