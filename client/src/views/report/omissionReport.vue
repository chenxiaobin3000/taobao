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
        <el-col :span="3">
          <div>本页面: {{ single ? single : 0 }} 元</div>
        </el-col>
        <el-col :span="15">
          <div>总计: {{ amount ? amount : 0 }} 元</div>
        </el-col>
      </el-row>
    </el-form>
    <el-table ref="table" v-loading="loading" :data="list" :height="tableHeight" style="width: 100%" border fit highlight-current-row>
      <el-table-column align="center" label="订单编号" width="160">
        <template slot-scope="scope">
          {{ scope.row.order_id }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="扣款金额" width="80">
        <template slot-scope="scope">
          {{ scope.row.amount }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="扣款明细">
        <template slot-scope="scope">
          {{ scope.row.deduction_detail }}
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.num" @pagination="getOmissionReport" />
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Pagination from '@/components/Pagination'
import { DeductionType } from '@/utils/const'
import { getOmissionReport } from '@/api/report/omissionReport'
import { getShopList } from '@/api/system/shop'

export default {
  components: { Pagination },
  data() {
    return {
      userdata: {},
      tableHeight: 600,
      list: null,
      total: 0,
      amount: 0,
      single: 0,
      loading: false,
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
      this.$message({ type: 'error', message: '不支持搜索!' })
    }
  },
  mounted: function() {
    setTimeout(() => {
      this.tableHeight = window.innerHeight - this.$refs.table.$el.offsetTop - 78
    }, 1000)
  },
  created() {
    this.userdata = this.$store.getters.userdata
    this.listQuery.id = this.$store.getters.shop
    this.getShopList()
  },
  methods: {
    getOmissionReport() {
      this.loading = true
      getOmissionReport(
        this.listQuery
      ).then(response => {
        this.total = response.data.data.total
        this.amount = response.data.data.amount
        this.single = 0
        this.list = response.data.data.list
        // 处理扣款明细
        this.list.forEach(v => {
          this.single += v.amount
          let datas = ''
          const details = v.deduction_detail.split('|')
          for (let i = 0; i < details.length; ++i) {
            const deductions = details[i].split('-')
            if (deductions.length !== 2) {
              this.$message({ type: 'error', message: '数据异常!' })
              break
            }
            datas = datas + DeductionType.num2text(parseInt(deductions[0])) + ':' + deductions[1] + ' | '
          }
          if (datas.length > 3) {
            v.deduction_detail = datas.substring(0, datas.length - 3)
          } else {
            v.deduction_detail = datas
          }
        })
        this.single = this.single.toFixed(2)
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
        if (this.listQuery.id === 0) {
          this.listQuery.id = this.shopList[0].id
        }
        this.getOmissionReport()
      })
    },
    handleChange() {
      this.$store.commit('header/SET_HEADER_SHOP', this.listQuery.id)
      this.getOmissionReport()
    }
  }
}
</script>
