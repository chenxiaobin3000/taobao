import Layout from '@/layout'

export default {
  path: '/middle',
  component: Layout,
  name: 'middle',
  meta: {
    title: '辅助管理',
    roles: [4000]
  },
  children: [{
    path: 'miscellaneous', component: () => import('@/views/middle/miscellaneous'),
    name: 'middle_miscellaneous', meta: { title: '杂项管理', roles: [4001] }
  }, {
    path: 'fakeSummary', component: () => import('@/views/middle/fakeSummary'),
    name: 'middle_fakeSummary', meta: { title: '刷单管理', roles: [4002] }
  }, {
    path: 'deductionSummary', component: () => import('@/views/middle/deductionSummary'),
    name: 'middle_deductionSummary', meta: { title: '扣款管理', roles: [4003] }
  }]
}
