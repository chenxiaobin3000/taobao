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

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.num" @pagination="getPromotionDetailList" />

    <el-dialog title="导入Excel" :visible.sync="dialogVisible">
      <upload-excel-component :on-success="handleSuccess" width="90%" line-height="300px" height="300px" />
    </el-dialog>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Pagination from '@/components/Pagination'
import UploadExcelComponent from '@/components/UploadExcel'
import { ImportCount, ImportSpan } from '@/utils/const'
import { sleep } from '@/utils/sleep'
import { xlsx_date_str } from '@/utils/xlsx'
import { getPromotionDetailList, addPromotionDetailList, delPromotionDetail } from '@/api/trunk/promotionDetail'
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
      this.getPromotionDetailList()
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
    getPromotionDetailList() {
      this.loading = true
      getPromotionDetailList(
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
        this.getPromotionDetailList()
      })
    },
    handleChange() {
      this.getPromotionDetailList()
    },
    handleExcel() {
      this.dialogVisible = true
    },
    async handleSuccess({ results, header }) {
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
          pd: xlsx_date_str(v[promotion_date]),
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
      let length = p.length
      if (length > ImportCount) {
        length = parseInt(length / ImportCount)
        for (let i = 0; i <= length; ++i) {
          addPromotionDetailList({
            id: this.listQuery.id,
            p: p.slice(i * ImportCount, (i + 1) * ImportCount)
          }).then(() => {
            if (i === length) {
              this.$message({ type: 'success', message: '导入成功!' })
              this.getPromotionDetailList()
              this.dialogVisible = false
            } else {
              this.$message({ type: 'success', message: '正在导入!' })
            }
          })
          await sleep(ImportSpan)
        }
      } else {
        addPromotionDetailList({
          id: this.listQuery.id,
          p: p
        }).then(() => {
          this.$message({ type: 'success', message: '导入成功!' })
          this.getPromotionDetailList()
          this.dialogVisible = false
        })
      }
    },
    handleDelete(row) {
      this.$confirm('确定要删除吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        delPromotionDetail({
          id: row.id
        }).then(() => {
          this.$message({ type: 'success', message: '删除成功!' })
          this.getPromotionDetailList()
        })
      })
    }
  }
}
</script>
