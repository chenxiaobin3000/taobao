<template>
  <div class="app-container">
    <el-form :model="listQuery" label-position="left" label-width="70px" style="width: 100%; padding: 0 1% 0 1%;">
      <el-form-item label="店铺:" prop="shopName">
        <el-select v-model="listQuery.id" class="filter-item" placeholder="请选择店铺" @change="handleChange">
          <el-option v-for="item in shopList" :key="item.id" :label="item.name" :value="item.id" />
        </el-select>
        <el-button type="primary" size="mini" style="float:right;width:60px" @click="handleExcel()">导入</el-button>
        <el-button type="danger" size="mini" style="float:right;width:60px;margin-right:10px;" @click="handleDeleteAll()">清空</el-button>
      </el-form-item>
    </el-form>
    <el-table ref="table" v-loading="loading" :data="list" :height="tableHeight" style="width: 100%" border fit highlight-current-row>
      <el-table-column align="center" label="订单编号" width="160">
        <template slot-scope="scope">
          {{ scope.row.order_id }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="财务类型" width="80">
        <template slot-scope="scope">
          {{ num2ftype(scope.row.finance_type) }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="扣费类型" width="80">
        <template slot-scope="scope">
          {{ num2dtype(scope.row.amount_type) }}
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
          {{ scope.row.deduction_note }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="操作" width="80">
        <template slot-scope="{row}">
          <el-button type="danger" size="mini" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.num" @pagination="getDeductionList" />

    <el-dialog title="导入Excel" :visible.sync="dialogVisible">
      <pre style="text-align:center;font-size:13px;">时间1  |  类型5  |  金额7  |  备注16</pre>
      <upload-excel-component :on-success="handleSuccess" width="90%" line-height="300px" height="300px" />
    </el-dialog>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Pagination from '@/components/Pagination'
import UploadExcelComponent from '@/components/UploadExcel'
import { DefaultOrder, ImportCount, ImportSpan, DeductionType, FinanceType } from '@/utils/const'
import { sleep } from '@/utils/sleep'
import { getDeductionList, addDeductionList, delDeduction, delAllDeduction } from '@/api/original/deduction'
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
    console.log(this.userdata)
    this.listQuery.id = 0
    this.listQuery.uid = this.userdata.user.id
    this.getShopList()
  },
  methods: {
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
    num2dtype(num) {
      return DeductionType.num2text(num)
    },
    num2ftype(num) {
      return FinanceType.num2text(num)
    },
    handleChange() {
      this.getDeductionList()
    },
    handleExcel() {
      this.dialogVisible = true
    },
    async handleSuccess({ results, header }) {
      const create_time = header[0]
      const finance_type = header[4]
      const amount = header[6]
      const deduction_note = header[15]
      const d = []
      let stop = false
      results.forEach(v => {
        if (v[amount] > 0 && !stop) {
          let oid = ''
          let dtype = DeductionType.text2num(note)
          const note = v[deduction_note]
          console.log(note)
          const ftype = FinanceType.text2num(v[finance_type])
          if (note.length < 2) {
            // 忽略在线支付
            if (ftype === FinanceType.ONLINE) {
              dtype = DeductionType.FILTER
              oid = DefaultOrder
            } else {
              stop = true
              this.$message({ type: 'error', message: '没有备注信息!' })
              console.log(v)
              return
            }
          }
          // 从备注抓取订单号
          let first = 0
          let second = 0
          switch (dtype) {
            case DeductionType.FU_WU_FEI: // 基础软件服务费
            case DeductionType.XIN_XIANG: // 品牌新享淘宝新客营销
            case DeductionType.XIN_KE: // 淘宝新客礼金技术服务费
            case DeductionType.TAO_JIN_BI: // 淘金币软件服务费
            case DeductionType.XIAN_YONG_HOU_FU: // 先用后付技术服务费()
            case DeductionType.KUA_JING_JI_CHU: // 淘宝天猫跨境服务基础费
            case DeductionType.KUA_JING_ZENG_ZHI: // 淘宝天猫跨境服务增值费
            case DeductionType.KUA_JING_DA_JIAN: // 出海增长计划中大件跨境服务增值费
            case DeductionType.TAO_TE: // 淘特营销推广服务费
            case DeductionType.XIAN_SHI: // 限时红包代商家垫付扣回
            case DeductionType.XIN_PIN: // 品牌新享淘宝新品营销
            case DeductionType.XIN_XIANG_FU_WU: // 品牌新享-淘宝营销托管
            case DeductionType.XIAO_FEI_QUAN: // 消费券代付资金扣回
            case DeductionType.GUAN_KONG: // 保证金管控资金使用
              first = note.indexOf('(') + 1
              second = note.indexOf(')', first)
              if (first !== -1 && second !== -1 && second - first === 19) {
                oid = note.substring(first, second)
              } else {
                stop = true
                this.$message({ type: 'error', message: '备注信息格式异常!' })
                console.log(v)
                return
              }
              break

            case DeductionType.TI_YAN: // 消费者体验提升计划服务费
              first = note.indexOf('订单号') + 3
              second = note.indexOf('，', first)
              if (first !== -1 && second !== -1 && second - first === 19) {
                oid = note.substring(first, second)
              } else {
                stop = true
                this.$message({ type: 'error', message: '备注信息格式异常!' })
                console.log(v)
                return
              }
              break

            case DeductionType.XIAN_YONG_TIAO_ZHANG: // 先用后付技术服务费-
              first = note.indexOf('(') + 1
              second = note.indexOf(')', first)
              if (first !== -1 && second !== -1 && second - first === 19) {
                oid = note.substring(first, second)
              } else {
                stop = true
                this.$message({ type: 'error', message: '备注信息格式异常!' })
                console.log(v)
                return
              }
              break

            // 无订单信息
            case DeductionType.GONG_YI: // 公益宝贝捐赠
            case DeductionType.YAN_CHI_FA_HUO: // 延迟发货赔付
            case DeductionType.XU_JIA_FA_HUO: // 虚假发货赔付
            case DeductionType.WU_LIU_YI_CHANG: // 物流异常赔付
            case DeductionType.QUE_HUO: // 缺货赔付
            case DeductionType.HUA_BEI: // 花呗服务费
              oid = DefaultOrder
              break

            // 不处理
            case DeductionType.TUI_KUAN: // 退款
            case DeductionType.ZHUAN_ZHANG: // 转账
            case DeductionType.BAO_ZHENG_JIN: // 保证金
            case DeductionType.DA_KUAN: // 小额打款
              oid = DefaultOrder
              break

            case DeductionType.OTHER: // 异常
              stop = true
              this.$message({ type: 'error', message: '备注信息异常!' })
              console.log(v)
              return

            case DeductionType.FILTER: // 过滤
              break
          }
          if (oid.length !== 19) {
            this.$message({ type: 'error', message: '关联订单号异常!' })
            console.log(v)
            return
          }
          d.push({
            o: oid,
            f: ftype,
            a: v[amount],
            t: dtype,
            c: v[create_time],
            n: note
          })
        }
      })
      if (stop) {
        return
      }
      // 预校验数据
      for (let i = 0; i < d.length; ++i) {
        if (d[i].t === DeductionType.OTHER || d[i].o.length !== 19) {
          this.$message({ type: 'error', message: '异常数据!' })
          console.log(d[i])
          return
        }
      }
      let length = d.length
      if (length > ImportCount) {
        length = parseInt(length / ImportCount)
        for (let i = 0; i <= length; ++i) {
          addDeductionList({
            id: this.listQuery.id,
            uid: this.userdata.user.id,
            d: d.slice(i * ImportCount, (i + 1) * ImportCount)
          }).then(() => {
            if (i === length) {
              this.$message({ type: 'success', message: '导入成功!' })
              this.getDeductionList()
              this.dialogVisible = false
            } else {
              this.$message({ type: 'success', message: '正在导入!' })
            }
          })
          await sleep(ImportSpan)
        }
      } else {
        addDeductionList({
          id: this.listQuery.id,
          uid: this.userdata.user.id,
          d: d
        }).then(() => {
          this.$message({ type: 'success', message: '导入成功!' })
          this.getDeductionList()
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
        delDeduction({
          id: row.id
        }).then(() => {
          this.$message({ type: 'success', message: '删除成功!' })
          this.getDeductionList()
        })
      })
    },
    handleDeleteAll() {
      this.$confirm('确定要清空数据吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        delAllDeduction({
          id: this.listQuery.id,
          uid: this.userdata.user.id
        }).then(() => {
          this.$message({ type: 'success', message: '删除成功!' })
          this.getDeductionList()
        })
      })
    }
  }
}
</script>
