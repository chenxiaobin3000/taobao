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
            <el-date-picker v-model="listQuery.sdate" type="date" value-format="yyyy-MM-dd" class="filter-item" style="width: 150px;" />
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item label="结束日期:" prop="endDate" label-width="80px">
            <el-date-picker v-model="listQuery.edate" type="date" value-format="yyyy-MM-dd" class="filter-item" style="width: 150px;" />
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-button type="primary" size="mini" style="width:80px" @click="handleSelect()">查询</el-button>
        </el-col>
      </el-row>
    </el-form>
    <el-row>
      <el-col :span="20">
        <el-table ref="table_good" v-loading="loading" :data="list" :height="tableHeight" style="width: 100%" border fit highlight-current-row>
          <el-table-column align="center" label="打款人" width="80">
            <template slot-scope="scope">
              {{ scope.row.user_name }}
            </template>
          </el-table-column>
          <el-table-column align="center" label="收款人" width="160">
            <template slot-scope="scope">
              {{ scope.row.payee_name }}
            </template>
          </el-table-column>
          <el-table-column align="center" label="订单编码" width="160">
            <template slot-scope="scope">
              {{ scope.row.order_id }}
            </template>
          </el-table-column>
          <el-table-column align="center" label="打款金额" width="80">
            <template slot-scope="scope">
              {{ scope.row.amount }}
            </template>
          </el-table-column>
          <el-table-column align="center" label="打款时间" width="160">
            <template slot-scope="scope">
              {{ scope.row.create_time }}
            </template>
          </el-table-column>
          <el-table-column align="center" label="备注">
            <template slot-scope="scope">
              {{ scope.row.transfer_note }}
            </template>
          </el-table-column>
        </el-table>
      </el-col>
      <el-col :span="4">
        <!--
        <el-table ref="table_follow" v-loading="loading" :data="list" :height="tableHeight" style="width: 100%" border fit highlight-current-row>
          <el-table-column align="center" label="打款人" width="80">
            <template slot-scope="scope">
              {{ scope.row.user_name }}
            </template>
          </el-table-column>
        </el-table>-->
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import { getGoodReport } from '@/api/report/goodReport'
import { getOwnShopList } from '@/api/system/shop'

export default {
  data() {
    return {
      userdata: {},
      tableHeight: 600,
      list: null,
      loading: false,
      shopList: [], // 本公司所有店铺列表
      listQuery: {
        id: 0,
        sdate: 0,
        edate: 0
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
        this.tableHeight = window.innerHeight - this.$refs.table_follow.$el.offsetTop - 78
      }
    }, 1000)
  },
  created() {
    this.userdata = this.$store.getters.userdata
    this.listQuery.id = this.$store.getters.shop
    this.getOwnShopList()
  },
  methods: {
    getGoodReport() {
      this.loading = true
      getGoodReport(
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
        this.getGoodReport()
      })
    },
    handleChange() {
      this.$store.commit('header/SET_HEADER_SHOP', this.listQuery.id)
      this.getGoodReport()
    },
    handleSelect() {
      this.getGoodReport()
    }
  }
}
</script>
