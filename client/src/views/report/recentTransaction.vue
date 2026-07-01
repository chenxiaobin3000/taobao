<template>
  <div class="app-container">
    <el-form :model="listQuery" label-position="left" label-width="50px" style="width: 100%; padding: 0 1%;">
      <el-row>
        <el-col :span="5">
          <el-form-item label="店铺:">
            <el-select v-model="listQuery.id" class="filter-item" placeholder="请选择店铺" @change="handleShopChange">
              <el-option v-for="item in shopList" :key="item.id" :label="item.name" :value="item.id" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="5">
          <el-form-item label="状态:">
            <el-select v-model="listQuery.status" class="filter-item" placeholder="请选择" @change="getList">
              <el-option v-for="item in statusFilterList" :key="item.id" :label="item.name" :value="item.id" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="5">
          <el-form-item label="开始日期:" label-width="80px">
            <el-date-picker v-model="listQuery.sdate" type="date" value-format="yyyy-MM-dd" class="filter-item" style="width: 150px;" />
          </el-form-item>
        </el-col>
        <el-col :span="5">
          <el-form-item label="结束日期:" label-width="80px">
            <el-date-picker v-model="listQuery.edate" type="date" value-format="yyyy-MM-dd" class="filter-item" style="width: 150px;" />
          </el-form-item>
        </el-col>
        <el-col :span="4">
          <el-button type="primary" size="mini" style="float:right;width:60px" @click="getList">查询</el-button>
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
        <template slot-scope="scope">{{ scope.row.short_name }}</template>
      </el-table-column>
      <el-table-column align="center" label="商品编码" width="120">
        <template slot-scope="scope">
          <a :href="getOriginUrl(scope.row)" target="_blank">{{ scope.row.good_id }}</a>
        </template>
      </el-table-column>
      <el-table-column align="center" label="优先级" width="70">
        <template slot-scope="scope">{{ scope.row.priority }}</template>
      </el-table-column>
      <el-table-column align="center" label="外部编码" width="120">
        <template slot-scope="scope">
          <a :href="getOriginUrl(scope.row)" target="_blank">{{ scope.row.origin }}</a>
        </template>
      </el-table-column>
      <el-table-column align="center" label="进货编码" width="120">
        <template slot-scope="scope">
          <a :href="getStockUrl(scope.row)" target="_blank">{{ scope.row.stock }}</a>
        </template>
      </el-table-column>
      <el-table-column align="center" label="商品类型" width="70">
        <template slot-scope="scope">{{ GoodType.num2text(scope.row.good_type) }}</template>
      </el-table-column>
      <el-table-column align="center" label="商品状态" width="70">
        <template slot-scope="scope">{{ GoodStatus.num2text(scope.row.good_status) }}</template>
      </el-table-column>
      <el-table-column align="center" label="首次刷单" width="90">
        <template slot-scope="scope">{{ scope.row.fake_date }}</template>
      </el-table-column>
      <el-table-column align="center" label="首次推广" width="90">
        <template slot-scope="scope">{{ scope.row.promotion_date }}</template>
      </el-table-column>
      <el-table-column align="center" label="完整名称">
        <template slot-scope="scope">{{ scope.row.name }}</template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import { GoodOriginType, GoodStatus, GoodStockType, GoodType } from '@/utils/const'
import { getRecentTransactionList } from '@/api/report/recentTransaction'
import { getOwnShopList } from '@/api/system/shop'

export default {
  data() {
    return {
      userdata: {},
      loading: false,
      tableHeight: 600,
      list: [],
      shopList: [],
      statusFilterList: [],
      GoodStatus,
      GoodType,
      listQuery: {
        id: 0,
        status: 0,
        sdate: '',
        edate: ''
      }
    }
  },
  computed: {
    ...mapState({
      search: state => state.header.search
    })
  },
  watch: {
    search() {
      this.$message({ type: 'error', message: '不支持搜索!' })
    }
  },
  created() {
    this.userdata = this.$store.getters.userdata
    this.listQuery.id = this.$store.getters.shop
    this.statusFilterList = [{ id: 0, name: '全部状态' }].concat(GoodStatus.getList())
    const endDate = new Date()
    const startDate = new Date()
    startDate.setDate(startDate.getDate() - 30)
    this.listQuery.sdate = this.formatDate(startDate)
    this.listQuery.edate = this.formatDate(endDate)
    this.getShopList()
  },
  mounted() {
    setTimeout(() => {
      if (this.$refs.table) {
        this.tableHeight = window.innerHeight - this.$refs.table.$el.offsetTop - 20
      }
    }, 1000)
  },
  methods: {
    getShopList() {
      getOwnShopList({
        id: this.userdata.company.id,
        uid: this.userdata.user.id
      }).then(response => {
        this.shopList = response.data.data || []
        if (this.listQuery.id === 0 && this.shopList.length) {
          this.listQuery.id = this.shopList[0].id
        }
        this.getList()
      })
    },
    getList() {
      if (!this.listQuery.id) {
        this.list = []
        return
      }
      this.loading = true
      getRecentTransactionList(this.listQuery).then(response => {
        this.list = (response.data.data.list || []).map(item => Object.assign({
          image_error: false
        }, item))
      }).finally(() => {
        this.loading = false
      })
    },
    handleShopChange() {
      this.$store.commit('header/SET_HEADER_SHOP', this.listQuery.id)
      this.getList()
    },
    getOriginUrl(row) {
      return GoodOriginType.getUrl(row.origin, row.origin_type)
    },
    getStockUrl(row) {
      return GoodStockType.getUrl(row.stock, row.stock_type)
    },
    getGoodImageUrl(row) {
      const basePath = (process.env.VUE_APP_GOOD_IMAGE_PATH || 'http://localhost:8000/static/good_images').replace(/\/$/, '')
      return basePath + '/' + GoodOriginType.getImagePath(row.origin, row.origin_type)
    },
    showGoodImage(row) {
      return GoodOriginType.getImagePath(row.origin, row.origin_type) && !row.image_error
    },
    handleGoodImageError(row) {
      this.$set(row, 'image_error', true)
    },
    formatDate(date) {
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      return `${year}-${month}-${day}`
    }
  }
}
</script>

<style scoped>
.good-thumb {
  display: block;
  width: 40px;
  height: 40px;
  margin: 0 auto;
  object-fit: cover;
}
</style>
