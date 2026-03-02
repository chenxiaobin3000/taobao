import Layout from '@/layout'

export default {
  path: '/report',
  component: Layout,
  name: 'report',
  meta: {
    title: '统计报表',
    roles: [5000]
  },
  children: [{
    path: 'yearReport', component: () => import('@/views/report/yearReport'),
    name: 'middle_yearReport', meta: { title: '年报汇总', roles: [5001] }
  }, {
    path: 'dayReport', component: () => import('@/views/report/dayReport'),
    name: 'middle_dayReport', meta: { title: '日报汇总', roles: [5002] }
  }, {
    path: 'goodReport', component: () => import('@/views/report/goodReport'),
    name: 'middle_goodReport', meta: { title: '商品汇总', roles: [5003] }
  }, {
    path: 'goodRadar', component: () => import('@/views/report/goodRadar'),
    name: 'middle_goodRadar', meta: { title: '商品雷达', roles: [5004] }
  }, {
    path: 'costReport', component: () => import('@/views/report/costReport'),
    name: 'middle_costReport', meta: { title: '成本汇总', roles: [5005] }
  }, {
    path: 'fakeReport', component: () => import('@/views/report/fakeReport'),
    name: 'middle_fakeReport', meta: { title: '刷单汇总', roles: [5006] }
  }, {
    path: 'orderReport', component: () => import('@/views/report/orderReport'),
    name: 'middle_orderReport', meta: { title: '订单汇总', roles: [5007] }
  }]
}
