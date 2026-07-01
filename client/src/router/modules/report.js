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
    name: 'report_boardReport', meta: { title: '业绩大屏', roles: [5001] }
  }, {
    path: 'yearReport', component: () => import('@/views/report/yearReport'),
    name: 'report_yearReport', meta: { title: '年报汇总', roles: [5002] }
  }, {
    path: 'dayReport', component: () => import('@/views/report/dayReport'),
    name: 'report_dayReport', meta: { title: '日报汇总', roles: [5003] }
  }, {
    path: 'promotionReport', component: () => import('@/views/report/promotionReport'),
    name: 'report_promotionReport', meta: { title: '推广汇总', roles: [5005] }
  }, {
    path: 'goodReport', component: () => import('@/views/report/goodReport'),
    name: 'report_goodReport', meta: { title: '商品汇总', roles: [5004] }
  }, {
    path: 'goodRadar', component: () => import('@/views/report/goodRadar'),
    name: 'report_goodRadar', meta: { title: '商品雷达', roles: [5006] }
  }, {
    path: 'recentTransaction', component: () => import('@/views/report/recentTransaction'),
    name: 'report_recentTransaction', meta: { title: '成交汇总', roles: [5012] }
  }, {
    path: 'orderReport', component: () => import('@/views/report/orderReport'),
    name: 'report_orderReport', meta: { title: '订单汇总', roles: [5007] }
  }, {
    path: 'omissionReport', component: () => import('@/views/report/omissionReport'),
    name: 'report_omissionReport', meta: { title: '遗漏汇总', roles: [5008] }
  }, {
    path: 'purchaseReport', component: () => import('@/views/report/purchaseReport'),
    name: 'report_purchaseReport', meta: { title: '采购汇总', roles: [5009] }
  }, {
    path: 'costReport', component: () => import('@/views/report/costReport'),
    name: 'report_costReport', meta: { title: '成本汇总', roles: [5011] }
  }, {
    path: 'taxReport', component: () => import('@/views/report/taxReport'),
    name: 'report_taxReport', meta: { title: '报税汇总', roles: [5010] }
  }]
}
