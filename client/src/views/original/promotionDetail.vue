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
      <el-form-item label="店铺:" prop="shopName">
        <el-select v-model="listQuery.id" class="filter-item" placeholder="请选择店铺" @change="handleChange">
          <el-option v-for="item in shopList" :key="item.id" :label="item.name" :value="item.id" />
        </el-select>
        <el-button type="danger" size="mini" style="float:right;width:60px;margin-right:10px;" @click="handleDeleteAll()">清空</el-button>
      </el-form-item>
    </el-form>
    <el-table ref="table" v-loading="loading" :data="list" :height="tableHeight" style="width: 100%" border fit highlight-current-row>
      <el-table-column align="center" label="推广日期" width="120">
        <template slot-scope="scope">
          {{ scope.row.promotion_date }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="商品名称">
        <template slot-scope="scope">
          {{ scope.row.good_name }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="花费" width="80">
        <template slot-scope="scope">
          {{ scope.row.cost }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="投产比" width="80">
        <template slot-scope="scope">
          {{ scope.row.roi }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="成交金额" width="80">
        <template slot-scope="scope">
          {{ scope.row.deal_amount }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="成交笔数" width="80">
        <template slot-scope="scope">
          {{ scope.row.deal_num }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="展现量" width="80">
        <template slot-scope="scope">
          {{ scope.row.show_num }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="点击量" width="80">
        <template slot-scope="scope">
          {{ scope.row.click_num }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="点击率" width="80">
        <template slot-scope="scope">
          {{ scope.row.click_rate }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="平均花费" width="80">
        <template slot-scope="scope">
          {{ scope.row.average_cost }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="千次花费" width="80">
        <template slot-scope="scope">
          {{ scope.row.thousand_cost }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="成交成本" width="80">
        <template slot-scope="scope">
          {{ scope.row.deal_cost }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="购物车" width="80">
        <template slot-scope="scope">
          {{ scope.row.shop_cart }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="收藏数" width="80">
        <template slot-scope="scope">
          {{ scope.row.favorites }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="操作" width="80">
        <template slot-scope="{row}">
          <el-button type="danger" size="mini" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.num" @pagination="getUserPromotionDetailList" />

  </div>
</template>

<script>
import { mapState } from 'vuex'
import Pagination from '@/components/Pagination'
import UploadExcelComponent from '@/components/UploadExcel'
import { getUserPromotionDetailList, addUserPromotionDetailList, delUserPromotionDetail, delAllUserPromotionDetail } from '@/api/original/promotionDetail'
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
      shopList: [], // 本公司所有店铺列表
      listQuery: {
        id: 0,
        uid: 0,
        page: 1,
        num: 10,
        search: null
      },
      dialogVisible: false
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
      this.getUserPromotionDetailList()
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
    getUserPromotionDetailList() {
      this.loading = true
      getUserPromotionDetailList(
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
        this.getUserPromotionDetailList()
      })
    },
    handleChange() {
      this.$store.commit('header/SET_HEADER_SHOP', this.listQuery.id)
      this.getUserPromotionDetailList()
    },

    async handleSuccess({ results, header }) {
      this.uploading = false
      this.uploadProgress = 0
      this.uploadProgressText = ''
      const promotion_date = header[0]
      const good_id = header[1]
      const show_num = header[4]
      const click_num = header[5]
      const click_rate = header[7]
      const cost = header[6]
      const average_cost = header[8]
      const thousand_cost = header[9]
      const deal_amount = header[18]
      const deal_num = header[19]
      const deal_cost = header[25]
      const shop_cart = header[26]
      const favorites = header[30]
      const roi = header[23]
      const p = []
      results.forEach(v => {
        p.push({
          pd: v[promotion_date],
          id: v[good_id],
          sn: v[show_num] ? v[show_num] : 0,
          cn: v[click_num] ? v[click_num] : 0,
          cr: v[click_rate] ? v[click_rate] : 0,
          co: v[cost] ? v[cost] : 0,
          ac: v[average_cost] ? v[average_cost] : 0,
          tc: v[thousand_cost] ? v[thousand_cost] : 0,
          da: v[deal_amount] ? v[deal_amount] : 0,
          dn: v[deal_num] ? v[deal_num] : 0,
          dc: v[deal_cost] ? v[deal_cost] : 0,
          sc: v[shop_cart] ? v[shop_cart] : 0,
          fa: v[favorites] ? v[favorites] : 0,
          roi: v[roi] ? v[roi] : 0
        })
      })
      await this.uploadExcelChunks(p)
      this.$message({ type: 'success', message: '导入成功!' })
      this.getUserPromotionDetailList()
    },
    async uploadExcelChunks(records) {
      const chunkSize = 1000
      const total = records.length
      this.uploading = true
      this.uploadProgress = 0
      this.uploadProgressText = `Uploading 0/${total}`
      try {
        for (let i = 0; i < total; i += chunkSize) {
          const chunk = records.slice(i, i + chunkSize)
          await addUserPromotionDetailList({
            id: this.listQuery.id,
            uid: this.userdata.user.id,
            p: chunk
          })
          const finished = Math.min(i + chunk.length, total)
          this.uploadProgress = Math.floor((finished / total) * 100)
          this.uploadProgressText = `Uploading ${finished}/${total}`
        }
        this.uploadProgress = 100
        this.uploadProgressText = `Imported ${total}/${total}`
      } finally {
        this.uploading = false
      }
    },
    handleDelete(row) {
      this.$confirm('确定要删除吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        delUserPromotionDetail({
          id: row.id
        }).then(() => {
          this.$message({ type: 'success', message: '删除成功!' })
          this.getUserPromotionDetailList()
        })
      })
    },
    handleDeleteAll() {
      this.$confirm('确定要清空数据吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        delAllUserPromotionDetail({
          id: this.listQuery.id,
          uid: this.userdata.user.id
        }).then(() => {
          this.$message({ type: 'success', message: '删除成功!' })
          this.getUserPromotionDetailList()
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

.excel-import-row > div:first-child {
  flex: 1 1 auto;
  min-width: 0;
}

.excel-import-row ::v-deep .drop {
  margin: 0;
  font-size: 13px;
  border-width: 1px;
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
