<template>
  <div class="quick-date-groups">
    <el-button-group v-for="(row, index) in rows" :key="index" class="quick-date-group">
      <el-button v-for="item in row" :key="item.key" size="mini" class="quick-date-button" :type="active === item.key ? 'primary' : ''" @click="select(item.key)">{{ item.label }}</el-button>
    </el-button-group>
  </div>
</template>

<script>
export default {
  props: {
    query: {
      type: Object,
      default: null
    },
    inclusiveEnd: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      active: '',
      updating: false,
      rows: [
        [
          { key: 'currentYear', label: '本年' },
          { key: 'lastMonth', label: '上月' },
          { key: 'currentMonth', label: '本月' },
          { key: 'lastWeek', label: '上周' },
          { key: 'currentWeek', label: '本周' },
          { key: 'yesterday', label: '昨天' }
        ],
        [
          { key: 'days90', label: '90天' },
          { key: 'days30', label: '30天' },
          { key: 'days14', label: '14天' },
          { key: 'days7', label: '7天' },
          { key: 'days3', label: '3天' },
          { key: 'today', label: '今天' }
        ]
      ]
    }
  },
  watch: {
    'query.sdate'() {
      if (!this.updating) this.clear()
    },
    'query.edate'() {
      if (!this.updating) this.clear()
    }
  },
  methods: {
    select(type) {
      const today = new Date()
      today.setHours(0, 0, 0, 0)
      let startDate = new Date(today)
      let endDate = this.inclusiveEnd ? new Date(today) : this.addDays(today, 1)

      if (type === 'currentYear') {
        startDate = new Date(today.getFullYear(), 0, 1)
      } else if (type === 'lastMonth') {
        startDate = new Date(today.getFullYear(), today.getMonth() - 1, 1)
        endDate = new Date(today.getFullYear(), today.getMonth(), 1)
        if (this.inclusiveEnd) endDate = this.addDays(endDate, -1)
      } else if (type === 'currentMonth') {
        startDate = new Date(today.getFullYear(), today.getMonth(), 1)
      } else if (type === 'lastWeek') {
        const currentMonday = this.getMonday(today)
        startDate = this.addDays(currentMonday, -7)
        endDate = this.inclusiveEnd ? this.addDays(currentMonday, -1) : currentMonday
      } else if (type === 'currentWeek') {
        startDate = this.getMonday(today)
      } else if (type === 'yesterday') {
        startDate = this.addDays(today, -1)
        endDate = this.inclusiveEnd ? startDate : today
      } else if (type.indexOf('days') === 0) {
        startDate = this.addDays(today, -(Number(type.replace('days', '')) - 1))
      }

      this.active = type
      const range = {
        sdate: this.formatDate(startDate),
        edate: this.formatDate(endDate)
      }
      if (this.query) {
        this.updating = true
        this.$set(this.query, 'sdate', range.sdate)
        this.$set(this.query, 'edate', range.edate)
        this.$nextTick(() => {
          this.updating = false
        })
      }
      this.$emit('change', range)
    },
    clear() {
      this.active = ''
    },
    getMonday(date) {
      return this.addDays(date, 1 - (date.getDay() || 7))
    },
    addDays(date, days) {
      const result = new Date(date)
      result.setDate(result.getDate() + days)
      return result
    },
    formatDate(date) {
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
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

.quick-date-button {
  flex: none;
  box-sizing: border-box;
  width: 38px;
  height: 14px;
  padding: 0;
  font-size: 10px;
  line-height: 12px;
}
</style>
