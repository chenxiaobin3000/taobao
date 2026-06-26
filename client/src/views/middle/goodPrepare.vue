<template>
  <div class="app-container">
    <el-form :model="listQuery" label-position="left" label-width="50px" style="width: 100%; padding: 0 1% 0 1%;">
      <el-row>
        <el-col :span="4">
          <el-form-item label="店铺:">
            <el-select v-model="listQuery.id" class="filter-item" placeholder="请选择店铺" @change="handleChange">
              <el-option v-for="item in shopList" :key="item.id" :label="item.name" :value="item.id" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="17">
          <div class="excel-import-cell">
            <div v-if="uploading || uploadProgress > 0" class="excel-import-progress">
              <el-progress :percentage="uploadProgress" />
              <span>{{ uploadProgressText }}</span>
            </div>
            <upload-excel-component :on-success="handleSuccess" width="100%" line-height="32px" height="36px" />
          </div>
        </el-col>
        <el-col :span="3">
          <el-button type="primary" size="mini" style="float:right;width:60px" @click="handleExport()">导出</el-button>
          <el-button type="danger" size="mini" style="float:right;width:60px;margin-right:10px;" @click="handleFlush()">刷新</el-button>
        </el-col>
      </el-row>
    </el-form>
    <el-table ref="table" v-loading="loading" :data="list" :height="tableHeight" style="width: 100%" border fit highlight-current-row>
      <el-table-column align="center" label="缩略图" width="70">
        <template slot-scope="scope">
          <img v-if="showGoodImage(scope.row)" :src="getGoodImageUrl(scope.row)" class="good-thumb" @error="handleGoodImageError(scope.row)">
          <span v-else>-</span>
        </template>
      </el-table-column>
      <el-table-column align="center" label="商品名称" width="100">
        <template slot-scope="scope">
          {{ scope.row.name }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="外部编码" width="120">
        <template slot-scope="scope">
          <a :href="handleJumpOrigin(scope.row.origin, scope.row.origin_type)" target="_blank">{{ scope.row.origin }}</a>
        </template>
      </el-table-column>
      <el-table-column align="center" label="外部类型" width="70">
        <template slot-scope="scope">
          {{ num2OriginType(scope.row.origin_type) }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="进货编码" width="120">
        <template slot-scope="scope">
          <a :href="handleJumpStock(scope.row.stock, scope.row.stock_type)" target="_blank">{{ scope.row.stock }}</a>
        </template>
      </el-table-column>
      <el-table-column align="center" label="进货类型" width="70">
        <template slot-scope="scope">
          {{ num2StockType(scope.row.stock_type) }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="创建时间" width="160">
        <template slot-scope="scope">
          {{ scope.row.ctime }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="上品时间" width="90">
        <template slot-scope="scope">
          {{ scope.row.join_date }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="备注">
        <template slot-scope="scope">
          {{ scope.row.good_note }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="操作" width="80">
        <template slot-scope="{row}">
          <el-button type="danger" size="mini" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.num" @pagination="getGoodPrepareList" />

  </div>
</template>

<script>
import { mapState } from 'vuex'
import XLSX from 'xlsx'
import Pagination from '@/components/Pagination'
import UploadExcelComponent from '@/components/UploadExcel'
import { GoodOriginType, GoodStockType } from '@/utils/const'
import { getGoodPrepareList, addGoodPrepareList, delGoodPrepare, flushGoodPrepare } from '@/api/middle/goodPrepare'
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
      uploading: false,
      uploadProgress: 0,
      uploadProgressText: '',
      originList: [], // 商品类型列表
      stockList: [], // 商品类型列表
      shopList: [], // 本公司所有店铺列表
      listQuery: {
        id: 0,
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
      this.getGoodPrepareList()
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
    this.originList = GoodOriginType.getList()
    this.stockList = GoodStockType.getList()
    this.getOwnShopList()
  },
  methods: {
    getGoodPrepareList() {
      this.loading = true
      getGoodPrepareList(
        this.listQuery
      ).then(response => {
        this.total = response.data.data.total
        this.list = (response.data.data.list || []).map(item => Object.assign({
          image_error: false
        }, item))
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
        this.getGoodPrepareList()
      })
    },
    num2OriginType(num) {
      return GoodOriginType.num2text(num)
    },
    num2StockType(num) {
      return GoodStockType.num2text(num)
    },
    handleJumpOrigin(id, type) {
      return GoodOriginType.getUrl(id, type)
    },
    handleJumpStock(id, type) {
      return GoodStockType.getUrl(id, type)
    },
    getGoodImageUrl(row) {
      const basePath = (process.env.VUE_APP_GOOD_IMAGE_PATH || 'http://localhost:8000/static/good_images').replace(/\/$/, '')
      return basePath + '/' + this.listQuery.id + '/' + row.origin + '.jpg'
    },
    showGoodImage(row) {
      return row.origin && !row.image_error
    },
    handleGoodImageError(row) {
      this.$set(row, 'image_error', true)
    },
    handleChange() {
      this.$store.commit('header/SET_HEADER_SHOP', this.listQuery.id)
      this.getGoodPrepareList()
    },
    handleSuccess({ results, header }) {
      if (!this.listQuery.id) {
        this.$message({ type: 'error', message: '请先选择店铺!' })
        return
      }
      const name = header[0]
      const origin = header[1]
      const originType = header[2]
      const stock = header[3]
      const stockType = header[4]
      const note = header[5]
      const goods = []
      for (let i = 0; i < results.length; i++) {
        const row = results[i]
        if (!row[name] && !row[origin] && !row[stock]) {
          continue
        }
        const originTypeNum = GoodOriginType.text2num(row[originType])
        const stockTypeNum = GoodStockType.text2num(row[stockType])
        if (originTypeNum === GoodOriginType.OTHER) {
          this.$message({ type: 'error', message: `第${i + 2}行外部类型异常` })
          return
        }
        if (stockTypeNum === GoodStockType.OTHER) {
          this.$message({ type: 'error', message: `第${i + 2}行进货类型异常` })
          return
        }
        goods.push({
          name: row[name],
          origin: row[origin],
          origin_type: originTypeNum,
          stock: row[stock],
          stock_type: stockTypeNum,
          note: row[note] || ''
        })
      }
      if (goods.length === 0) {
        this.$message({ type: 'error', message: '没有可导入数据!' })
        return
      }
      this.uploadChunks(goods)
    },
    async uploadChunks(goods) {
      this.uploading = true
      this.uploadProgress = 0
      this.uploadProgressText = `上传中 0/${goods.length}`
      const chunkSize = 300
      try {
        for (let i = 0; i < goods.length; i += chunkSize) {
          const chunk = goods.slice(i, i + chunkSize)
          await addGoodPrepareList({
            id: this.listQuery.id,
            g: chunk
          })
          const count = Math.min(i + chunk.length, goods.length)
          this.uploadProgress = Math.floor((count / goods.length) * 100)
          this.uploadProgressText = `已导入 ${count}/${goods.length}`
        }
        this.uploadProgress = 100
        this.uploadProgressText = `已导入 ${goods.length}/${goods.length}`
        this.$message({ type: 'success', message: '导入成功!' })
        this.getGoodPrepareList()
      } catch (error) {
        Promise.reject(error)
      } finally {
        this.uploading = false
      }
    },
    handleExport() {
      if (!this.listQuery.id) {
        this.$message({ type: 'error', message: '请先选择店铺!' })
        return
      }
      const query = Object.assign({}, this.listQuery, {
        page: 1,
        num: this.total > 0 ? this.total : 1000
      })
      getGoodPrepareList(query).then(response => {
        const list = response.data.data.list || []
        if (list.length === 0) {
          this.$message({ type: 'warning', message: '没有可导出数据!' })
          return
        }
        const rows = list.map(item => ({
          商品名称: item.name,
          外部编码: item.origin,
          外部类型: this.num2OriginType(item.origin_type),
          进货编码: item.stock,
          进货类型: this.num2StockType(item.stock_type),
          备注: item.good_note
        }))
        const worksheet = XLSX.utils.json_to_sheet(rows)
        const workbook = XLSX.utils.book_new()
        XLSX.utils.book_append_sheet(workbook, worksheet, '上新')
        XLSX.writeFile(workbook, '新品.xlsx')
      })
    },
    handleFlush() {
      flushGoodPrepare({
        id: this.listQuery.id
      }).then(() => {
        this.$message({ type: 'success', message: '刷新成功!' })
        this.getGoodPrepareList()
      })
    },
    handleDelete(row) {
      this.$confirm('确定要删除吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        delGoodPrepare({
          id: row.id
        }).then(() => {
          this.$message({ type: 'success', message: '删除成功!' })
          this.getGoodPrepareList()
        })
      })
    }
  }
}
</script>
<style scoped>
.excel-import-cell {
  display: flex;
  align-items: center;
  gap: 12px;
  padding-right: 12px;
}

.excel-import-cell > div:last-child {
  flex: 1 1 auto;
  min-width: 0;
}

.excel-import-cell ::v-deep .drop {
  margin: 0;
  font-size: 13px;
  border-width: 1px;
}

.excel-import-cell ::v-deep .drop .el-button {
  margin-left: 10px;
}

.excel-import-progress {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1 1 auto;
  min-width: 220px;
  font-size: 13px;
  color: #606266;
}

.excel-import-progress ::v-deep .el-progress {
  flex: 1 1 auto;
}

.good-thumb {
  display: block;
  width: 40px;
  height: 40px;
  margin: 0 auto;
  object-fit: cover;
}
</style>
