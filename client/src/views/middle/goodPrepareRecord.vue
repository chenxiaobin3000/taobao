<template>
  <div class="app-container">
    <el-form :model="listQuery" label-position="left" label-width="70px" style="width: 100%; padding: 0 1%;">
      <el-row>
        <el-col :span="4">
          <el-form-item label="店铺:">
            <el-select v-model="listQuery.id" class="filter-item" placeholder="请选择店铺" @change="getList">
              <el-option v-for="item in shopList" :key="item.id" :label="item.name" :value="item.id" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="5">
          <el-form-item label="开始日期:" label-width="80px">
            <el-date-picker v-model="listQuery.sdate" type="date" value-format="yyyy-MM-dd" class="filter-item" style="width: 150px;" @change="clearQuickDate" />
          </el-form-item>
        </el-col>
        <el-col :span="5">
          <el-form-item label="结束日期:" label-width="80px">
            <el-date-picker v-model="listQuery.edate" type="date" value-format="yyyy-MM-dd" class="filter-item" style="width: 150px;" @change="clearQuickDate" />
          </el-form-item>
        </el-col>
        <el-col :span="7">
          <div class="quick-date-groups">
            <el-button-group class="quick-date-group">
              <el-button v-for="item in quickDateRow1" :key="item.key" size="mini" class="custom-height-btn" :type="activeQuickDate === item.key ? 'primary' : ''" @click="setQuickDate(item.key)">{{ item.label }}</el-button>
            </el-button-group>
            <el-button-group class="quick-date-group">
              <el-button v-for="item in quickDateRow2" :key="item.key" size="mini" class="custom-height-btn" :type="activeQuickDate === item.key ? 'primary' : ''" @click="setQuickDate(item.key)">{{ item.label }}</el-button>
            </el-button-group>
          </div>
        </el-col>
        <el-col :span="3">
          <el-button type="primary" size="mini" style="float:right;width:60px" @click="getList">查询</el-button>
        </el-col>
      </el-row>
    </el-form>

    <el-table ref="table" v-loading="loading" :data="list" :height="tableHeight" style="width: 100%" border fit highlight-current-row>
      <el-table-column align="center" label="日期" width="110">
        <template slot-scope="scope">{{ scope.row.prepare_date }}</template>
      </el-table-column>
      <el-table-column align="center" label="店铺" width="120">
        <template slot-scope="scope">{{ scope.row.shop_name }}</template>
      </el-table-column>
      <el-table-column align="center" label="上新明细">
        <template slot-scope="scope">{{ scope.row.prepare_detail }}</template>
      </el-table-column>
      <el-table-column align="center" label="收菜日期" width="110">
        <template slot-scope="scope">{{ scope.row.harvest_date }}</template>
      </el-table-column>
      <el-table-column align="center" label="备注">
        <template slot-scope="scope">{{ scope.row.record_note }}</template>
      </el-table-column>
      <el-table-column align="center" label="操作" width="150">
        <template slot-scope="{row}">
          <el-button type="primary" size="mini" @click="handleUpdate(row)">编辑</el-button>
          <el-button type="danger" size="mini" @click="handleClear(row)">清空</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog title="编辑上新记录" :visible.sync="dialogVisible">
      <el-form :model="temp" label-position="left" label-width="80px" style="width: 100%; padding: 0 4%;">
        <el-form-item label="日期">
          <el-date-picker v-model="temp.prepare_date" type="date" value-format="yyyy-MM-dd" class="filter-item" style="width: 150px;" disabled />
        </el-form-item>
        <el-form-item label="店铺">
          <el-select v-model="temp.shop_ids" multiple class="filter-item" placeholder="请选择店铺" style="width: 100%;">
            <el-option v-for="item in editShopList" :key="item.id" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="上新明细">
          <el-input v-model="temp.prepare_detail" maxlength="20" show-word-limit />
        </el-form-item>
        <el-form-item label="收菜日期">
          <el-date-picker v-model="temp.harvest_date" type="date" value-format="yyyy-MM-dd" class="filter-item" style="width: 150px;" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="temp.record_note" maxlength="20" show-word-limit />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="updateData">确定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import { getOwnShopList } from '@/api/system/shop'
import { clearGoodPrepareRecord, getGoodPrepareRecordList, setGoodPrepareRecord } from '@/api/middle/goodPrepareRecord'

export default {
  data() {
    return {
      userdata: {},
      tableHeight: 600,
      list: [],
      loading: false,
      dialogVisible: false,
      shopList: [],
      ownShopList: [],
      activeQuickDate: '',
      quickDateRow1: [
        { key: 'currentYear', label: '本年' },
        { key: 'lastMonth', label: '上月' },
        { key: 'currentMonth', label: '本月' },
        { key: 'lastWeek', label: '上周' },
        { key: 'currentWeek', label: '本周' },
        { key: 'yesterday', label: '昨天' }
      ],
      quickDateRow2: [
        { key: 'days90', label: '90天' },
        { key: 'days30', label: '30天' },
        { key: 'days14', label: '14天' },
        { key: 'days7', label: '7天' },
        { key: 'days3', label: '3天' },
        { key: 'today', label: '今天' }
      ],
      listQuery: {
        id: 0,
        sdate: '',
        edate: ''
      },
      temp: {}
    }
  },
  computed: {
    ...mapState({
      search: state => state.header.search
    }),
    editShopList() {
      if (this.listQuery.id) {
        return this.ownShopList.filter(item => item.id === this.listQuery.id)
      }
      return this.ownShopList
    }
  },
  watch: {
    search() {
      this.$message({ type: 'error', message: '不支持搜索' })
    }
  },
  created() {
    this.userdata = this.$store.getters.userdata
    const endDate = new Date()
    const startDate = this.addDays(endDate, -29)
    this.listQuery.sdate = this.formatDate(startDate)
    this.listQuery.edate = this.formatDate(endDate)
    this.getOwnShopList()
  },
  mounted() {
    setTimeout(() => {
      if (this.$refs.table) {
        this.tableHeight = window.innerHeight - this.$refs.table.$el.offsetTop - 20
      }
    }, 1000)
  },
  methods: {
    getOwnShopList() {
      getOwnShopList({
        id: this.userdata.company.id,
        uid: this.userdata.user.id
      }).then(response => {
        this.ownShopList = response.data.data || []
        this.shopList = [{ id: 0, name: '全部' }].concat(this.ownShopList)
        this.getList()
      })
    },
    getList() {
      this.loading = true
      getGoodPrepareRecordList(this.listQuery).then(response => {
        this.list = response.data.data.list || []
      }).finally(() => {
        this.loading = false
      })
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row)
      if (!this.temp.shop_ids || !this.temp.shop_ids.length) {
        this.temp.shop_ids = this.listQuery.id ? [this.listQuery.id] : []
      }
      this.temp.prepare_detail = row.edit_prepare_detail || row.prepare_detail || ''
      this.temp.harvest_date = row.edit_harvest_date || row.harvest_date || ''
      this.temp.record_note = row.edit_record_note || row.record_note || ''
      this.dialogVisible = true
    },
    updateData() {
      setGoodPrepareRecord({
        ids: this.temp.shop_ids,
        cdate: this.temp.prepare_date,
        detail: this.temp.prepare_detail,
        hdate: this.temp.harvest_date,
        note: this.temp.record_note
      }).then(() => {
        this.dialogVisible = false
        this.$message({ type: 'success', message: '保存成功' })
        this.getList()
      })
    },
    handleClear(row) {
      this.$confirm('确定要清空吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        clearGoodPrepareRecord({
          ids: row.shop_ids,
          cdate: row.prepare_date
        }).then(() => {
          this.$message({ type: 'success', message: '清空成功' })
          this.getList()
        })
      })
    },
    setQuickDate(type) {
      const today = new Date()
      today.setHours(0, 0, 0, 0)
      let startDate = new Date(today)
      let endDate = new Date(today)

      if (type === 'currentYear') {
        startDate = new Date(today.getFullYear(), 0, 1)
      } else if (type === 'lastMonth') {
        startDate = new Date(today.getFullYear(), today.getMonth() - 1, 1)
        endDate = this.addDays(new Date(today.getFullYear(), today.getMonth(), 1), -1)
      } else if (type === 'currentMonth') {
        startDate = new Date(today.getFullYear(), today.getMonth(), 1)
      } else if (type === 'lastWeek') {
        const currentMonday = this.getMonday(today)
        startDate = this.addDays(currentMonday, -7)
        endDate = this.addDays(currentMonday, -1)
      } else if (type === 'currentWeek') {
        startDate = this.getMonday(today)
      } else if (type === 'yesterday') {
        startDate = this.addDays(today, -1)
        endDate = startDate
      } else if (type.indexOf('days') === 0) {
        const days = Number(type.replace('days', ''))
        startDate = this.addDays(today, -(days - 1))
      }

      this.listQuery.sdate = this.formatDate(startDate)
      this.listQuery.edate = this.formatDate(endDate)
      this.activeQuickDate = type
      this.getList()
    },
    getMonday(date) {
      const day = date.getDay() || 7
      return this.addDays(date, 1 - day)
    },
    addDays(date, days) {
      const result = new Date(date)
      result.setDate(result.getDate() + days)
      return result
    },
    clearQuickDate() {
      this.activeQuickDate = ''
    },
    formatDate(date) {
      const year = date.getFullYear()
      const month = `${date.getMonth() + 1}`.padStart(2, '0')
      const day = `${date.getDate()}`.padStart(2, '0')
      return `${year}-${month}-${day}`
    }
  }
}
</script>

<style scoped>
.quick-date-groups {
  height: 28px;
}

.quick-date-group {
  display: flex;
  width: auto;
  height: 14px;
}

.custom-height-btn {
  flex: none;
  box-sizing: border-box;
  width: 38px;
  height: 14px;
  padding: 0;
  font-size: 10px;
  line-height: 12px;
}
</style>
