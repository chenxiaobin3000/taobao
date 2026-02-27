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
      <el-table-column align="center" label="付款金额" width="80">
        <template slot-scope="scope">
          {{ scope.row.payment }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="采购金额" width="80">
        <template slot-scope="scope">
          {{ scope.row.procure }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="订单状态" width="80">
        <template slot-scope="scope">
          {{ num2type(scope.row.order_status) }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="时间" width="160">
        <template slot-scope="scope">
          {{ scope.row.create_time }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="商品" width="160">
        <template slot-scope="scope">
          {{ scope.row.good_names }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="备注">
        <template slot-scope="scope">
          {{ scope.row.order_note }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="操作" width="80">
        <template slot-scope="{row}">
          <el-button type="danger" size="mini" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.num" @pagination="getOrderList" />

    <el-dialog title="导入Excel" :visible.sync="dialogVisible">
      <upload-excel-component :on-success="handleSuccess" width="90%" line-height="300px" height="300px" />
    </el-dialog>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Pagination from '@/components/Pagination'
import UploadExcelComponent from '@/components/UploadExcel'
import { ImportCount, ImportSpan, OrderStatus } from '@/utils/const'
import { sleep } from '@/utils/sleep'
import { getOrderList, addOrderList, delOrder } from '@/api/trunk/order'
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
      this.getOrderList()
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
    getOrderList() {
      this.loading = true
      getOrderList(
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
        this.getOrderList()
      })
    },
    num2type(num) {
      return OrderStatus.num2text(num)
    },
    handleChange() {
      this.getOrderList()
    },
    handleExcel() {
      this.dialogVisible = true
    },
    async handleSuccess({ results, header }) {
      const order_id = header[0]
      const payment = header[6]
      const order_status = header[2]
      const create_time = header[3]
      const product_name = header[4]
      const order_note = header[5]
      const o = []
      results.forEach(v => {
        o.push({
          id: v[order_id],
          pa: v[payment],
          pr: 0,
          st: OrderStatus.text2num(v[order_status]),
          ct: v[create_time],
          na: v[product_name],
          pi: '',
          no: v[order_note]
        })
      })
      // 提取采购价
      let length = o.length
      for (let i = 0; i < length; ++i) {
        const ext = this.extract(o[i].no)
        if (!ext[0]) {
          this.$message({ type: 'error', message: '数据异常!' })
          console.log(o[i])
          return
        }
        o[i].pr = ext[1]
        o[i].pi = ext[2]
      }
      if (length > ImportCount) {
        length = parseInt(length / ImportCount)
        for (let i = 0; i <= length; ++i) {
          addOrderList({
            id: this.listQuery.id,
            o: o.slice(i * ImportCount, (i + 1) * ImportCount)
          }).then(() => {
            if (i === length) {
              this.$message({ type: 'success', message: '导入成功!' })
              this.getOrderList()
              this.dialogVisible = false
            } else {
              this.$message({ type: 'success', message: '正在导入!' })
            }
          })
          await sleep(ImportSpan)
        }
      } else {
        addOrderList({
          id: this.listQuery.id,
          o: o
        }).then(() => {
          this.$message({ type: 'success', message: '导入成功!' })
          this.getOrderList()
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
        delOrder({
          id: row.id
        }).then(() => {
          this.$message({ type: 'success', message: '删除成功!' })
          this.getOrderList()
        })
      })
    },
    // 从备注提取采购金额和订单号
    extract(note) {
      const ret = [false, -1, '']
      // 空数据直接返回0
      if (note === undefined) {
        return [true, 0, '0000000000000000000']
      }
      // 校验人工审核
      let count = 0
      const notes = note.split('|')
      for (let i = 0; i < notes.length; ++i) {
        if (notes[i].length > 19) {
          ++count
        }
      }
      if (count > 2 && note.indexOf('元-利润:0元') === -1) {
        console.log(notes.length)
        console.log('未经人工校验:' + note)
        return ret
      }
      const data = notes[0].trim()
      // 忽略长度小于订单编号的数据
      if (data.length < 20) {
        console.log('异常数据:' + note)
        return ret
      }
      // 按标准格式查找: tb:id-采购价:0元-利润:0元 |
      const first = data.indexOf(':')
      if (first === -1) {
        console.log('没有找到账号信息:' + data)
        return ret
      }
      const second = data.indexOf('-采购价:', first + 1)
      if (second === -1 || second - first !== 20) {
        console.log('没有找到-采购价:' + data)
        return ret
      }
      // 查找采购价
      const third = data.indexOf('元-利润:', second + 5)
      if (third === -1) {
        console.log('没有找到元-利润:' + data)
        return ret
      }
      ret[0] = true
      ret[1] = data.substring(second + 5, third)
      ret[2] = data.substring(first + 1, second)
      return ret
    }
  }
}
</script>
