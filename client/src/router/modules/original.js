import Layout from '@/layout'

export default {
  path: '/original',
  component: Layout,
  name: 'original',
  meta: {
    title: '数据填报',
    roles: [2000]
  },
  children: [{
    path: 'order', component: () => import('@/views/original/order'),
    name: 'original_order', meta: { title: '订单管理', roles: [2001] }
  }, {
    path: 'promotion', component: () => import('@/views/original/promotion'),
    name: 'original_promotion', meta: { title: '推广管理', roles: [2002] }/*
  }, {
    path: 'promotionDetail', component: () => import('@/views/original/promotionDetail'),
    name: 'original_promotionDetail', meta: { title: '推广明细', roles: [2003] }
  }, {
    path: 'zhifubao', component: () => import('@/views/original/zhifubao'),
    name: 'original_zhifubao', meta: { title: '支付宝', roles: [2004] }
  }, {
    path: 'weixin', component: () => import('@/views/original/weixin'),
    name: 'original_weixin', meta: { title: '微信支付', roles: [2005] }
  }, {
    path: 'refund', component: () => import('@/views/original/refund'),
    name: 'original_refund', meta: { title: '退货管理', roles: [2006] }
  }, {
    path: 'transfer', component: () => import('@/views/original/transfer'),
    name: 'original_transfer', meta: { title: '小额打款', roles: [2007] }*/
  }]
}
