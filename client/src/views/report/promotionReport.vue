<template>
  <div class="app-container">
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
          <el-form-item label="关注:" prop="followName">
            <el-select v-model="listQuery.follow" class="filter-item" placeholder="请选择" @change="handleSelect">
              <el-option v-for="item in followFilterList" :key="'F' + item.id" :label="item.name" :value="item.id" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item label="日期:" prop="date">
            <el-date-picker v-model="listQuery.date" type="date" value-format="yyyy-MM-dd" class="filter-item" style="width: 150px;" @change="handleSelect" />
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>
    <el-table ref="table" v-loading="loading" :data="list" :height="tableHeight" style="width: 100%" border fit highlight-current-row>
      <el-table-column align="center" label="商品编号" width="110" fixed>
        <template slot-scope="scope">
          {{ scope.row.good_id }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="名称" width="90" fixed>
        <template slot-scope="scope">
          {{ scope.row.name }}
        </template>
      </el-table-column>
      <el-table-column v-for="metric in metricList" :key="metric.key" align="center" :label="metric.name">
        <el-table-column v-for="period in periodList" :key="metric.key + period.key" align="center" :label="period.name" :width="metric.width">
          <template slot-scope="scope">
            <div v-if="metric.key === 'profit'" :style="{ color: scope.row[period.key][metric.key] < 0 ? 'red' : 'green' }">{{ scope.row[period.key][metric.key] }}</div>
            <span v-else>{{ getMetricValue(scope.row, period.key, metric.key) }}</span>
          </template>
        </el-table-column>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import { GoodFollowStatus } from '@/utils/const'
import { getPromotionReport } from '@/api/report/promotionReport'
import { getOwnShopList } from '@/api/system/shop'

export default {
  data() {
    return {
      userdata: {},
      tableHeight: 600,
      list: null,
      loading: false,
      shopList: [], // 本公司所有店铺列表
      followFilterList: [], // 关注状态列表
      periodList: [
        { key: 'yesterday', name: '前1天' },
        { key: 'before_yesterday', name: '前2天' },
        { key: 'three_days', name: '前3天' },
        { key: 'five_days', name: '前5天' },
        { key: 'seven_days', name: '前7天' },
        { key: 'fifteen_days', name: '前15天' },
        { key: 'thirty_days', name: '前30天' }
      ],
      metricList: [
        { key: 'profit', name: '利润', width: 80 },
        { key: 'cost', name: '花费', width: 80 },
        { key: 'payment', name: '实际', width: 80 },
        { key: 'payment_rate', name: '实际比', width: 60 },
        { key: 'deal_amount', name: '成交', width: 80 },
        { key: 'deal_rate', name: '成交比', width: 60 }
      ],
      listQuery: {
        id: 0,
        follow: 1,
        date: 0,
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
      this.getPromotionReport()
    }
  },
  mounted: function() {
    setTimeout(() => {
      if (this.$refs.table) {
        this.tableHeight = window.innerHeight - this.$refs.table.$el.offsetTop - 20
      }
    }, 1000)
  },
  created() {
    this.userdata = this.$store.getters.userdata
    this.listQuery.id = this.$store.getters.shop
    this.followFilterList = GoodFollowStatus.getList()
    this.listQuery.date = new Date().toLocaleDateString().replace(/\//g, '-')
    this.getOwnShopList()
  },
  methods: {
    getMetricValue(row, periodKey, metricKey) {
      const period = row[periodKey] || {}
      if (metricKey === 'payment_rate') {
        return this.formatRatio(period.payment, period.cost)
      }
      if (metricKey === 'deal_rate') {
        return this.formatRatio(period.deal_amount, period.cost)
      }
      return period[metricKey]
    },
    formatRatio(value, cost) {
      const costValue = Number(cost) || 0
      if (costValue === 0) {
        return '0.00'
      }
      return ((Number(value) || 0) / costValue).toFixed(2)
    },
    getPromotionReport() {
      this.loading = true
      getPromotionReport(
        this.listQuery
      ).then(response => {
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
        this.getPromotionReport()
      })
    },
    handleChange() {
      this.$store.commit('header/SET_HEADER_SHOP', this.listQuery.id)
      this.getPromotionReport()
    },
    handleSelect() {
      this.getPromotionReport()
    }
  }
}
</script>
