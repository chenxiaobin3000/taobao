import Layout from '@/layout'

export default {
  path: '/original',
  component: Layout,
  name: 'original',
  meta: {
    title: '数据管理',
    roles: [3000]
  },
  children: [{
    path: 'order', component: () => import('@/views/original/order'),
    name: 'original_order', meta: { title: '订单管理', roles: [3001] }
  }, {
    path: 'promotion', component: () => import('@/views/original/promotion'),
    name: 'original_promotion', meta: { title: '推广管理', roles: [3002] }
  }, {
    path: 'promotionDetail', component: () => import('@/views/original/promotionDetail'),
    name: 'original_promotionDetail', meta: { title: '推广明细', roles: [3003] }
  }, {
    path: 'deduction', component: () => import('@/views/original/deduction'),
    name: 'original_deduction', meta: { title: '扣费管理', roles: [3004] }
  }, {
    path: 'deductionDiscard', component: () => import('@/views/original/deductionDiscard'),
    name: 'original_deductionDiscard', meta: { title: '扣费废弃', roles: [3005] }
  }, {
    path: 'polymerize', component: () => import('@/views/original/polymerize'),
    name: 'original_polymerize', meta: { title: '聚合管理', roles: [3006] }
  }, {
    path: 'polymerizeDiscard', component: () => import('@/views/original/polymerizeDiscard'),
    name: 'original_polymerizeDiscard', meta: { title: '聚合废弃', roles: [3007] }
  }, {
    path: 'refund', component: () => import('@/views/original/refund'),
    name: 'original_refund', meta: { title: '退货管理', roles: [3008] }
  }, {
    path: 'transfer', component: () => import('@/views/original/transfer'),
    name: 'original_transfer', meta: { title: '小额打款', roles: [3009] }
  }]
}
