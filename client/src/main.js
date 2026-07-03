import Vue from 'vue'

import Cookies from 'js-cookie'

import 'normalize.css/normalize.css' // a modern alternative to CSS resets

import Element from 'element-ui'
import './styles/element-variables.scss'

import '@/styles/index.scss' // global css

import App from './App'
import QuickDate from '@/components/QuickDate'
import QuickStartDate from '@/components/QuickStartDate'
import store from './store'
import router from './router'

import './icons' // icon
import './permission' // permission control

import * as filters from './filters' // global filters

Vue.component('QuickDate', QuickDate)
Vue.component('QuickStartDate', QuickStartDate)

Vue.use(Element, {
  size: Cookies.get('size') || 'mini' // set element-ui default size: medium
})

Vue.mixin({
  mounted() {
    this.__bindTableLayout()
  },
  updated() {
    this.__refreshTableLayout()
  },
  activated() {
    this.__refreshTableLayout()
  },
  beforeDestroy() {
    if (this.__tableLayoutResizeHandler) {
      window.removeEventListener('resize', this.__tableLayoutResizeHandler)
    }
  },
  methods: {
    __getTableRef() {
      if (!this.$refs || !this.$refs.table) {
        return null
      }
      return Array.isArray(this.$refs.table) ? this.$refs.table[0] : this.$refs.table
    },
    __hasTableHeight() {
      return this.$data && Object.prototype.hasOwnProperty.call(this.$data, 'tableHeight')
    },
    __bindTableLayout() {
      if (!this.__hasTableHeight()) {
        return
      }
      this.__tableLayoutResizeHandler = () => this.__refreshTableLayout()
      window.addEventListener('resize', this.__tableLayoutResizeHandler)
      this.__refreshTableLayout()
    },
    __refreshTableLayout() {
      if (!this.__hasTableHeight()) {
        return
      }
      this.$nextTick(() => {
        const table = this.__getTableRef()
        if (!table || !table.$el) {
          return
        }
        if (this.tableHeight !== 600 && this.__tableHeightBottomOffset === undefined) {
          this.__tableHeightBottomOffset = window.innerHeight - table.$el.offsetTop - this.tableHeight
        }
        if (this.__tableHeightBottomOffset !== undefined) {
          this.tableHeight = window.innerHeight - table.$el.offsetTop - this.__tableHeightBottomOffset
        }
        if (table.doLayout) {
          table.doLayout()
        }
      })
    }
  }
})

// register global utility filters
Object.keys(filters).forEach(key => {
  Vue.filter(key, filters[key])
})

Vue.config.productionTip = false

new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
})
