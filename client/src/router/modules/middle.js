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
    path: 'fake', component: () => import('@/views/middle/fake'),
    name: 'middle_fake', meta: { title: '刷单管理', roles: [4002] }
  }]
}
