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
          <el-form-item label="开始日期:" prop="startDate" label-width="80px">
            <el-date-picker v-model="start_date" type="date" value-format="yyyy-MM-dd" class="filter-item" style="width: 150px;" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-button type="primary" size="mini" style="float:right;width:60px" @click="handleFlush()">刷新</el-button>
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

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.num" @pagination="getDeductionSummaryList" />
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Pagination from '@/components/Pagination'
import { DeductionType } from '@/utils/const'
import { getDeductionSummaryList, flushDeductionSummary } from '@/api/middle/deductionSummary'
import { getShopList } from '@/api/system/shop'

export default {
  components: { Pagination },
  data() {
    return {
      userdata: {},
      tableHeight: 600,
      list: null,
      total: 0,
      loading: false,
      shopList: [], // 本公司所有店铺列表
      start_date: 0,
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
      if (this.$refs.table) {
        this.tableHeight = window.innerHeight - this.$refs.table.$el.offsetTop - 78
      }
    }, 1000)
  },
  created() {
    this.userdata = this.$store.getters.userdata
    this.listQuery.id = this.$store.getters.shop
    this.start_date = new Date().toLocaleDateString().replace(/\//g, '-')
    this.getShopList()
  },
  methods: {
    getDeductionSummaryList() {
      this.loading = true
      getDeductionSummaryList(
        this.listQuery
      ).then(response => {
        this.total = response.data.data.total
        this.list = response.data.data.list
        // 处理扣款明细
        this.list.forEach(v => {
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
        this.getDeductionSummaryList()
      })
    },
    handleChange() {
      this.$store.commit('header/SET_HEADER_SHOP', this.listQuery.id)
      this.getDeductionSummaryList()
    },
    handleFlush() {
      flushDeductionSummary({
        id: this.listQuery.id,
        sdate: this.start_date
      }).then(() => {
        this.$message({ type: 'success', message: '刷新成功!' })
        this.getDeductionSummaryList()
      })
    }
  }
}
</script>
