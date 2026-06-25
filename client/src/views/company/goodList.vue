<template>
  <div class="app-container">
    <div class="excel-import-row">
      <upload-excel-component :on-success="handleSuccess" width="100%" line-height="32px" height="36px" />
    </div>
    <el-form :model="listQuery" label-position="left" label-width="50px" style="width: 100%; padding: 0 1% 0 1%;">
      <el-row>
        <el-col :span="5">
          <el-form-item label="店铺:">
            <el-select v-model="listQuery.id" class="filter-item" placeholder="请选择店铺" @change="handleChange">
              <el-option v-for="item in shopList" :key="item.id" :label="item.name" :value="item.id" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="5">
          <el-form-item label="类型:">
            <el-select v-model="listQuery.type" class="filter-item" placeholder="请选择类型" @change="handleFilterChange">
              <el-option v-for="item in typeFilterList" :key="item.id" :label="item.name" :value="item.id" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="5">
          <el-form-item label="状态:">
            <el-select v-model="listQuery.status" class="filter-item" placeholder="请选择状态" @change="handleFilterChange">
              <el-option v-for="item in statusFilterList" :key="item.id" :label="item.name" :value="item.id" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="5">
          <el-form-item label="关注:">
            <el-select v-model="listQuery.follow" class="filter-item" placeholder="请选择关注" @change="handleFilterChange">
              <el-option v-for="item in followFilterList" :key="item.id" :label="item.name" :value="item.id" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="4">
          <el-button type="danger" size="mini" style="float:right;width:60px;margin-right:10px;" @click="handleFlush()">刷新</el-button>
        </el-col>
      </el-row>
    </el-form>
    <el-table ref="table" v-loading="loading" :data="list" :height="tableHeight" style="width: 100%" border fit highlight-current-row>
      <el-table-column align="center" label="商品名称" width="100">
        <template slot-scope="scope">
          {{ scope.row.short_name }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="商品编码" width="120">
        <template slot-scope="scope">
          {{ scope.row.good_id }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="优先级" width="70">
        <template slot-scope="{row}">
          <span v-if="row.show" class="priority-cell">
            <a @click="handleEditPriority(row)">{{ row.priority }}</a>
            <el-button
              v-if="row.priority !== 0 && row.follow_id !== 0"
              class="priority-delete"
              icon="el-icon-close"
              circle
              @click.stop="handleDeletePriority(row)"
            />
          </span>
          <el-input v-else v-model="followTemp.priority" @keyup.enter.native="handleSetPriority" />
        </template>
      </el-table-column>
      <el-table-column align="center" label="外部编码" width="120">
        <template slot-scope="scope">
          <a :href="handleJumpOrigin(scope.row.origin, scope.row.origin_type)" target="_blank">{{ scope.row.origin }}</a>
        </template>
      </el-table-column>
      <el-table-column align="center" label="进货编码" width="120">
        <template slot-scope="scope">
          <a :href="handleJumpStock(scope.row.stock, scope.row.stock_type)" target="_blank">{{ scope.row.stock }}</a>
        </template>
      </el-table-column>
      <el-table-column align="center" label="商品类型" width="70">
        <template slot-scope="scope">
          {{ num2type(scope.row.good_type) }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="商品状态" width="70">
        <template slot-scope="scope">
          {{ num2status(scope.row.good_status) }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="首次刷单" width="90">
        <template slot-scope="scope">
          {{ scope.row.fake_date }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="首次推广" width="90">
        <template slot-scope="scope">
          {{ scope.row.promotion_date }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="完整名称">
        <template slot-scope="scope">
          {{ scope.row.name }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="操作" width="160">
        <template slot-scope="{row}">
          <el-button type="primary" size="mini" @click="handleUpdate(row)">编辑</el-button>
          <el-button type="danger" size="mini" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total > 0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.num" @pagination="getGoodList" />

    <!-- 商品信息编辑 -->
    <el-dialog title="修改商品信息" :visible.sync="dialogVisible">
      <el-form :model="temp" label-position="left" label-width="70px" style="width: 100%; padding: 0 4% 0 4%;">
        <el-form-item label="商品编码">
          <div>{{ temp.good_id }}</div>
        </el-form-item>
        <el-form-item label="商品名称">
          <el-input v-model="temp.short_name" />
        </el-form-item>
        <el-form-item label="外部编码">
          <el-input v-model="temp.origin" />
        </el-form-item>
        <el-form-item label="进货编码">
          <el-input v-model="temp.stock" />
        </el-form-item>
        <el-form-item label="商品类型">
          <el-select v-model="temp.good_type" class="filter-item" placeholder="请选择类型">
            <el-option v-for="item in typeList" :key="item.id" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="商品状态">
          <el-select v-model="temp.good_status" class="filter-item" placeholder="请选择状态">
            <el-option v-for="item in statusList" :key="item.id" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="完整名称">
          <el-input v-model="temp.name" />
        </el-form-item>
        <el-form-item label="添加别名">
          <el-input v-model="temp.alias" style="width:80%" />
          <el-button type="primary" size="mini" style="float:right;width:18%" @click="addGoodAlias(temp.good_id)">新增</el-button>
        </el-form-item>
        <el-form-item v-for="item in goodAliasList" :key="item.id" label="别名">
          <div>
            {{ item.name }}
            <el-button type="danger" size="mini" style="float:right" @click="delGoodAlias(item.id, temp.good_id)">删除</el-button>
          </div>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="danger" @click="dialogVisible = false">鍙栨秷</el-button>
        <el-button type="primary" @click="updateData()">纭畾</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Pagination from '@/components/Pagination'
import UploadExcelComponent from '@/components/UploadExcel'
import { GoodFollowStatus, GoodOriginType, GoodStockType, GoodStatus, GoodType } from '@/utils/const'
import { getGoodList, addGoodList, delGood, setGood, flushGood } from '@/api/system/good'
import { getGoodAliasById, addGoodAlias, delGoodAlias, delGoodAliasById } from '@/api/system/goodAlias'
import { getGoodFollowList, addGoodFollow, setGoodFollow, delGoodFollow } from '@/api/system/goodFollow'
import { getOwnShopList } from '@/api/system/shop'

export default {
  components: { Pagination, UploadExcelComponent },
  data() {
    return {
      userdata: {},
      tableHeight: 600,
      list: null,
      total: 0,
      loading: false,
      typeList: [], // 商品类型列表
      typeFilterList: [], // 商品类型筛选列表
      statusList: [], // 商品状态列表
      statusFilterList: [], // 商品状态筛选列表
      followFilterList: [], // 关注筛选列表
      shopList: [], // 本公司所有店铺列表
      goodAliasList: [], // 商品所有别名列表
      listFollow: [], // 商品优先级列表
      listQuery: {
        id: 0,
        page: 1,
        num: 10,
        search: null,
        type: 0,
        status: 0,
        follow: 1
      },
      temp: {},
      followTemp: {},
      dialogVisible: false
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
      this.getGoodList()
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
    this.typeList = GoodType.getList()
    this.typeFilterList = [{ id: 0, name: '全部类型' }].concat(this.typeList)
    this.statusList = GoodStatus.getList()
    this.statusFilterList = [{ id: 0, name: '全部状态' }].concat(this.statusList)
    this.followFilterList = GoodFollowStatus.getList()
    this.resetTemp()
    this.getOwnShopList()
  },
  methods: {
    resetTemp() {
      this.temp = {
        id: 0,
        good_id: '',
        name: '',
        origin: '',
        short_name: '',
        good_type: GoodType.NORMAL,
        good_status: GoodStatus.SALE,
        alias: ''
      }
      this.followTemp = {
        id: 0,
        good_id: '',
        priority: 0
      }
    },
    getGoodList() {
      this.loading = true
      getGoodList(
        this.listQuery
      ).then(response => {
        this.total = response.data.data.total
        this.list = (response.data.data.list || []).map(v => Object.assign({
          priority: 0,
          show: true,
          follow_id: 0
        }, v))
        this.getGoodFollowList()
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
        this.listFollow = response.data.data.list || []
        this.list.forEach(v => {
          v.priority = 0
          v.show = true
          v.follow_id = 0
          for (let i = 0; i < this.listFollow.length; ++i) {
            if (v.good_id === this.listFollow[i].good_id) {
              v.priority = this.listFollow[i].priority
              v.follow_id = this.listFollow[i].id
              break
            }
          }
        })
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
        this.getGoodList()
      })
    },
    num2status(num) {
      return GoodStatus.num2text(num)
    },
    num2type(num) {
      return GoodType.num2text(num)
    },
    handleJumpOrigin(id, type) {
      return GoodOriginType.getUrl(id, type)
    },
    handleJumpStock(id, type) {
      return GoodStockType.getUrl(id, type)
    },
    handleChange() {
      this.$store.commit('header/SET_HEADER_SHOP', this.listQuery.id)
      this.listQuery.page = 1
      this.getGoodList()
    },
    handleFilterChange() {
      this.listQuery.page = 1
      this.getGoodList()
    },
    handleSuccess({ results, header }) {
      const sname = header[0]
      const id = header[1]
      const priority = header[2]
      const type = header[3]
      const status = header[4]
      const origin = header[5]
      const origin_type = header[6]
      const stock = header[7]
      const stock_type = header[8]
      const name = header[9]
      const alias1 = header[10]
      const alias2 = header[11]
      const alias3 = header[12]
      const alias4 = header[13]
      const alias5 = header[14]
      const g = []
      let stop = false
      results.forEach(v => {
        const type_num = GoodType.text2num(v[type])
        const status_num = GoodStatus.text2num(v[status])
        const origin_num = GoodOriginType.text2num(v[origin_type])
        const stock_num = GoodStockType.text2num(v[stock_type])
        const priority_num = parseInt(v[priority] || 0)
        if (isNaN(priority_num) || priority_num < 0 || priority_num > 10) {
          console.log('优先级异常:' + v[id])
          stop = true
        }
        if (type_num === GoodType.OTHER) {
          console.log('商品类型异常:' + v[id])
          stop = true
        }
        if (status_num === GoodStatus.OTHER) {
          console.log('商品状态异常?' + v[id])
          stop = true
        }
        if (origin_num === GoodOriginType.OTHER) {
          console.log('外部编号异常:' + v[id])
          stop = true
        }
        if (stock_num === GoodStockType.OTHER) {
          console.log('进货编号异常:' + v[id])
          stop = true
        }
        g.push({
          i: v[id],
          n: v[name],
          sn: v[sname],
          o: v[origin],
          ot: origin_num,
          st: v[stock],
          stt: stock_num,
          t: type_num,
          s: status_num,
          p: priority_num,
          as: [v[alias1], v[alias2], v[alias3], v[alias4], v[alias5]]
        })
      })
      if (stop) {
        this.$message({ type: 'error', message: '商品信息异常!' })
        return
      }
      // 校验是否重复id
      for (let i = 0; i < g.length - 1; ++i) {
        for (let j = i + 1; j < g.length; ++j) {
          if (g[i].i === g[j].i) {
            this.$message({ type: 'error', message: '商品编号重复!' })
            console.log(g[i].i)
            return
          }
        }
      }
      addGoodList({
        id: this.listQuery.id,
        g: g
      }).then(() => {
        this.$message({ type: 'success', message: '导入成功!' })
        this.getGoodList()
      })
    },
    handleFlush() {
      flushGood({
        id: this.listQuery.id
      }).then(() => {
        this.$message({ type: 'success', message: '刷新成功!' })
        this.getGoodList()
      })
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row)
      getGoodAliasById({
        id: this.listQuery.id,
        gid: row.good_id
      }).then(response => {
        this.goodAliasList = response.data.data
        this.dialogVisible = true
      })
    },
    handleEditPriority(row) {
      this.list.forEach(v => {
        v.show = true
      })
      row.show = false
      this.followTemp = {
        id: row.follow_id || 0,
        good_id: row.good_id,
        priority: row.priority
      }
    },
    handleSetPriority() {
      const priority = parseInt(this.followTemp.priority)
      if (isNaN(priority) || priority < 0 || priority > 10) {
        this.$message({ type: 'error', message: '优先级必须在[0-10]之间!' })
        return
      }
      if (this.followTemp.id === 0) {
        if (priority === 0) {
          this.getGoodFollowList()
          return
        }
        addGoodFollow({
          id: this.listQuery.id,
          good_id: this.followTemp.good_id,
          priority: priority
        }).then(() => {
          this.$message({ type: 'success', message: '修改成功!' })
          this.getGoodFollowList()
        })
      } else if (priority === 0) {
        delGoodFollow({
          id: this.followTemp.id
        }).then(() => {
          this.$message({ type: 'success', message: '修改成功!' })
          this.getGoodFollowList()
        })
      } else {
        setGoodFollow({
          id: this.followTemp.id,
          priority: priority
        }).then(() => {
          this.$message({ type: 'success', message: '修改成功!' })
          this.getGoodFollowList()
        })
      }
    },
    handleDeletePriority(row) {
      delGoodFollow({
        id: row.follow_id
      }).then(() => {
        this.getGoodFollowList()
      })
    },
    updateData() {
      setGood({
        id: this.temp.id,
        name: this.temp.name,
        sname: this.temp.short_name,
        type: this.temp.good_type,
        status: this.temp.good_status,
        origin: this.temp.origin,
        origin_type: GoodOriginType.TAO_BAO,
        stock: this.temp.stock,
        stock_type: GoodStockType.ALIBABA
      }).then(() => {
        this.$message({ type: 'success', message: '修改成功!' })
        this.getGoodList()
        this.dialogVisible = false
      })
    },
    addGoodAlias(good_id) {
      addGoodAlias({
        id: this.listQuery.id,
        gid: this.temp.good_id,
        name: this.temp.alias
      }).then(() => {
        getGoodAliasById({
          id: this.listQuery.id,
          gid: good_id
        }).then(response => {
          this.$message({ type: 'success', message: '新增成功!' })
          this.goodAliasList = response.data.data
        })
      })
    },
    delGoodAlias(id, good_id) {
      delGoodAlias({
        id: id
      }).then(() => {
        getGoodAliasById({
          id: this.listQuery.id,
          gid: good_id
        }).then(response => {
          this.$message({ type: 'success', message: '删除成功!' })
          this.goodAliasList = response.data.data
        })
      })
    },
    handleDelete(row) {
      this.$confirm('确定要删除吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        delGoodAliasById({
          id: this.listQuery.id,
          gid: row.good_id
        }).then(() => {
          delGood({
            id: row.id
          }).then(() => {
            this.$message({ type: 'success', message: '删除成功!' })
            this.getGoodList()
          })
        })
      })
    }
  }
}
</script>

<style scoped>
.excel-import-row {
  position: sticky;
  top: 0;
  z-index: 9;
  display: flex;
  align-items: center;
  gap: 16px;
  min-height: 56px;
  padding: 6px 1%;
  margin-bottom: 8px;
  background: #fff;
  border-bottom: 1px solid #d8dce5;
}

.excel-import-row>div:last-child {
  flex: 1 1 auto;
  min-width: 0;
}

.excel-import-row ::v-deep .drop {
  margin: 0;
  font-size: 13px;
  border-width: 1px;
}

.excel-import-row ::v-deep .drop .el-button {
  margin-left: 10px;
}

.priority-cell {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
}

.priority-delete {
  width: 12px;
  height: 12px;
  min-height: 12px;
  padding: 0;
  font-size: 8px;
  color: #909399;
  background: #f4f4f5;
  border-color: #dcdfe6;
}

.priority-delete:hover,
.priority-delete:focus {
  color: #606266;
  background: #e9e9eb;
  border-color: #c8c9cc;
}
</style>
