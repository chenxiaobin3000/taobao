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
      <el-table-column align="center" label="订单编码" width="160">
        <template slot-scope="scope">
          {{ scope.row.order_id }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="应付" width="160">
        <template slot-scope="scope">
          {{ scope.row.payment }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="实付">
        <template slot-scope="scope">
          {{ scope.row.actual_pay }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="采购">
        <template slot-scope="scope">
          {{ scope.row.procure_pay }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="状态">
        <template slot-scope="scope">
          {{ scope.row.order_status }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="创建时间">
        <template slot-scope="scope">
          {{ scope.row.create_time }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="商品id">
        <template slot-scope="scope">
          {{ scope.row.product_name }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="备注">
        <template slot-scope="scope">
          {{ scope.row.order_note }}
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

    <!-- 订单信息编辑 -->
    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogVisible">
      <el-form :model="temp" label-position="left" label-width="70px" style="width: 100%; padding: 0 4% 0 4%;">
        <el-form-item label="采购" prop="procure_pay">
          <el-input v-model="temp.procure_pay" />
        </el-form-item>
        <el-form-item label="状态" prop="order_status">
          <el-input v-model="temp.order_status" />
        </el-form-item>
        <el-form-item label="备注" prop="order_note">
          <el-input v-model="temp.order_note" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="danger" @click="dialogVisible=false">取消</el-button>
        <el-button type="primary" @click="dialogStatus==='create'?createData():updateData()">确定</el-button>
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
import { getGoodList, addGood, addGoodList, delGood, setGood } from '@/api/system/good'
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
      temp: {},
      dialogVisible: false,
      dialogExcelVisible: false,
      dialogStatus: '',
      textMap: {
        update: '修改商品信息',
        create: '新建商品'
      }
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
      this.resetTemp()
      this.dialogStatus = 'create'
      this.dialogVisible = true
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
      addGoodList({
        id: this.listQuery.id,
        g: g
      }).then(() => {
        this.$message({ type: 'success', message: '导入成功!' })
        this.getGoodList()
        this.dialogVisible = false
      })
    },
    createData() {
      addGood({
        id: this.listQuery.id,
        gid: this.temp.good_id,
        name: this.temp.name,
        sname: this.temp.short_name
      }).then(() => {
        this.$message({ type: 'success', message: '新增成功!' })
        this.getGoodList()
        this.dialogVisible = false
      })
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row)
      this.dialogStatus = 'update'
      this.dialogVisible = true
    },
    updateData() {
      setGood({
        id: this.temp.id,
        name: this.temp.name,
        sname: this.temp.short_name
      }).then(() => {
        this.$message({ type: 'success', message: '修改成功!' })
        this.getGoodList()
        this.dialogVisible = false
      })
    },
    handleDelete(row) {
      this.$confirm('确定要删除吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        delGood({
          id: row.id
        }).then(() => {
          this.$message({ type: 'success', message: '删除成功!' })
          this.getGoodList()
        })
      })
    }
  }
}
</script>
