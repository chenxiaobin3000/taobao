import Layout from '@/layout'

export default {
  path: '/middle',
  component: Layout,
  name: 'middle',
  meta: {
    title: '辅助工具',
    roles: [6000]
  },
  children: [{
    path: 'miscellaneous', component: () => import('@/views/middle/miscellaneous'),
    name: 'middle_miscellaneous', meta: { title: '杂项管理', roles: [6001] }
  }, {
    path: 'orderSummary', component: () => import('@/views/middle/orderSummary'),
    name: 'middle_orderSummary', meta: { title: '订单管理', roles: [6002] }
  }, {
    path: 'fakeSummary', component: () => import('@/views/middle/fakeSummary'),
    name: 'middle_fakeSummary', meta: { title: '刷单管理', roles: [6003] }
  }, {
    path: 'deductionSummary', component: () => import('@/views/middle/deductionSummary'),
    name: 'middle_deductionSummary', meta: { title: '扣款管理', roles: [6004] }
  }, {
    path: 'goodPrepare', component: () => import('@/views/middle/goodPrepare'),
    name: 'middle_goodPrepare', meta: { title: '上新商品', roles: [6005] }
  }, {
    path: 'receiptItem', component: () => import('@/views/middle/receiptManager'),
    name: 'middle_receiptItem', meta: { title: '发票管理', roles: [6006] }
  }, {
    path: 'receiptFrom', component: () => import('@/views/middle/receiptFrom'),
    name: 'middle_receiptFrom', meta: { title: '进项管理', roles: [6007] }
  }, {
    path: 'receiptTo', component: () => import('@/views/middle/receiptTo'),
    name: 'middle_receiptTo', meta: { title: '出项管理', roles: [6008] }
  }]
}
