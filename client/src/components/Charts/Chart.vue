<template>
  <div :id="id" :class="className" :style="{height:height,width:width}" />
</template>

<script>
import echarts from 'echarts'
import resize from './mixins/resize'

export default {
  mixins: [resize],
  props: {
    className: {
      type: String,
      default: 'chart'
    },
    id: {
      type: String,
      default: 'chart'
    },
    width: {
      type: String,
      default: '200px'
    },
    height: {
      type: String,
      default: '200px'
    },
    labels: {
      type: Array,
      default: () => []
    },
    xdata: {
      type: Array,
      default: () => []
    },
    tdata: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      chart: null
    }
  },
  watch: {
    tdata() {
      this.destroy()
      this.initChart()
    }
  },
  beforeDestroy() {
    this.destroy()
  },
  methods: {
    initChart() {
      this.chart = echarts.init(document.getElementById(this.id))
      this.chart.setOption({
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross',
            textStyle: { color: '#fff' }
          }
        },
        grid: {
          left: '5%',
          right: '5%',
          top: 50,
          bottom: 30,
          borderWidth: 0,
          textStyle: { color: '#fff' }
        },
        legend: {
          x: '1%',
          top: '2',
          textStyle: { color: '#90979c' },
          data: this.labels
        },
        xAxis: [{
          type: 'category',
          axisLine: {
            lineStyle: {
              color: '#90979c'
            }
          },
          data: this.xdata
        }],
        yAxis: [{
          type: 'value',
          minInterval: 1,
          splitLine: { show: false },
          axisLine: {
            lineStyle: {
              color: '#90979c'
            }
          }
        }, {
          type: 'value',
          minInterval: 1,
          splitLine: { show: false },
          axisLine: {
            lineStyle: {
              color: '#90979c'
            }
          }
        }],
        series: this.createDate(this.tdata)
      })
    },
    createDate(list) {
      const ret = []
      const size = list.length
      for (let i = 0; i < size; i++) {
        ret.push({
          name: list[i].name,
          type: list[i].type,
          symbolSize: 10,
          data: list[i].data,
          yAxisIndex: list[i].yAxisIndex,
          itemStyle: {
            normal: {
              color: list[i].color,
              label: {
                show: false,
                position: 'top',
                formatter(p) {
                  return p.value > 0 ? p.value : ''
                }
              }
            }
          }
        })
      }
      return ret
    },
    destroy() {
      if (!this.chart) {
        return
      }
      this.chart.dispose()
      this.chart = null
    }
  }
}
</script>
