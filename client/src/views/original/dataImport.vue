<template>
  <div class="app-container data-import-page">
    <div class="import-row">
      <div
        class="file-upload"
        :class="{ disabled: processing }"
        @click="handleClickUpload"
        @drop.prevent="handleDrop"
        @dragover.prevent
        @dragenter.prevent
      >
        <span>{{ processing ? '正在处理，请稍候' : '拖拽原始数据文件夹到这里' }}<em v-if="!processing">浏览本地</em></span>
        <input
          ref="importFolder"
          type="file"
          webkitdirectory
          directory
          multiple
          accept=".xls,.xlsx,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
          @change="handleFolderChange"
        >
      </div>
    </div>

    <el-form :model="listQuery" label-position="left" label-width="50px" class="filter-row">
      <el-row>
        <el-col :span="6">
          <el-form-item label="店铺">
            <el-select v-model="listQuery.id" class="filter-item" placeholder="请选择店铺" :disabled="processing" @change="handleShopChange">
              <el-option v-for="item in shopList" :key="item.id" :label="item.name" :value="item.id" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="18">
          <el-button v-if="hasTrunkPermission" type="primary" :loading="processing" :disabled="!listQuery.id" class="merge-button" @click="handleMergeAll">一键合并</el-button>
          <el-button type="success" :loading="processing" class="init-button" @click="handleInitializeFolder">初始化</el-button>
          <el-button type="danger" :loading="processing" :disabled="!listQuery.id" class="clear-button" @click="handleClearAll">一键清空</el-button>
        </el-col>
      </el-row>
    </el-form>

    <el-progress v-if="processing || progress > 0" :percentage="progress" class="progress" />

    <div ref="processInfo" class="process-info">
      <div v-if="processLogs.length === 0" class="process-placeholder">处理信息会显示在这里</div>
      <div
        v-for="(item, index) in processLogs"
        :key="index"
        class="process-line"
        :class="`process-line-${item.type}`"
      >
        {{ item.text }}
      </div>
    </div>
  </div>
</template>

<script>
import XLSX from 'xlsx'
import { saveAs } from 'file-saver'
import { excelDateToText } from '@/utils/excel'
import { DeductionType, FinanceType, GoodOriginType, GoodStatus, GoodStockType, GoodType, NoneTime, OrderStatus, PromotionType, RefundStatus, RefundType } from '@/utils/const'
import { extractOrderProcure, parseDeductionRows } from '@/utils/deduction'
import { getOwnShopList } from '@/api/system/shop'
import { addGoodList, getGoodInitZip } from '@/api/system/good'
import { addUserOrderList, delAllUserOrder } from '@/api/original/order'
import { delAllUserFake } from '@/api/original/fake'
import { addUserPromotionList, delAllUserPromotion } from '@/api/original/promotion'
import { addUserPromotionDetailList, delAllUserPromotionDetail } from '@/api/original/promotionDetail'
import { addUserDeductionList, delAllUserDeduction } from '@/api/original/deduction'
import { delAllUserDeductionDiscard } from '@/api/original/deductionDiscard'
import { addUserPolymerizeList, delAllUserPolymerize } from '@/api/original/polymerize'
import { delAllUserPolymerizeDiscard } from '@/api/original/polymerizeDiscard'
import { addUserRefundList, delAllUserRefund } from '@/api/original/refund'
import { delAllUserRefundGift } from '@/api/original/refundGift'
import { addUserTransferList, delAllUserTransfer } from '@/api/original/transfer'
import { delAllUserPurchase } from '@/api/original/purchase'
import { mergeOrder } from '@/api/trunk/order'
import { mergeFake } from '@/api/trunk/fake'
import { mergePromotion } from '@/api/trunk/promotion'
import { mergePromotionDetail } from '@/api/trunk/promotionDetail'
import { mergeDeduction } from '@/api/trunk/deduction'
import { mergePolymerize } from '@/api/trunk/polymerize'
import { mergeRefund } from '@/api/trunk/refund'
import { mergeTransfer } from '@/api/trunk/transfer'

const MODULES = [
  { name: '商品', payload: 'g', parse: 'parseGoods', add: addGoodList },
  { name: '订单', payload: 'o', parse: 'parseOrders', add: addUserOrderList },
  { name: '推广', payload: 'p', parse: 'parsePromotions', add: addUserPromotionList },
  { name: '推广明细', payload: 'p', parse: 'parsePromotionDetails', add: addUserPromotionDetailList },
  { name: '扣费', payload: 'd', parse: 'parseDeductions', add: addUserDeductionList },
  { name: '聚合', payload: 'p', parse: 'parsePolymerizes', add: addUserPolymerizeList },
  { name: '退货', payload: 'r', parse: 'parseRefunds', add: addUserRefundList },
  { name: '打款', payload: 't', parse: 'parseTransfers', add: addUserTransferList }
]

const MERGE_MODULES = [
  { name: '订单', merge: mergeOrder },
  { name: '刷单', merge: mergeFake },
  { name: '推广', merge: mergePromotion },
  { name: '推广明细', merge: mergePromotionDetail },
  { name: '扣费', merge: mergeDeduction },
  { name: '聚合', merge: mergePolymerize },
  { name: '退货', merge: mergeRefund },
  { name: '打款', merge: mergeTransfer }
]

const CLEAR_MODULES = [
  { name: '订单', delAll: delAllUserOrder },
  { name: '刷单', delAll: delAllUserFake },
  { name: '推广', delAll: delAllUserPromotion },
  { name: '推广明细', delAll: delAllUserPromotionDetail },
  { name: '扣费', delAll: delAllUserDeduction },
  { name: '扣费(过滤)', delAll: delAllUserDeductionDiscard },
  { name: '聚合', delAll: delAllUserPolymerize },
  { name: '聚合(过滤)', delAll: delAllUserPolymerizeDiscard },
  { name: '退货', delAll: delAllUserRefund },
  { name: '退货(过滤)', delAll: delAllUserRefundGift },
  { name: '打款', delAll: delAllUserTransfer },
  { name: '采购', delAll: delAllUserPurchase }
]

export default {
  data() {
    return {
      userdata: {},
      shopList: [],
      listQuery: {
        id: 0,
        uid: 0
      },
      processLogs: [],
      processing: false,
      progress: 0
    }
  },
  computed: {
    hasTrunkPermission() {
      return this.$store.getters.roles.includes(4000)
    }
  },
  created() {
    this.userdata = this.$store.getters.userdata
    this.listQuery.id = this.$store.getters.shop
    this.listQuery.uid = this.userdata.user.id
    this.getOwnShopList()
  },
  methods: {
    getOwnShopList() {
      return getOwnShopList({
        id: this.userdata.company.id,
        uid: this.userdata.user.id
      }).then(response => {
        this.shopList = response.data.data
        if (this.listQuery.id === 0 && this.shopList.length > 0) {
          this.listQuery.id = this.shopList[0].id
        }
      })
    },
    handleShopChange() {
      this.$store.commit('header/SET_HEADER_SHOP', this.listQuery.id)
    },
    handleClickUpload() {
      if (this.processing) {
        return
      }
      this.$refs.importFolder.click()
    },
    async handleFolderChange(e) {
      const files = Array.from(e.target.files || [])
      e.target.value = ''
      await this.handleFiles(files)
    },
    async handleDrop(e) {
      if (this.processing) {
        return
      }
      const files = await this.getDroppedFiles(e.dataTransfer)
      await this.handleFiles(files)
    },
    async getDroppedFiles(dataTransfer) {
      const items = Array.from(dataTransfer.items || [])
      if (items.length > 0 && items[0].webkitGetAsEntry) {
        const files = []
        for (const item of items) {
          const entry = item.webkitGetAsEntry()
          if (entry) {
            files.push(...await this.readEntry(entry))
          }
        }
        return files
      }
      return Array.from(dataTransfer.files || [])
    },
    readEntry(entry) {
      if (entry.isFile) {
        return new Promise(resolve => {
          entry.file(file => resolve([file]))
        })
      }
      if (entry.isDirectory) {
        return new Promise(resolve => {
          const reader = entry.createReader()
          const entries = []
          const readBatch = () => {
            reader.readEntries(async batch => {
              if (batch.length === 0) {
                const files = []
                for (const item of entries) {
                  files.push(...await this.readEntry(item))
                }
                resolve(files)
              } else {
                entries.push(...batch)
                readBatch()
              }
            })
          }
          readBatch()
        })
      }
      return Promise.resolve([])
    },
    async handleFiles(files) {
      if (!this.listQuery.id) {
        this.$message({ type: 'error', message: '请先选择店铺!' })
        return
      }
      const excelFiles = files.filter(file => this.isExcel(file.name))
      if (excelFiles.length === 0) {
        this.processLogs = []
        this.log('文件夹中没有Excel文件!', 'error')
        this.$message({ type: 'error', message: '文件夹中没有Excel文件!' })
        return
      }
      const fileMap = this.buildModuleFileMap(excelFiles)
      this.processing = true
      this.progress = 0
      this.processLogs = []
      this.log(`开始批量导入，店铺: ${this.getShopName()}`)
      try {
        for (let i = 0; i < MODULES.length; i++) {
          const module = MODULES[i]
          const file = fileMap[module.name]
          if (!file) {
            this.log(`${module.name}: 未找到同名Excel，跳过`, 'warn')
            this.progress = Math.floor(((i + 1) / MODULES.length) * 100)
            continue
          }
          this.log(`${module.name}: 读取 ${file.name}`)
          const sheet = await this.readExcel(file)
          const records = this[module.parse](sheet.results, sheet.header)
          if (records.length === 0) {
            throw new Error(`${module.name}: 没有可导入数据`)
          }
          this.log(`${module.name}: 解析 ${records.length} 条`)
          await this.uploadChunks(module, records)
          this.log(`${module.name}: 原始数据导入完成`, 'success')
          this.progress = Math.floor(((i + 1) / MODULES.length) * 100)
        }
        this.progress = 100
        this.log('批量导入完成', 'success')
        this.$message({ type: 'success', message: '批量导入完成!' })
      } catch (error) {
        this.log(`处理失败: ${this.getErrorMessage(error)}`, 'error')
        this.$message({ type: 'error', message: '批量导入失败，请查看处理信息!' })
      } finally {
        this.processing = false
      }
    },
    async handleMergeAll() {
      if (!this.listQuery.id) {
        this.$message({ type: 'error', message: '请先选择店铺!' })
        return
      }
      this.processing = true
      this.progress = 0
      this.processLogs = []
      this.log(`开始一键合并，店铺: ${this.getShopName()}`)
      try {
        await this.mergeAllModules()
        this.progress = 100
        this.log('一键合并完成', 'success')
        this.$message({ type: 'success', message: '一键合并完成!' })
      } catch (error) {
        this.log(`合并失败: ${this.getErrorMessage(error)}`, 'error')
        this.$message({ type: 'error', message: '一键合并失败，请查看处理信息!' })
      } finally {
        this.processing = false
      }
    },
    async handleInitializeFolder() {
      this.processing = true
      this.progress = 0
      this.processLogs = []
      try {
        this.log('开始生成初始化压缩包')
        const response = await getGoodInitZip({
          id: this.userdata.company.id
        })
        const contentType = response.headers['content-type'] || ''
        if (contentType.indexOf('application/json') !== -1) {
          const message = await this.readBlobError(response.data)
          throw new Error(message)
        }
        this.progress = 100
        const saved = await this.saveInitZip(response.data)
        if (!saved) {
          this.log('已取消保存初始化压缩包', 'warn')
          this.$message({ type: 'warning', message: '已取消保存!' })
          return
        }
        this.log('初始化压缩包生成完成', 'success')
        this.$message({ type: 'success', message: '初始化压缩包生成完成!' })
      } catch (error) {
        this.log(`初始化失败: ${this.getErrorMessage(error)}`, 'error')
        this.$message({ type: 'error', message: '初始化失败，请查看处理信息!' })
      } finally {
        this.processing = false
      }
    },
    async saveInitZip(blob) {
      const fileName = '淘宝数据.zip'
      if (window.isSecureContext && window.showSaveFilePicker) {
        this.log('请选择初始化压缩包保存位置，默认位置为下载目录')
        try {
          const handle = await window.showSaveFilePicker({
            suggestedName: fileName,
            startIn: 'downloads',
            types: [{
              description: 'ZIP压缩包',
              accept: {
                'application/zip': ['.zip']
              }
            }]
          })
          const writable = await handle.createWritable()
          await writable.write(blob)
          await writable.close()
          return true
        } catch (error) {
          if (error && error.name === 'AbortError') {
            return false
          }
          throw error
        }
      }
      this.log('当前环境不支持保存位置选择，已保存到浏览器默认下载目录', 'warn')
      saveAs(blob, fileName)
      return true
    },
    readBlobError(blob) {
      return new Promise(resolve => {
        const reader = new FileReader()
        reader.onload = e => {
          try {
            const data = JSON.parse(e.target.result)
            resolve(data.msg || '未知错误')
          } catch (error) {
            resolve('未知错误')
          }
        }
        reader.onerror = () => resolve('未知错误')
        reader.readAsText(blob)
      })
    },
    handleClearAll() {
      if (!this.listQuery.id) {
        this.$message({ type: 'error', message: '请先选择店铺!' })
        return
      }
      this.$confirm('确定要清空当前店铺下所有原始数据吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.clearAllOriginalData()
      })
    },
    async clearAllOriginalData() {
      this.processing = true
      this.progress = 0
      this.processLogs = []
      this.log(`开始一键清空，店铺: ${this.getShopName()}`)
      try {
        for (let i = 0; i < CLEAR_MODULES.length; i++) {
          const module = CLEAR_MODULES[i]
          await module.delAll({
            id: this.listQuery.id,
            uid: this.userdata.user.id
          })
          this.progress = Math.floor(((i + 1) / CLEAR_MODULES.length) * 100)
          this.log(`${module.name}: 已清空`, 'success')
        }
        this.progress = 100
        this.log('一键清空完成', 'success')
        this.$message({ type: 'success', message: '一键清空完成!' })
      } catch (error) {
        this.log(`清空失败: ${this.getErrorMessage(error)}`, 'error')
        this.$message({ type: 'error', message: '一键清空失败，请查看处理信息!' })
      } finally {
        this.processing = false
      }
    },
    async mergeAllModules() {
      for (let i = 0; i < MERGE_MODULES.length; i++) {
        await this.mergeModule(MERGE_MODULES[i])
        this.progress = Math.floor(((i + 1) / MERGE_MODULES.length) * 100)
      }
    },
    async mergeModule(module) {
      await module.merge({ id: this.listQuery.id })
      this.log(`${module.name}: 已合并到主干`, 'success')
    },
    getShopName() {
      const shop = this.shopList.find(item => item.id === this.listQuery.id)
      return shop ? shop.name : ''
    },
    buildModuleFileMap(files) {
      const map = {}
      files.forEach(file => {
        const name = file.name.replace(/\.(xlsx|xls)$/i, '')
        if (MODULES.some(item => item.name === name)) {
          if (map[name]) {
            throw new Error(`${name}: 存在重复Excel文件`)
          }
          map[name] = file
        }
      })
      return map
    },
    isExcel(name) {
      return /\.xlsx?$/i.test(name)
    },
    readExcel(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader()
        reader.onload = e => {
          try {
            const data = new Uint8Array(e.target.result)
            const workbook = XLSX.read(data, { type: 'array' })
            const sheetName = workbook.SheetNames[0]
            const worksheet = workbook.Sheets[sheetName]
            const rows = XLSX.utils.sheet_to_json(worksheet, { header: 1, defval: '' })
            const header = rows[0] || []
            const body = rows.slice(1).filter(row => row.some(value => value !== ''))
            const results = body.map(row => {
              const item = {}
              header.forEach((key, index) => {
                item[key] = row[index] === undefined ? '' : row[index]
              })
              return item
            })
            resolve({ header, results })
          } catch (error) {
            reject(error)
          }
        }
        reader.onerror = () => reject(reader.error)
        reader.readAsArrayBuffer(file)
      })
    },
    async uploadChunks(module, records) {
      const chunkSize = 1000
      for (let i = 0; i < records.length; i += chunkSize) {
        const chunk = records.slice(i, i + chunkSize)
        await module.add({
          id: this.listQuery.id,
          uid: this.userdata.user.id,
          [module.payload]: chunk
        })
        this.log(`${module.name}: 已上传 ${Math.min(i + chunk.length, records.length)}/${records.length}`, 'success')
      }
    },
    parseGoods(results, header) {
      const shortName = header[0]
      const goodId = header[1]
      const priority = header[2]
      const type = header[3]
      const status = header[4]
      const origin = header[5]
      const originType = header[6]
      const stock = header[7]
      const stockType = header[8]
      const name = header[9]
      const alias1 = header[10]
      const alias2 = header[11]
      const alias3 = header[12]
      const alias4 = header[13]
      const alias5 = header[14]
      const records = results.map((v, index) => {
        const typeNum = GoodType.text2num(v[type])
        const statusNum = GoodStatus.text2num(v[status])
        const originNum = GoodOriginType.text2num(v[originType])
        const stockNum = GoodStockType.text2num(v[stockType])
        const priorityNum = parseInt(v[priority] || 0)
        if (isNaN(priorityNum) || priorityNum < 0 || priorityNum > 10) {
          throw new Error(`商品第${index + 2}行优先级异常: ${v[goodId]}`)
        }
        if (typeNum === GoodType.OTHER) {
          throw new Error(`商品第${index + 2}行类型异常: ${v[goodId]}`)
        }
        if (statusNum === GoodStatus.OTHER) {
          throw new Error(`商品第${index + 2}行状态异常: ${v[goodId]}`)
        }
        if (originNum === GoodOriginType.OTHER) {
          throw new Error(`商品第${index + 2}行外部编号异常: ${v[goodId]}`)
        }
        if (stockNum === GoodStockType.OTHER) {
          throw new Error(`商品第${index + 2}行进货编号异常: ${v[goodId]}`)
        }
        return {
          i: v[goodId],
          n: v[name],
          sn: v[shortName],
          o: v[origin],
          ot: originNum,
          st: v[stock],
          stt: stockNum,
          t: typeNum,
          s: statusNum,
          p: priorityNum,
          as: [v[alias1], v[alias2], v[alias3], v[alias4], v[alias5]]
        }
      })
      for (let i = 0; i < records.length - 1; ++i) {
        for (let j = i + 1; j < records.length; ++j) {
          if (records[i].i === records[j].i) {
            throw new Error(`商品编号重复: ${records[i].i}`)
          }
        }
      }
      return records
    },
    parseOrders(results, header) {
      const orderId = header[0]
      const payment = header[6]
      const orderStatus = header[2]
      const createTime = header[3]
      const productName = header[4]
      const orderNote = header[5]
      const records = results.map(v => ({
        id: v[orderId],
        pa: v[payment],
        pr: 0,
        st: OrderStatus.text2num(v[orderStatus]),
        ct: v[createTime],
        na: v[productName],
        pi: '',
        no: v[orderNote]
      }))
      const errors = []
      records.forEach((record, index) => {
        if (record.st === OrderStatus.OTHER) {
          errors.push(this.formatOrderImportError(index, '订单状态异常', record))
          return
        }
        const ext = extractOrderProcure(record.no, record.id, message => this.log(message))
        if (ext[0]) {
          record.pr = ext[1]
          record.pi = ext[2]
        } else if (![OrderStatus.CLOSE, OrderStatus.UNPAID, OrderStatus.PAID, OrderStatus.UNCREATED].includes(record.st) && parseFloat(record.pa) > 6) {
          errors.push(this.formatOrderImportError(index, '订单备注解析异常', record))
        }
      })
      if (errors.length > 0) {
        throw new Error(`订单数据异常，共${errors.length}条:\n\n${errors.join('\n\n')}`)
      }
      return records
    },
    formatOrderImportError(index, reason, order) {
      return [
        `行号: ${index + 2}`,
        `原因: ${reason}`,
        `订单编号: ${order.id}`,
        `订单状态: ${order.st}`,
        `付款金额: ${order.pa}`,
        `创建时间: ${order.ct}`,
        `商品名称: ${order.na}`,
        `备注: ${order.no}`
      ].join('\n')
    },
    parsePromotions(results, header) {
      const output = header[2]
      const createDate = header[1]
      const payment = header[4]
      const promotionNote = header[6]
      const records = []
      results.forEach(v => {
        if (v[output] === '支出') {
          records.push({
            d: excelDateToText(v[createDate], 'yyyy-MM-dd'),
            p: v[payment],
            t: PromotionType.text2num(v[promotionNote]),
            n: v[promotionNote]
          })
        }
      })
      records.forEach((record, index) => {
        if (record.t === PromotionType.OTHER) {
          throw new Error(`推广第${index + 2}行类型异常`)
        }
      })
      return records
    },
    parsePromotionDetails(results, header) {
      const promotionDate = header[0]
      const goodId = header[1]
      const showNum = header[4]
      const clickNum = header[5]
      const clickRate = header[7]
      const cost = header[6]
      const averageCost = header[8]
      const thousandCost = header[9]
      const dealAmount = header[18]
      const dealNum = header[19]
      const dealCost = header[25]
      const shopCart = header[26]
      const favorites = header[30]
      const roi = header[23]
      return results.map(v => ({
        pd: excelDateToText(v[promotionDate], 'yyyy-MM-dd'),
        id: v[goodId],
        sn: v[showNum] ? v[showNum] : 0,
        cn: v[clickNum] ? v[clickNum] : 0,
        cr: v[clickRate] ? v[clickRate] : 0,
        co: v[cost] ? v[cost] : 0,
        ac: v[averageCost] ? v[averageCost] : 0,
        tc: v[thousandCost] ? v[thousandCost] : 0,
        da: v[dealAmount] ? v[dealAmount] : 0,
        dn: v[dealNum] ? v[dealNum] : 0,
        dc: v[dealCost] ? v[dealCost] : 0,
        sc: v[shopCart] ? v[shopCart] : 0,
        fa: v[favorites] ? v[favorites] : 0,
        roi: v[roi] ? v[roi] : 0
      }))
    },
    parseDeductions(results, header) {
      return parseDeductionRows(results, {
        createTime: header[0],
        financeType: header[4],
        amount: header[6],
        goodName: header[11],
        deductionNote: header[12]
      })
    },
    parsePolymerizes(results, header) {
      const orderId = header[2]
      const financeType = header[3]
      const amount = header[5]
      const createTime = header[0]
      const polymerizeNote = header[7]
      const records = []
      results.forEach((v, index) => {
        const ftype = FinanceType.text2num(v[financeType])
        if (v[amount] > 0 && ftype !== FinanceType.CASH) {
          if (!v[polymerizeNote] || v[polymerizeNote].length < 2) {
            throw new Error(`聚合第${index + 2}行没有备注信息`)
          }
          records.push({
            o: v[orderId],
            f: ftype,
            a: v[amount],
            t: DeductionType.text2num(v[polymerizeNote]),
            c: v[createTime],
            n: v[polymerizeNote]
          })
        }
      })
      records.forEach((record, index) => {
        if (record.t === DeductionType.OTHER || record.o.length !== 19) {
          throw new Error(`聚合第${index + 2}行数据异常`)
        }
      })
      return records
    },
    parseRefunds(results, header) {
      const refundId = header[1]
      const orderId = header[0]
      const productId = header[12]
      const actualPay = header[4]
      const refundPay = header[5]
      const refundPlatform = header[14]
      const refundType = header[11]
      const refundStatus = header[10]
      const payTime = header[2]
      const applyTime = header[8]
      const timeoutTime = header[9]
      const completeTime = header[3]
      const records = results.map(v => ({
        uid: v[refundId],
        oid: v[orderId],
        pid: v[productId],
        ap: v[actualPay],
        rp: v[refundPay],
        rl: v[refundPlatform],
        rt: RefundType.text2num(v[refundType]),
        rs: RefundStatus.text2num(v[refundStatus]),
        pt: v[payTime],
        at: v[applyTime],
        tt: v[timeoutTime] === '' ? NoneTime : v[timeoutTime],
        ct: v[completeTime] === '' ? NoneTime : v[completeTime]
      }))
      records.forEach((record, index) => {
        if (record.rt === RefundType.OTHER || record.rs === RefundStatus.OTHER) {
          throw new Error(`退货第${index + 2}行数据异常`)
        }
      })
      return records
    },
    parseTransfers(results, header) {
      const userName = header[0]
      const payeeName = header[1]
      const orderId = header[7]
      const amount = header[4]
      const createTime = header[5]
      const transferNote = header[9]
      return results.map(v => ({
        n: v[userName],
        p: v[payeeName],
        o: v[orderId],
        a: v[amount],
        c: excelDateToText(v[createTime]),
        tn: v[transferNote]
      }))
    },
    log(message, type = 'info') {
      const line = `[${new Date().toLocaleTimeString()}] ${message}`
      this.processLogs.push({ text: line, type })
      this.$nextTick(() => {
        if (this.$refs.processInfo) {
          this.$refs.processInfo.scrollTop = this.$refs.processInfo.scrollHeight
        }
      })
    },
    getErrorMessage(error) {
      if (!error) {
        return '未知错误'
      }
      if (error.response && error.response.data && error.response.data.msg) {
        return error.response.data.msg
      }
      return error.message || String(error)
    }
  }
}
</script>

<style scoped>
.data-import-page {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 84px);
}

.import-row {
  position: sticky;
  top: 0;
  z-index: 9;
  min-height: 48px;
  padding: 6px 1%;
  margin-bottom: 12px;
  background: #fff;
  border-bottom: 1px solid #d8dce5;
}

.filter-row {
  width: 100%;
  padding: 0 1% 0 1%;
}

.filter-row ::v-deep .el-form-item {
  margin-bottom: 0;
}

.file-upload {
  width: 100%;
  height: 36px;
  line-height: 34px;
  text-align: center;
  cursor: pointer;
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  box-sizing: border-box;
}

.merge-button {
  float: right;
  width: 80px;
}

.init-button {
  float: right;
  width: 80px;
  margin-right: 10px;
}

.clear-button {
  float: right;
  width: 80px;
  margin-right: 10px;
}

.file-upload:hover {
  border-color: #409eff;
}

.file-upload.disabled {
  cursor: not-allowed;
  background: #f5f7fa;
}

.file-upload span {
  font-size: 13px;
  color: #606266;
}

.file-upload em {
  margin-left: 8px;
  color: #409eff;
  font-style: normal;
}

.file-upload input {
  display: none;
}

.progress {
  margin: 0 1% 12px;
}

.process-info {
  flex: 1 1 auto;
  min-height: 0;
  margin-top: 12px;
  padding: 5px 15px;
  overflow: auto;
  color: #606266;
  font-size: 13px;
  line-height: 1.5;
  white-space: pre-wrap;
  background: #fff;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  box-sizing: border-box;
}

.process-placeholder {
  color: #c0c4cc;
}

.process-line {
  margin: 0;
}

.process-line-error {
  color: #f56c6c;
}

.process-line-success {
  color: #67c23a;
}

.process-line-warn {
  color: #e6a23c;
}
</style>
