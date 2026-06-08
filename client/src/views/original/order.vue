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
      <el-table-column align="center" label="采购金额" width="80">
        <template slot-scope="scope">
          {{ scope.row.procure }}
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
      <el-table-column align="center" label="商品" width="160">
        <template slot-scope="scope">
          {{ scope.row.good_names }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="备注">
        <template slot-scope="scope">
          {{ scope.row.order_note }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="操作" width="80">
        <template slot-scope="{row}">
          <el-button type="danger" size="mini" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.num" @pagination="getUserOrderList" />

  </div>
</template>

<script>
import { mapState } from 'vuex'
import Pagination from '@/components/Pagination'
import UploadExcelComponent from '@/components/UploadExcel'
import { OrderStatus } from '@/utils/const'
import { extractOrderProcure } from '@/utils/deduction'
import { getUserOrderList, addUserOrderList, delUserOrder, delAllUserOrder } from '@/api/original/order'
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
      shopList: [], // 本公司所有店铺列表
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
      this.getUserOrderList()
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
    getUserOrderList() {
      this.loading = true
      getUserOrderList(
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
        this.getUserOrderList()
      })
    },
    num2status(num) {
      return OrderStatus.num2text(num)
    },
    handleChange() {
      this.$store.commit('header/SET_HEADER_SHOP', this.listQuery.id)
      this.listQuery.page = 1
      this.getUserOrderList()
    },
    handleSelect() {
      this.listQuery.page = 1
      this.getUserOrderList()
    },
    async handleSuccess({ results, header }) {
      this.uploading = false
      this.uploadProgress = 0
      this.uploadProgressText = ''
      const order_id = header[0]
      const payment = header[6]
      const order_status = header[2]
      const create_time = header[3]
      const product_name = header[4]
      const order_note = header[5]
      const o = []
      results.forEach(v => {
        o.push({
          id: v[order_id],
          pa: v[payment],
          pr: 0,
          st: OrderStatus.text2num(v[order_status]),
          ct: v[create_time],
          na: v[product_name],
          pi: '',
          no: v[order_note]
        })
      })
      // 提取采购价
      const length = o.length
      const errors = []
      for (let i = 0; i < length; ++i) {
        // 异常状态
        if (o[i].st === OrderStatus.OTHER) {
          errors.push(this.formatImportError(i, '订单状态异常', o[i]))
          continue
        }
        const ext = extractOrderProcure(o[i].no, o[i].id, message => console.log(message))
        if (ext[0]) {
          o[i].pr = ext[1]
          o[i].pi = ext[2]
        } else {
          // 忽略未付款或订单关闭
          if (o[i].st === OrderStatus.CLOSE || o[i].st === OrderStatus.UNPAID || o[i].st === OrderStatus.PAID || o[i].st === OrderStatus.UNCREATED) {
            continue
          }
          // 金额小于6认定为刷单，忽略备注
          if (parseFloat(o[i].pa) > 6) {
            errors.push(this.formatImportError(i, '订单备注解析异常', o[i]))
          }
        }
      }
      if (errors.length > 0) {
        this.downloadImportErrors(errors)
        this.$message({ type: 'error', message: '数据异常，请查看下载的异常信息文件!' })
        return
      }
      await this.uploadOrderChunks(o)
      this.$message({ type: 'success', message: '导入成功!' })
      this.getUserOrderList()
    },
    async uploadOrderChunks(orders) {
      const chunkSize = 1000
      const total = orders.length
      this.uploading = true
      this.uploadProgress = 0
      this.uploadProgressText = `正在导入 0/${total}`
      try {
        for (let i = 0; i < total; i += chunkSize) {
          const chunk = orders.slice(i, i + chunkSize)
          await addUserOrderList({
            id: this.listQuery.id,
            uid: this.userdata.user.id,
            o: chunk
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
    formatImportError(index, reason, order) {
      return [
        `行号: ${index + 2}`,
        `原因: ${reason}`,
        `订单编号: ${order.id}`,
        `订单状态: ${order.st}`,
        `付款金额: ${order.pa}`,
        `创建时间: ${order.ct}`,
        `商品名称: ${order.na}`,
        `备注: ${order.no}`
      ].join('\r\n')
    },
    downloadImportErrors(errors) {
      const content = errors.join('\r\n\r\n')
      const blob = new Blob([content], { type: 'text/plain;charset=utf-8' })
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = 'order_import_errors.txt'
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
        delUserOrder({
          id: row.id
        }).then(() => {
          this.$message({ type: 'success', message: '删除成功!' })
          this.getUserOrderList()
        })
      })
    },
    handleDeleteAll() {
      this.$confirm('确定要清空数据吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        delAllUserOrder({
          id: this.listQuery.id,
          uid: this.userdata.user.id
        }).then(() => {
          this.$message({ type: 'success', message: '删除成功!' })
          this.getUserOrderList()
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
