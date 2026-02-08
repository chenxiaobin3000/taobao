<template>
  <div class="app-container">
    <el-form :model="listQuery" label-position="left" label-width="70px" style="width: 100%; padding: 0 1% 0 1%;">
      <el-form-item label="店铺:" prop="shopName">
        <el-select v-model="listQuery.id" class="filter-item" placeholder="请选择店铺" @change="handleChange">
          <el-option v-for="item in shopList" :key="item.id" :label="item.name" :value="item.id" />
        </el-select>
        <el-button type="primary" size="mini" style="float:right;width:60px" @click="handleExcel()">导入</el-button>
      </el-form-item>
    </el-form>
    <el-table ref="table" v-loading="loading" :data="list" :height="tableHeight" style="width: 100%" border fit highlight-current-row>
      <el-table-column align="center" label="商品名称" width="160">
        <template slot-scope="scope">
          {{ scope.row.short_name }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="商品类型" width="80">
        <template slot-scope="scope">
          {{ num2type(scope.row.good_type) }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="商品编码" width="160">
        <template slot-scope="scope">
          {{ scope.row.good_id }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="商品状态" width="160">
        <template slot-scope="scope">
          {{ num2status(scope.row.good_status) }}
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
      <upload-excel-component :on-success="handleSuccess" width="90%" line-height="300px" height="300px" />
    </el-dialog>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Pagination from '@/components/Pagination'
import UploadExcelComponent from '@/components/UploadExcel'
import { GoodStatus, GoodType } from '@/utils/const'
import { getGoodList, addGoodList, delGood, setGood } from '@/api/system/good'
import { getGoodAliasById, addGoodAlias, delGoodAlias, delGoodAliasById } from '@/api/system/goodAlias'
import { getShopList } from '@/api/system/shop'

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
      search: state => state.header.search,
      create: state => state.header.create
    })
  },
  watch: {
    search(newVal, oldVal) {
      this.listQuery.search = newVal
      this.getGoodList()
    },
    create() {
      this.$message({ type: 'error', message: '不支持新建!' })
    }
  },
  mounted: function() {
    setTimeout(() => {
      this.tableHeight = window.innerHeight - this.$refs.table.$el.offsetTop - 78
    }, 1000)
  },
  created() {
    this.userdata = this.$store.getters.userdata
    this.listQuery.id = 0
    this.typeList = GoodType.getList()
    this.statusList = GoodStatus.getList()
    this.resetTemp()
    this.getShopList()
  },
  methods: {
    resetTemp() {
      this.temp = {
        id: 0,
        good_id: '',
        name: '',
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
    getShopList() {
      getShopList({
        id: this.userdata.company.id,
        page: 1,
        num: 1000
      }).then(response => {
        this.shopList = response.data.data.list
        this.listQuery.id = this.shopList[0].id
        this.getGoodList()
      })
    },
    num2status(num) {
      return GoodStatus.num2text(num)
    },
    num2type(num) {
      return GoodType.num2text(num)
    },
    handleChange() {
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
      const name = header[4]
      const g = []
      results.forEach(v => {
        g.push({
          i: v[id],
          n: v[name],
          sn: v[sname],
          t: v[type],
          s: v[status]
        })
      })
      addGoodList({
        id: this.listQuery.id,
        g: g
      }).then(() => {
        this.$message({ type: 'success', message: '导入成功!' })
        this.getGoodList()
        this.dialogVisible = false
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
        status: this.temp.good_status
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
