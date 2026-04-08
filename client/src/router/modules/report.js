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
    path: 'boardReport', component: () => import('@/views/report/boardReport'),
    name: 'middle_boardReport', meta: { title: '业绩大屏', roles: [5001] }
  }, {
    path: 'yearReport', component: () => import('@/views/report/yearReport'),
    name: 'middle_yearReport', meta: { title: '年报汇总', roles: [5002] }
  }, {
    path: 'dayReport', component: () => import('@/views/report/dayReport'),
    name: 'middle_dayReport', meta: { title: '日报汇总', roles: [5003] }
  }, {
    path: 'goodReport', component: () => import('@/views/report/goodReport'),
    name: 'middle_goodReport', meta: { title: '商品汇总', roles: [5004] }
  }, {
    path: 'promotionReport', component: () => import('@/views/report/promotionReport'),
    name: 'middle_promotionReport', meta: { title: '推广汇总', roles: [5005] }
  }, {
    path: 'costReport', component: () => import('@/views/report/costReport'),
    name: 'middle_costReport', meta: { title: '成本汇总', roles: [5006] }
  }, {
    path: 'orderReport', component: () => import('@/views/report/orderReport'),
    name: 'middle_orderReport', meta: { title: '订单汇总', roles: [5007] }
  }, {
    path: 'omissionReport', component: () => import('@/views/report/omissionReport'),
    name: 'middle_omissionReport', meta: { title: '遗漏汇总', roles: [5008] }
  }]
}
