<template>
  <div class="app-container">
    <el-form :model="listQuery" label-position="left" label-width="50px" style="width: 100%; padding: 0 1% 0 1%;">
      <el-form-item label="店铺:" prop="shopName">
        <el-select v-model="listQuery.id" class="filter-item" placeholder="请选择店铺" @change="handleChange">
          <el-option v-for="item in shopList" :key="item.id" :label="item.name" :value="item.id" />
        </el-select>
        <el-button type="primary" size="mini" style="float:right;width:60px" @click="handleExcel()">导入</el-button>
        <el-button type="danger" size="mini" style="float:right;width:60px;margin-right:10px;" @click="handleFlush()">刷新</el-button>
      </el-form-item>
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

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.num" @pagination="getGoodList" />

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
        <el-button type="danger" @click="dialogVisible=false">取消</el-button>
        <el-button type="primary" @click="updateData()">确定</el-button>
      </div>
    </el-dialog>

    <el-dialog title="导入Excel" :visible.sync="dialogExcelVisible">
      <pre style="text-align:center;font-size:13px;">商品名称1  |  商品编号2  |  类型3(商品,赠品,补差价)  |  状态4(在售,下架,删除)</pre>
      <pre style="text-align:center;font-size:13px;">外部编号5  |  外部类型6(淘宝,天猫)  |  完整名称7  |  别名8(最多5个)</pre>
      <upload-excel-component :on-success="handleSuccess" width="90%" line-height="300px" height="300px" />
    </el-dialog>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Pagination from '@/components/Pagination'
import UploadExcelComponent from '@/components/UploadExcel'
import { GoodOriginType, GoodStockType, GoodStatus, GoodType } from '@/utils/const'
import { getGoodList, addGoodList, delGood, setGood, flushGood } from '@/api/system/good'
import { getGoodAliasById, addGoodAlias, delGoodAlias, delGoodAliasById } from '@/api/system/goodAlias'
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
      statusList: [], // 商品状态列表
      shopList: [], // 本公司所有店铺列表
      goodAliasList: [], // 商品所有别名列表
      listQuery: {
        id: 0,
        page: 1,
        num: 10,
        search: null
      },
      temp: {},
      dialogVisible: false,
      dialogExcelVisible: false
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
    this.statusList = GoodStatus.getList()
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
    },
    getGoodList() {
      this.loading = true
      getGoodList(
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
      this.getGoodList()
    },
    handleExcel() {
      this.dialogExcelVisible = true
    },
    handleSuccess({ results, header }) {
      const sname = header[0]
      const id = header[1]
      const type = header[2]
      const status = header[3]
      const origin = header[4]
      const origin_type = header[5]
      const stock = header[6]
      const stock_type = header[7]
      const name = header[8]
      const alias1 = header[9]
      const alias2 = header[10]
      const alias3 = header[11]
      const alias4 = header[12]
      const alias5 = header[13]
      const g = []
      let stop = false
      results.forEach(v => {
        const type_num = GoodType.text2num(v[type])
        const status_num = GoodStatus.text2num(v[status])
        const origin_num = GoodOriginType.text2num(v[origin_type])
        const stock_num = GoodStockType.text2num(v[stock_type])
        if (type_num === GoodType.OTHER) {
          console.log('商品类型异常:' + v[id])
          stop = true
        }
        if (status_num === GoodStatus.OTHER) {
          console.log('商品状态异常:' + v[id])
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
        this.dialogExcelVisible = false
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
