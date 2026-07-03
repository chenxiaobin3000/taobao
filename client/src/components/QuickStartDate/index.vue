<template>
  <el-button-group class="quick-start-date">
    <el-button v-for="item in buttons" :key="item.key" size="mini" class="quick-start-date-button" :type="active === item.key ? 'primary' : ''" @click="select(item)">{{ item.label }}</el-button>
  </el-button-group>
</template>

<script>
export default {
  props: {
    value: {
      type: [String, Number, Date],
      default: ''
    }
  },
  data() {
    return {
      active: '',
      updating: false,
      buttons: [
        { key: 'currentYear', label: '本年' },
        { key: 'days180', label: '180天', days: 180 },
        { key: 'days90', label: '90天', days: 90 },
        { key: 'days30', label: '30天', days: 30 },
        { key: 'days14', label: '14天', days: 14 },
        { key: 'days7', label: '7天', days: 7 }
      ]
    }
  },
  watch: {
    value() {
      if (!this.updating) this.active = ''
    }
  },
  methods: {
    select(item) {
      const today = new Date()
      today.setHours(0, 0, 0, 0)
      const startDate = item.key === 'currentYear'
        ? new Date(today.getFullYear(), 0, 1)
        : this.addDays(today, -(item.days - 1))
      this.active = item.key
      this.updating = true
      this.$emit('input', this.formatDate(startDate))
      this.$nextTick(() => {
        this.updating = false
      })
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
.quick-start-date {
  display: flex;
  width: auto;
  height: 28px;
}

.quick-start-date-button {
  flex: none;
  box-sizing: border-box;
  width: 38px;
  height: 28px;
  padding: 0;
  font-size: 10px;
  line-height: 26px;
}
</style>
