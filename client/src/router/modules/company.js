import Layout from '@/layout'

export default {
  path: '/company',
  component: Layout,
  name: 'company',
  meta: {
    title: '公司数据',
    roles: [2000]
  },
  children: [{
    path: 'company', component: () => import('@/views/company/company'),
    name: 'company_company', meta: { title: '公司信息', roles: [2001] }
  }, {
    path: 'shopList', component: () => import('@/views/company/shopList'),
    name: 'company_shopList', meta: { title: '店铺管理', roles: [2002] }
  }, {
    path: 'goodList', component: () => import('@/views/company/goodList'),
    name: 'company_goodList', meta: { title: '商品管理', roles: [2003] }
  }, {
    path: 'userList', component: () => import('@/views/company/userList'),
    name: 'company_userList', meta: { title: '用户管理', roles: [2004] }
  }, {
    path: 'roleList', component: () => import('@/views/company/roleList'),
    name: 'company_roleList', meta: { title: '角色管理', roles: [2005] }
  }, {
    path: 'resetPwd', component: () => import('@/views/company/resetPwd'),
    name: 'company_resetPwd', meta: { title: '重置密码', roles: [2006] }
  }]
}
