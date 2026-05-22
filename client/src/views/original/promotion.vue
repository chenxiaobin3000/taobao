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
      <el-table-column align="center" label="交易日期" width="160">
        <template slot-scope="scope">
          {{ scope.row.create_date }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="金额" width="80">
        <template slot-scope="scope">
          {{ scope.row.payment }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="类型" width="160">
        <template slot-scope="scope">
          {{ num2type(scope.row.promotion_type) }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="备注">
        <template slot-scope="scope">
          {{ scope.row.promotion_note }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="操作" width="80">
        <template slot-scope="{row}">
          <el-button type="danger" size="mini" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.num" @pagination="getUserPromotionList" />

  </div>
</template>

<script>
import { mapState } from 'vuex'
import Pagination from '@/components/Pagination'
import UploadExcelComponent from '@/components/UploadExcel'
import { PromotionType } from '@/utils/const'
import { excelDateToText } from '@/utils/excel'
import { getUserPromotionList, addUserPromotionList, delUserPromotion, delAllUserPromotion } from '@/api/original/promotion'
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
      this.getUserPromotionList()
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
    getUserPromotionList() {
      this.loading = true
      getUserPromotionList(
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
        this.getUserPromotionList()
      })
    },
    num2type(num) {
      return PromotionType.num2text(num)
    },
    handleChange() {
      this.$store.commit('header/SET_HEADER_SHOP', this.listQuery.id)
      this.getUserPromotionList()
    },

    async handleSuccess({ results, header }) {
      this.uploading = false
      this.uploadProgress = 0
      this.uploadProgressText = ''
      const output = header[2]
      const create_date = header[1]
      const payment = header[4]
      const promotion_note = header[6]
      const p = []
      results.forEach(v => {
        if (v[output] === '支出') {
          p.push({
            d: excelDateToText(v[create_date], 'yyyy-MM-dd'),
            p: v[payment],
            t: PromotionType.text2num(v[promotion_note]),
            n: v[promotion_note]
          })
        }
      })
      const length = p.length
      // 预校验数据
      for (let i = 0; i < length; ++i) {
        if (p[i].t === PromotionType.OTHER) {
          this.$message({ type: 'error', message: '数据异常!' })
          console.log(p[i])
          return
        }
      }
      await this.uploadExcelChunks(p)
      this.$message({ type: 'success', message: '导入成功!' })
      this.getUserPromotionList()
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
          await addUserPromotionList({
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
        delUserPromotion({
          id: row.id
        }).then(() => {
          this.$message({ type: 'success', message: '删除成功!' })
          this.getUserPromotionList()
        })
      })
    },
    handleDeleteAll() {
      this.$confirm('确定要清空数据吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        delAllUserPromotion({
          id: this.listQuery.id,
          uid: this.userdata.user.id
        }).then(() => {
          this.$message({ type: 'success', message: '删除成功!' })
          this.getUserPromotionList()
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
