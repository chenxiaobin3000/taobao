import Layout from '@/layout'

export default {
  path: '/trunk',
  component: Layout,
  name: 'trunk',
  meta: {
    title: '存档数据',
    roles: [4000]
  },
  children: [{
    path: 'order', component: () => import('@/views/trunk/order'),
    name: 'trunk_order', meta: { title: '订单管理', roles: [4001] }
  }, {
    path: 'fake', component: () => import('@/views/trunk/fake'),
    name: 'trunk_fake', meta: { title: '刷单管理', roles: [4002] }
  }, {
    path: 'promotion', component: () => import('@/views/trunk/promotion'),
    name: 'trunk_promotion', meta: { title: '推广管理', roles: [4003] }
  }, {
    path: 'promotionDetail', component: () => import('@/views/trunk/promotionDetail'),
    name: 'trunk_promotionDetail', meta: { title: '推广明细', roles: [4004] }
  }, {
    path: 'deduction', component: () => import('@/views/trunk/deduction'),
    name: 'trunk_deduction', meta: { title: '扣费管理', roles: [4005] }
  }, {
    path: 'polymerize', component: () => import('@/views/trunk/polymerize'),
    name: 'trunk_polymerize', meta: { title: '聚合管理', roles: [4007] }
  }, {
    path: 'refund', component: () => import('@/views/trunk/refund'),
    name: 'trunk_refund', meta: { title: '退货管理', roles: [4009] }
  }, {
    path: 'transfer', component: () => import('@/views/trunk/transfer'),
    name: 'trunk_transfer', meta: { title: '小额打款', roles: [4010] }
  }]
}
