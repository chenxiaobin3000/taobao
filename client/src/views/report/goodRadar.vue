<template>
  <div class="app-container">
    <el-form :model="listQuery" label-position="left" label-width="50px" style="width: 100%; padding: 0 1% 0 1%;">
      <el-row>
        <el-col :span="5">
          <el-form-item label="店铺:">
            <el-select v-model="listQuery.id" class="filter-item" placeholder="请选择店铺" @change="handleShopChange">
              <el-option v-for="item in shopList" :key="item.id" :label="item.name" :value="item.id" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="5">
          <el-form-item label="商品:">
            <el-select v-model="listQuery.good_id" class="filter-item" placeholder="请选择商品" filterable @change="handleSelect">
              <el-option v-for="item in goodList" :key="item.good_id" :label="item.short_name" :value="item.good_id">
                <div class="good-option">
                  <img v-if="showGoodOptionImage(item)" :src="getGoodImageUrl(item)" class="good-option-img" @error="handleGoodOptionImageError(item)">
                  <span class="good-option-img-placeholder" v-else />
                  <span>{{ item.short_name }}</span>
                </div>
              </el-option>
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="5">
          <el-form-item label="开始日期:" label-width="80px">
            <el-date-picker v-model="listQuery.sdate" type="date" value-format="yyyy-MM-dd" class="filter-item" style="width: 150px;" @change="handleSelect" />
          </el-form-item>
        </el-col>
        <el-col :span="5">
          <el-form-item label="结束日期:" label-width="80px">
            <el-date-picker v-model="listQuery.edate" type="date" value-format="yyyy-MM-dd" class="filter-item" style="width: 150px;" @change="handleSelect" />
          </el-form-item>
        </el-col>
      </el-row>
      <el-row class="summary-row">
        <el-col :span="3">
          <div :style="{ color: summary.profit < 0 ? 'red' : 'green' }">利润: {{ summary.profit }}</div>
        </el-col>
        <el-col :span="3">
          <div>实际金额: {{ summary.payment }}</div>
        </el-col>
        <el-col :span="3">
          <div>花费: {{ summary.cost }}</div>
        </el-col>
        <el-col :span="3">
          <div>实际比: {{ summary.roi2 }}</div>
        </el-col>
        <el-col :span="3">
          <div>推广成交: {{ summary.deal_amount }}</div>
        </el-col>
        <el-col :span="3">
          <div>笔数: {{ summary.deal_num }}</div>
        </el-col>
        <el-col :span="3">
          <div>名义比: {{ summary.roi1 }}</div>
        </el-col>
        <el-col :span="3">
          <div>总金额: {{ summary.all }}</div>
        </el-col>
      </el-row>
      <el-row class="summary-row">
        <el-col :span="3">
          <div>退款金额: {{ summary.close }}</div>
        </el-col>
        <el-col :span="3">
          <div>秒退金额: {{ summary.flash }}</div>
        </el-col>
        <el-col :span="3">
          <div>总退货率: {{ summary.return1 }}%</div>
        </el-col>
        <el-col :span="3">
          <div>净退货率: {{ summary.return2 }}%</div>
        </el-col>
        <el-col :span="3">
          <div>采购: {{ summary.procure }}</div>
        </el-col>
        <el-col :span="3">
          <div>利润比: {{ summary.profit_rate }}</div>
        </el-col>
        <el-col :span="3">
          <div>扣款: {{ summary.deduction }}</div>
        </el-col>
        <el-col :span="3">
          <div>购物车: {{ summary.shop_cart }} / 收藏: {{ summary.favorites }}</div>
        </el-col>
      </el-row>
    </el-form>
    <el-table ref="table" v-loading="loading" :data="listReport" :height="tableHeight" style="width: 100%" border fit highlight-current-row>
      <el-table-column align="center" label="日期" width="100" fixed>
        <template slot-scope="scope">
          {{ scope.row.create_date }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="利润" width="80">
        <template slot-scope="scope">
          <div :style="{ color: scope.row.profit < 0 ? 'red' : 'green' }">{{ scope.row.profit }}</div>
        </template>
      </el-table-column>
      <el-table-column align="center" label="实际金额" width="80">
        <template slot-scope="scope">
          <strong>{{ scope.row.payment }}</strong>
        </template>
      </el-table-column>
      <el-table-column align="center" label="花费" width="80">
        <template slot-scope="scope">
          <strong>{{ scope.row.cost }}</strong>
        </template>
      </el-table-column>
      <el-table-column align="center" label="实际比" width="60">
        <template slot-scope="scope">
          <strong>{{ scope.row.roi2 }}</strong>
        </template>
      </el-table-column>
      <el-table-column align="center" label="推广成交" width="80">
        <template slot-scope="scope">
          {{ scope.row.deal_amount }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="笔数" width="50">
        <template slot-scope="scope">
          {{ scope.row.deal_num }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="名义比" width="60">
        <template slot-scope="scope">
          {{ scope.row.roi1 }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="总金额" width="80">
        <template slot-scope="scope">
          {{ scope.row.all }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="退款金额" width="80">
        <template slot-scope="scope">
          {{ scope.row.close }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="秒退金额" width="80">
        <template slot-scope="scope">
          {{ scope.row.flash }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="总退货率" width="70">
        <template slot-scope="scope">
          {{ scope.row.return1 }}%
        </template>
      </el-table-column>
      <el-table-column align="center" label="净退货率" width="70">
        <template slot-scope="scope">
          {{ scope.row.return2 }}%
        </template>
      </el-table-column>
      <el-table-column align="center" label="采购" width="80">
        <template slot-scope="scope">
          <strong>{{ scope.row.procure }}</strong>
        </template>
      </el-table-column>
      <el-table-column align="center" label="利润比" width="70">
        <template slot-scope="scope">
          <strong>{{ scope.row.profit_rate }}</strong>
        </template>
      </el-table-column>
      <el-table-column align="center" label="扣款" width="80">
        <template slot-scope="scope">
          {{ scope.row.deduction }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="购物车" width="60">
        <template slot-scope="scope">
          {{ scope.row.shop_cart }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="收藏" width="60">
        <template slot-scope="scope">
          {{ scope.row.favorites }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="备注">
        <template slot-scope="scope">
          {{ scope.row.transfer_note }}
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import { getGoodRadar } from '@/api/report/goodRadar'
import { getOwnShopList } from '@/api/system/shop'

export default {
  data() {
    return {
      userdata: {},
      tableHeight: 600,
      listReport: null,
      loading: false,
      shopList: [],
      goodList: [],
      listQuery: {
        id: 0,
        good_id: '',
        sdate: 0,
        edate: 0
      }
    }
  },
  computed: {
    ...mapState({
      search: state => state.header.search
    }),
    summary() {
      const list = this.listReport || []
      return {
        profit: this.sum(list, 'profit'),
        payment: this.sum(list, 'payment'),
        cost: this.sum(list, 'cost'),
        roi2: this.average(list, 'roi2'),
        deal_amount: this.sum(list, 'deal_amount'),
        deal_num: this.sum(list, 'deal_num', 0),
        roi1: this.average(list, 'roi1'),
        all: this.sum(list, 'all'),
        close: this.sum(list, 'close'),
        flash: this.sum(list, 'flash'),
        return1: this.average(list, 'return1', 1),
        return2: this.average(list, 'return2', 1),
        procure: this.sum(list, 'procure'),
        profit_rate: `${this.average(list, 'profit_rate', 1)}%`,
        deduction: this.sum(list, 'deduction'),
        shop_cart: this.sum(list, 'shop_cart', 0),
        favorites: this.sum(list, 'favorites', 0)
      }
    }
  },
  watch: {
    search(newVal, oldVal) {
      this.$message({ type: 'error', message: '不支持搜索!' })
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
    this.listQuery.sdate = new Date()
    const endDate = new Date()
    endDate.setTime(endDate.getTime() - 1000 * 60 * 60 * 24)
    this.listQuery.edate = endDate.toLocaleDateString().replace(/\//g, '-')
    const seconds = this.listQuery.sdate.getTime() - 1000 * 60 * 60 * 24 * 30
    this.listQuery.sdate.setTime(seconds)
    this.listQuery.sdate = this.listQuery.sdate.toLocaleDateString().replace(/\//g, '-')
    this.getOwnShopList()
  },
  methods: {
    getGoodRadar() {
      this.loading = true
      getGoodRadar(
        this.listQuery
      ).then(response => {
        this.goodList = (response.data.data.goods || []).map(item => Object.assign({
          option_image_error: false
        }, item))
        if (!this.listQuery.good_id && response.data.data.good_id) {
          this.listQuery.good_id = response.data.data.good_id
        }
        this.listReport = this.buildReportList(response.data.data.list)
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
        this.getGoodRadar()
      })
    },
    handleShopChange() {
      this.$store.commit('header/SET_HEADER_SHOP', this.listQuery.id)
      this.listQuery.good_id = ''
      this.getGoodRadar()
    },
    handleSelect() {
      this.getGoodRadar()
    },
    getGoodImageUrl(item) {
      const basePath = (process.env.VUE_APP_GOOD_IMAGE_PATH || 'http://localhost:8000/static/good_images').replace(/\/$/, '')
      return basePath + '/' + this.listQuery.id + '/' + item.good_id + '.jpg'
    },
    showGoodOptionImage(item) {
      return item.good_id && !item.option_image_error
    },
    handleGoodOptionImageError(item) {
      this.$set(item, 'option_image_error', true)
    },
    buildReportList(list) {
      if (!list) {
        return []
      }
      return list.map(item => {
        const payment = this.toNumber(item.payment)
        const close = this.toNumber(item.close)
        const flash = this.toNumber(item.flash)
        const refund = this.toNumber(item.refund)
        const cost = this.toNumber(item.cost)
        const deal_amount = this.toNumber(item.deal_amount)
        const procure = this.toNumber(item.procure)
        const deduction = this.toNumber(item.deduction)

        item.all = this.round(payment + close + flash)
        item.profit = this.round(payment - refund - cost - procure - deduction)
        item.roi1 = this.round(deal_amount / cost)
        item.roi2 = this.round((payment - refund) / cost)
        item.profit_rate = payment === 0 ? '0.0%' : this.round(((payment - procure) / payment) * 100, 1).toFixed(1) + '%'
        item.return1 = this.round(this.round((refund + close + flash) / (payment + close + flash), 3) * 100, 1)
        item.return2 = this.round(this.round((refund + close) / (payment + close), 3) * 100, 1)
        return item
      })
    },
    toNumber(value) {
      if (typeof value === 'string') {
        value = value.replace('%', '')
      }
      const number = Number(value)
      return Number.isFinite(number) ? number : 0
    },
    round(value, digits = 2) {
      const factor = Math.pow(10, digits)
      return Math.round(this.toNumber(value) * factor) / factor
    },
    sum(list, key, digits = 2) {
      return this.round(list.reduce((total, item) => total + this.toNumber(item[key]), 0), digits)
    },
    average(list, key, digits = 2) {
      if (!list.length) {
        return this.round(0, digits)
      }
      return this.round(list.reduce((total, item) => total + this.toNumber(item[key]), 0) / list.length, digits)
    }
  }
}
</script>
<style scoped>
.summary-row {
  font-size: small;
  line-height: 24px;
}

.good-option {
  display: flex;
  align-items: center;
  gap: 8px;
}

.good-option-img,
.good-option-img-placeholder {
  flex: 0 0 auto;
  width: 28px;
  height: 28px;
}

.good-option-img {
  object-fit: cover;
}

</style>
