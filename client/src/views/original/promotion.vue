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
      <el-table-column align="center" label="交易日期" width="160">
        <template slot-scope="scope">
          {{ scope.row.create_date }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="金额" width="80">
        <template slot-scope="scope">
          {{ scope.row.payment }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="类型" width="160">
        <template slot-scope="scope">
          {{ num2type(scope.row.promotion_type) }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="备注">
        <template slot-scope="scope">
          {{ scope.row.promotion_note }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="操作" width="80">
        <template slot-scope="{row}">
          <el-button type="danger" size="mini" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.num" @pagination="getPromotionList" />

    <el-dialog title="导入Excel" :visible.sync="dialogVisible">
      <pre style="text-align:center;font-size:13px;">日期2  |  类型3  |  金额5  |  备注7</pre>
      <upload-excel-component :on-success="handleSuccess" width="90%" line-height="300px" height="300px" />
    </el-dialog>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Pagination from '@/components/Pagination'
import UploadExcelComponent from '@/components/UploadExcel'
import { ImportCount, ImportSpan, PromotionType } from '@/utils/const'
import { sleep } from '@/utils/sleep'
import { xlsx_date_str } from '@/utils/xlsx'
import { getPromotionList, addPromotionList, delPromotion } from '@/api/original/promotion'
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
        uid: 0,
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
      this.getPromotionList()
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
    this.listQuery.uid = this.userdata.user.id
    this.getShopList()
  },
  methods: {
    getPromotionList() {
      this.loading = true
      getPromotionList(
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
        this.getPromotionList()
      })
    },
    num2type(num) {
      return PromotionType.num2text(num)
    },
    handleChange() {
      this.getPromotionList()
    },
    handleExcel() {
      this.dialogVisible = true
    },
    async handleSuccess({ results, header }) {
      const output = header[2]
      const create_date = header[1]
      const payment = header[4]
      const promotion_note = header[6]
      const p = []
      results.forEach(v => {
        if (v[output] === '支出') {
          p.push({
            d: xlsx_date_str(v[create_date]),
            p: v[payment],
            t: PromotionType.text2num(v[promotion_note]),
            n: v[promotion_note]
          })
        }
      })
      let length = p.length
      // 预校验数据
      for (let i = 0; i < length; ++i) {
        if (p[i].t === PromotionType.OTHER) {
          this.$message({ type: 'error', message: '数据异常!' })
          console.log(p[i])
          return
        }
      }
      if (length > ImportCount) {
        length = parseInt(length / ImportCount)
        for (let i = 0; i <= length; ++i) {
          addPromotionList({
            id: this.listQuery.id,
            uid: this.userdata.user.id,
            p: p.slice(i * ImportCount, (i + 1) * ImportCount)
          }).then(() => {
            if (i === length) {
              this.$message({ type: 'success', message: '导入成功!' })
              this.getPromotionList()
              this.dialogVisible = false
            } else {
              this.$message({ type: 'success', message: '正在导入!' })
            }
          })
          await sleep(ImportSpan)
        }
      } else {
        addPromotionList({
          id: this.listQuery.id,
          uid: this.userdata.user.id,
          p: p
        }).then(() => {
          this.$message({ type: 'success', message: '导入成功!' })
          this.getPromotionList()
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
        delPromotion({
          id: row.id
        }).then(() => {
          this.$message({ type: 'success', message: '删除成功!' })
          this.getPromotionList()
        })
      })
    }
  }
}
</script>
