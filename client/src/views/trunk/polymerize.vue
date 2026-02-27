<template>
  <div class="app-container">
    <el-form :model="listQuery" label-position="left" label-width="70px" style="width: 100%; padding: 0 1% 0 1%;">
      <el-form-item label="店铺:" prop="shopName">
        <el-select v-model="listQuery.id" class="filter-item" placeholder="请选择店铺" @change="handleChange">
          <el-option v-for="item in shopList" :key="item.id" :label="item.name" :value="item.id" />
        </el-select>
        <el-button type="primary" size="mini" style="float:right;width:60px" @click="handleTrunk()">合并</el-button>
      </el-form-item>
    </el-form>
    <el-table ref="table" v-loading="loading" :data="list" :height="tableHeight" style="width: 100%" border fit highlight-current-row>
      <el-table-column align="center" label="订单编号" width="160">
        <template slot-scope="scope">
          {{ scope.row.order_id }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="类型" width="80">
        <template slot-scope="scope">
          {{ num2type(scope.row.amount_type) }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="金额" width="80">
        <template slot-scope="scope">
          {{ scope.row.amount }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="时间" width="160">
        <template slot-scope="scope">
          {{ scope.row.create_time }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="备注">
        <template slot-scope="scope">
          {{ scope.row.polymerize_note }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="操作" width="80">
        <template slot-scope="{row}">
          <el-button type="danger" size="mini" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.num" @pagination="getPolymerizeList" />

    <el-dialog title="导入Excel" :visible.sync="dialogVisible">
      <upload-excel-component :on-success="handleSuccess" width="90%" line-height="300px" height="300px" />
    </el-dialog>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Pagination from '@/components/Pagination'
import UploadExcelComponent from '@/components/UploadExcel'
import { ImportCount, ImportSpan, DeductionType } from '@/utils/const'
import { sleep } from '@/utils/sleep'
import { getPolymerizeList, addPolymerizeList, delPolymerize } from '@/api/trunk/polymerize'
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
      dialogVisible: false
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
      this.getPolymerizeList()
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
    this.getShopList()
  },
  methods: {
    getPolymerizeList() {
      this.loading = true
      getPolymerizeList(
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
        this.getPolymerizeList()
      })
    },
    num2type(num) {
      return DeductionType.num2text(num)
    },
    handleChange() {
      this.getPolymerizeList()
    },
    handleExcel() {
      this.dialogVisible = true
    },
    async handleSuccess({ results, header }) {
      const order_id = header[2]
      const amount = header[5]
      const create_time = header[0]
      const polymerize_note = header[7]
      const p = []
      results.forEach(v => {
        if (v[amount] > 0 && v[polymerize_note].length > 4) {
          p.push({
            o: v[order_id],
            a: v[amount],
            t: DeductionType.text2num(v[polymerize_note]),
            c: v[create_time],
            n: v[polymerize_note]
          })
        }
      })
      // 预校验数据
      for (let i = 0; i < p.length; ++i) {
        if (p[i].t === DeductionType.OTHER || p[i].o.length !== 19) {
          this.$message({ type: 'error', message: '异常数据!' })
          console.log(p[i])
          return
        }
      }
      let length = p.length
      if (length > ImportCount) {
        length = parseInt(length / ImportCount)
        for (let i = 0; i <= length; ++i) {
          addPolymerizeList({
            id: this.listQuery.id,
            p: p.slice(i * ImportCount, (i + 1) * ImportCount)
          }).then(() => {
            if (i === length) {
              this.$message({ type: 'success', message: '导入成功!' })
              this.getPolymerizeList()
              this.dialogVisible = false
            } else {
              this.$message({ type: 'success', message: '正在导入!' })
            }
          })
          await sleep(ImportSpan)
        }
      } else {
        addPolymerizeList({
          id: this.listQuery.id,
          p: p
        }).then(() => {
          this.$message({ type: 'success', message: '导入成功!' })
          this.getPolymerizeList()
          this.dialogVisible = false
        })
      }
    },
    handleDelete(row) {
      this.$confirm('确定要删除吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        delPolymerize({
          id: row.id
        }).then(() => {
          this.$message({ type: 'success', message: '删除成功!' })
          this.getPolymerizeList()
        })
      })
    }
  }
}
</script>
