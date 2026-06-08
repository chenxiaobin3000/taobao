<template>
  <div class="app-container">
    <el-form :model="listQuery" label-position="left" label-width="50px" style="width: 100%; padding: 0 1% 0 1%;">
      <el-row>
        <el-col :span="6">
          <el-form-item label="店铺:">
            <el-select v-model="listQuery.id" class="filter-item" placeholder="请选择店铺" @change="handleChange">
              <el-option v-for="item in shopList" :key="item.id" :label="item.name" :value="item.id" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item label="开始日期:" label-width="80px">
            <el-date-picker v-model="start_date" type="date" value-format="yyyy-MM-dd" class="filter-item" style="width: 150px;" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-button type="primary" size="mini" style="float:right;width:60px" :loading="flushing" :disabled="flushing" @click="handleFlush()">刷新</el-button>
        </el-col>
      </el-row>
    </el-form>
    <div v-if="flushing || flushProgress > 0" class="flush-progress">
      <el-progress :percentage="flushProgress" />
      <span>{{ flushProgressText }}</span>
    </div>
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
import { getOwnShopList } from '@/api/system/shop'

export default {
  components: { Pagination },
  data() {
    return {
      userdata: {},
      tableHeight: 600,
      list: null,
      total: 0,
      loading: false,
      flushing: false,
      flushProgress: 0,
      flushProgressText: '',
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
      this.listQuery.search = newVal
      this.listQuery.page = 1
      this.getDeductionSummaryList()
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
    this.start_date = new Date()
    const seconds = this.start_date.getTime() - 1000 * 60 * 60 * 24 * 180
    this.start_date.setTime(seconds)
    this.start_date = this.start_date.toLocaleDateString().replace(/\//g, '-')
    this.getOwnShopList()
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
        if (this.list) {
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
        }
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
        this.getDeductionSummaryList()
      })
    },
    handleChange() {
      this.$store.commit('header/SET_HEADER_SHOP', this.listQuery.id)
      this.listQuery.page = 1
      this.getDeductionSummaryList()
    },
    async handleFlush() {
      const start = this.parseDate(this.start_date)
      const end = this.addDays(this.today(), 1)
      if (!start || start >= end) {
        this.$message({ type: 'error', message: '开始日期要早于当前时间' })
        return
      }
      const chunkDays = 15
      const totalDays = Math.max(1, Math.ceil((end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24)))
      let finishedDays = 0
      let cursor = start
      this.flushing = true
      this.flushProgress = 0
      this.flushProgressText = `刷新中: 0/${totalDays}天`
      try {
        while (cursor < end) {
          const next = this.addDays(cursor, chunkDays)
          const batchEnd = next < end ? next : end
          await flushDeductionSummary({
            id: this.listQuery.id,
            full_sdate: this.formatDate(start),
            sdate: this.formatDate(cursor),
            edate: this.formatDate(batchEnd)
          })
          finishedDays = Math.min(totalDays, Math.ceil((batchEnd.getTime() - start.getTime()) / (1000 * 60 * 60 * 24)))
          this.flushProgress = Math.floor((finishedDays / totalDays) * 100)
          this.flushProgressText = `刷新中: ${finishedDays}/${totalDays}天`
          cursor = batchEnd
        }
        this.flushProgress = 100
        this.flushProgressText = `刷新完成: ${totalDays}/${totalDays}天`
        this.$message({ type: 'success', message: '刷新成功!' })
        this.getDeductionSummaryList()
      } finally {
        this.flushing = false
      }
    },
    parseDate(value) {
      if (value instanceof Date) {
        return value
      }
      if (!value) {
        return null
      }
      return new Date(value.replace(/-/g, '/'))
    },
    addDays(date, days) {
      const result = new Date(date.getTime())
      result.setDate(result.getDate() + days)
      return result
    },
    today() {
      const now = new Date()
      return new Date(now.getFullYear(), now.getMonth(), now.getDate())
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
.flush-progress {
  display: flex;
  align-items: center;
  gap: 10px;
  min-height: 32px;
  padding: 0 1% 8px;
  font-size: 13px;
  color: #606266;
}

.flush-progress ::v-deep .el-progress {
  flex: 1 1 auto;
}
</style>
