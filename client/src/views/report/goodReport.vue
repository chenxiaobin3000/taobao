<template>
  <div class="app-container">
    <el-form :model="listQuery" label-position="left" label-width="50px" style="width: 100%; padding: 0 1% 0 1%;">
      <el-row>
        <el-col :span="5">
          <el-form-item label="店铺:" prop="shopName">
            <el-select v-model="listQuery.id" class="filter-item" placeholder="请选择店铺" @change="handleChange">
              <el-option v-for="item in shopList" :key="item.id" :label="item.name" :value="item.id" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="5">
          <el-form-item label="关注:" prop="followName">
            <el-select v-model="listQuery.follow" class="filter-item" placeholder="请选择" @change="handleSelect">
              <el-option v-for="item in followList" :key="'F' + item.id" :label="item.name" :value="item.id" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="5">
          <el-form-item label="开始日期:" prop="startDate" label-width="80px">
            <el-date-picker v-model="listQuery.sdate" type="date" value-format="yyyy-MM-dd" class="filter-item" style="width: 150px;" />
          </el-form-item>
        </el-col>
        <el-col :span="5">
          <el-form-item label="结束日期:" prop="endDate" label-width="80px">
            <el-date-picker v-model="listQuery.edate" type="date" value-format="yyyy-MM-dd" class="filter-item" style="width: 150px;" />
          </el-form-item>
        </el-col>
        <el-col :span="4">
          <el-button type="primary" size="mini" style="float:right;width:60px" @click="handleSelect()">查询</el-button>
        </el-col>
      </el-row>
    </el-form>
    <el-row>
      <el-col :span="19">
        <el-table ref="table_good" v-loading="loading" :data="listReport" :height="tableHeight" style="width: 100%" border fit highlight-current-row>
          <el-table-column align="center" label="商品编号" width="120">
            <template slot-scope="scope">
              {{ scope.row.good_id }}
            </template>
          </el-table-column>
          <el-table-column align="center" label="名称" width="90">
            <template slot-scope="scope">
              {{ scope.row.name }}
            </template>
          </el-table-column>
          <el-table-column align="center" label="花费" width="80">
            <template slot-scope="scope">
              {{ scope.row.cost }}
            </template>
          </el-table-column>
          <el-table-column align="center" label="成交金额" width="80">
            <template slot-scope="scope">
              {{ scope.row.deal_amount }}
            </template>
          </el-table-column>
          <el-table-column align="center" label="笔数" width="50">
            <template slot-scope="scope">
              {{ scope.row.deal_num }}
            </template>
          </el-table-column>
          <el-table-column align="center" label="总金额" width="80">
            <template slot-scope="scope">
              {{ scope.row.all }}
            </template>
          </el-table-column>
          <el-table-column align="center" label="实际金额" width="80">
            <template slot-scope="scope">
              {{ scope.row.payment }}
            </template>
          </el-table-column>
          <el-table-column align="center" label="退款" width="80">
            <template slot-scope="scope">
              {{ scope.row.refund }}
            </template>
          </el-table-column>
          <el-table-column align="center" label="采购" width="80">
            <template slot-scope="scope">
              {{ scope.row.procure }}
            </template>
          </el-table-column>
          <el-table-column align="center" label="扣款" width="80">
            <template slot-scope="scope">
              {{ scope.row.deduction }}
            </template>
          </el-table-column>
          <el-table-column align="center" label="备注">
            <template slot-scope="scope">
              {{ scope.row.transfer_note }}
            </template>
          </el-table-column>
        </el-table>
      </el-col>
      <el-col :span="5">
        <el-table ref="table_follow" v-loading="loading" :data="listGood" :height="tableHeight" style="width: 100%" border fit highlight-current-row>
          <el-table-column align="center" label="商品编号" width="120">
            <template slot-scope="scope">
              {{ scope.row.good_id }}
            </template>
          </el-table-column>
          <el-table-column align="center" label="名称" width="90">
            <template slot-scope="scope">
              {{ scope.row.short_name }}
            </template>
          </el-table-column>
          <el-table-column align="center" label="优先级">
            <template slot-scope="scope">
              <a v-if="scope.row.show" @click="handleEdit(scope.row.good_id)">{{ scope.row.priority }}</a>
              <el-input v-else v-model="temp.priority" @keyup.enter.native="handleSetPriority" />
            </template>
          </el-table-column>
        </el-table>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import { GoodFollowStatus } from '@/utils/const'
import { getGoodReport } from '@/api/report/goodReport'
import { getGoodFollowList, addGoodFollow, setGoodFollow, delGoodFollow } from '@/api/report/goodFollow'
import { getOwnShopList } from '@/api/system/shop'
import { getGoodList } from '@/api/system/good'

export default {
  data() {
    return {
      userdata: {},
      tableHeight: 600,
      listReport: null,
      listGood: null,
      listFollow: null,
      loading: false,
      shopList: [], // 本公司所有店铺列表
      followList: [], // 关注状态列表
      listQuery: {
        id: 0,
        follow: 1,
        sdate: 0,
        edate: 0
      },
      temp: {}
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
      if (this.$refs.table_follow) {
        this.tableHeight = window.innerHeight - this.$refs.table_good.$el.offsetTop - 78
      }
    }, 1000)
  },
  created() {
    this.userdata = this.$store.getters.userdata
    this.listQuery.id = this.$store.getters.shop
    this.followList = GoodFollowStatus.getList()
    this.listQuery.sdate = new Date()
    this.listQuery.edate = new Date().toLocaleDateString().replace(/\//g, '-')
    const seconds = this.listQuery.sdate.getTime() - 1000 * 60 * 60 * 24 * 31
    this.listQuery.sdate.setTime(seconds)
    this.listQuery.sdate = this.listQuery.sdate.toLocaleDateString().replace(/\//g, '-')
    this.resetTemp()
    this.getOwnShopList()
  },
  methods: {
    resetTemp() {
      this.temp = {
        priority: 0
      }
    },
    getGoodReport() {
      this.loading = true
      getGoodReport(
        this.listQuery
      ).then(response => {
        switch (this.listQuery.follow) {
          case GoodFollowStatus.ALL:
            this.listReport = response.data.data.list
            break

          case GoodFollowStatus.HAS_FOLLOW:
            this.listReport = []
            response.data.data.list.forEach(v => {
              for (let i = 0; i < this.listFollow.length; ++i) {
                if (v.good_id === this.listFollow[i].good_id) {
                  this.listReport.push(v)
                }
              }
            })
            break

          default:
            this.listReport = []
            response.data.data.list.forEach(v => {
              let find = false
              for (let i = 0; i < this.listFollow.length; ++i) {
                if (v.good_id === this.listFollow[i].good_id) {
                  find = true
                  break
                }
              }
              if (!find) {
                this.listReport.push(v)
              }
            })
        }
        this.loading = false
      }).catch(error => {
        this.loading = false
        Promise.reject(error)
      })
    },
    getGoodFollowList() {
      getGoodFollowList({
        id: this.listQuery.id,
        page: 1,
        num: 1000
      }).then(response => {
        this.listFollow = response.data.data.list
        if (this.listFollow) {
          this.listGood.forEach(v => {
            v.priority = 0
            v.show = true
            for (let i = 0; i < this.listFollow.length; ++i) {
              if (v.good_id === this.listFollow[i].good_id) {
                v.priority = this.listFollow[i].priority
                break
              }
            }
          })
        }
        this.getGoodReport()
      })
    },
    getGoodList() {
      getGoodList({
        id: this.listQuery.id,
        page: 1,
        num: 1000
      }).then(response => {
        this.listGood = response.data.data.list
        this.listGood.forEach(v => {
          v.priority = 0
          v.show = true
        })
        this.getGoodFollowList()
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
        this.getGoodList()
      })
    },
    handleChange() {
      this.$store.commit('header/SET_HEADER_SHOP', this.listQuery.id)
      this.getGoodReport()
    },
    handleSelect() {
      this.getGoodReport()
    },
    handleEdit(good_id) {
      this.listGood.forEach(v => {
        if (v.good_id === good_id) {
          v.show = false
          this.temp.id = 0
          this.temp.good_id = good_id
          this.temp.priority = v.priority
          for (let i = 0; i < this.listFollow.length; ++i) {
            if (v.good_id === this.listFollow[i].good_id) {
              this.temp.id = this.listFollow[i].id
            }
          }
        }
      })
    },
    handleSetPriority() {
      // 优先级必须在[0-10]之间
      const priority = parseInt(this.temp.priority)
      if (priority < 0 || priority > 10) {
        this.$message({ type: 'error', message: '优先级必须在[0-10]之间!' })
        return
      }
      if (this.temp.id === 0) {
        addGoodFollow({
          id: this.listQuery.id,
          good_id: this.temp.good_id,
          priority: priority
        }).then(() => {
          this.$message({ type: 'success', message: '修改成功!' })
          this.getGoodFollowList()
        })
      } else {
        this.listFollow.forEach(v => {
          if (v.good_id === this.temp.good_id) {
            if (priority === 0) {
              // 优先级小于0直接删除
              delGoodFollow({
                id: this.temp.id
              }).then(() => {
                this.$message({ type: 'success', message: '修改成功!' })
                this.getGoodFollowList()
              })
            } else {
              setGoodFollow({
                id: this.temp.id,
                priority: priority
              }).then(() => {
                this.$message({ type: 'success', message: '修改成功!' })
                this.getGoodFollowList()
              })
            }
          }
        })
      }
      this.temp.id = 0
      this.temp.good_id = 0
    }
  }
}
</script>
