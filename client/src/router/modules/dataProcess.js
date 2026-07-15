import Layout from '@/layout'

export default {
  path: '/dataProcess',
  component: Layout,
  name: 'dataProcess',
  meta: {
    title: '数据处理',
    roles: [7000]
  },
  children: [{
    path: 'orderSummary', component: () => import('@/views/middle/orderSummary'),
    name: 'dataProcess_orderSummary', meta: { title: '订单管理', roles: [7001] }
  }, {
    path: 'fakeSummary', component: () => import('@/views/middle/fakeSummary'),
    name: 'dataProcess_fakeSummary', meta: { title: '刷单管理', roles: [7002] }
  }, {
    path: 'deductionSummary', component: () => import('@/views/middle/deductionSummary'),
    name: 'dataProcess_deductionSummary', meta: { title: '扣款管理', roles: [7003] }
  }]
}
