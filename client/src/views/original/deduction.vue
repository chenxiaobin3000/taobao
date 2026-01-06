<template>
  <div class="app-container">
    <el-form :model="listQuery" label-position="left" label-width="70px" style="width: 100%; padding: 0 1% 0 1%;">
      <el-form-item label="店铺:" prop="shopName">
        <el-select v-model="listQuery.id" class="filter-item" placeholder="请选择店铺">
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
      <el-table-column align="center" label="商品编码" width="160">
        <template slot-scope="scope">
          {{ scope.row.good_id }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="完整名称">
        <template slot-scope="scope">
          {{ scope.row.name }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="操作" width="80">
        <template slot-scope="{row}">
          <el-button type="danger" size="mini" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getDeductionList" />

    <el-dialog title="导入Excel" :visible.sync="dialogVisible">
      <upload-excel-component :on-success="handleSuccess" width="90%" line-height="300px" height="300px" />
    </el-dialog>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Pagination from '@/components/Pagination'
import UploadExcelComponent from '@/components/UploadExcel'
import { getDeductionList, addDeduction, addDeductionList, delDeduction } from '@/api/original/deduction'
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
      shopList: [], // 本公司所有店铺列表
      listQuery: {
        id: 0,
        page: 1,
        num: 10,
        search: null
      },
      dialogVisible: false,
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
      this.getDeductionList()
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
    this.resetTemp()
    this.getShopList()
  },
  methods: {
    resetTemp() {
      this.temp = {
        id: 0,
        good_id: '',
        name: '',
        short_name: ''
      }
    },
    getDeductionList() {
      this.loading = true
      getDeductionList(
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
        this.getDeductionList()
      })
    },
    handleExcel() {
      this.dialogExcelVisible = true
    },
    handleSuccess({ results, header }) {
      const sname = header[0]
      const id = header[1]
      const name = header[2]
      const g = []
      results.forEach(v => {
        g.push({
          i: v[id],
          n: v[name],
          sn: v[sname]
        })
      })
      addDeductionList({
        id: this.listQuery.id,
        g: g
      }).then(() => {
        this.$message({ type: 'success', message: '导入成功!' })
        this.getDeductionList()
        this.dialogVisible = false
      })
    },
    createData() {
      addDeduction({
        id: this.listQuery.id,
        gid: this.temp.good_id,
        name: this.temp.name,
        sname: this.temp.short_name
      }).then(() => {
        this.$message({ type: 'success', message: '新增成功!' })
        this.getDeductionList()
        this.dialogVisible = false
      })
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row)
      this.dialogStatus = 'update'
      this.dialogVisible = true
    },
    updateData() {
      setDeduction({
        id: this.temp.id,
        name: this.temp.name,
        sname: this.temp.short_name
      }).then(() => {
        this.$message({ type: 'success', message: '修改成功!' })
        this.getDeductionList()
        this.dialogVisible = false
      })
    },
    handleDelete(row) {
      this.$confirm('确定要删除吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        delDeduction({
          id: row.id
        }).then(() => {
          this.$message({ type: 'success', message: '删除成功!' })
          this.getDeductionList()
        })
      })
    }
  }
}
</script>
