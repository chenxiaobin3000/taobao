<template>
  <div class="app-container">
    <el-form :model="listQuery" label-position="left" label-width="50px" style="width: 100%; padding: 0 1% 0 1%;">
      <el-row>
        <el-col :span="6">
          <el-form-item label="店铺:" prop="shopName">
            <el-select v-model="listQuery.id" class="filter-item" placeholder="请选择店铺" @change="handleChangeShop">
              <el-option v-for="item in shopList" :key="'S' + item.id" :label="item.name" :value="item.id" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item label="来源:" prop="fromName">
            <el-select v-model="listQuery.uid" class="filter-item" placeholder="请选择店铺" @change="handleChangeUser">
              <el-option v-for="item in userList" :key="'U' + item.user_id" :label="item.name" :value="item.user_id" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-button type="primary" size="mini" style="float:right;width:60px" @click="handleMerge()">合并</el-button>
        </el-col>
      </el-row>
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
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Pagination from '@/components/Pagination'
import { getPromotionDetailList, mergePromotionDetail, delPromotionDetail } from '@/api/trunk/promotionDetail'
import { getUserPromotionDetailList } from '@/api/original/promotionDetail'
import { getShopList } from '@/api/system/shop'
import { getUserListByShop } from '@/api/system/userShop'

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
      userList: [], // 本店铺所有负责人列表
      listQuery: {
        id: 0,
        uid: 0,
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
      this.getPromotionDetailList()
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
        if (this.listQuery.id === 0) {
          this.listQuery.id = this.shopList[0].id
        }
        this.getUserListByShop()
      })
    },
    getUserListByShop() {
      getUserListByShop(
        this.listQuery
      ).then(response => {
        this.userList = response.data.data
        this.userList.unshift({ user_id: 0, name: '☆ 主干 ☆' })
        this.getPromotionDetailList()
      })
    },
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
    handleChangeShop() {
      this.$store.commit('header/SET_HEADER_SHOP', this.listQuery.id)
      this.listQuery.uid = 0
      this.getPromotionDetailList()
    },
    handleChangeUser() {
      if (this.listQuery.uid === 0) {
        this.getPromotionDetailList()
      } else {
        this.getUserPromotionDetailList()
      }
    },
    handleMerge() {
      this.$confirm('确定要合并数据吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        mergePromotionDetail({
          id: this.listQuery.id,
          uid: this.listQuery.uid
        }).then(() => {
          this.$message({ type: 'success', message: '合并成功!' })
          this.listQuery.uid = 0
          this.getPromotionDetailList()
        })
      })
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
