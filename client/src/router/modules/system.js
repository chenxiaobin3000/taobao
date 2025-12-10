import Layout from '@/layout'

export default {
  path: '/system',
  component: Layout,
  name: 'system',
  meta: {
    title: '系统管理',
    roles: [1000]
  },
  children: [{
    path: 'setPassword', component: () => import('@/views/system/setPassword'),
    name: 'system_setPassword', meta: { title: '修改密码', roles: [1003] }
  }, {
    path: 'userList', component: () => import('@/views/system/userList'),
    name: 'system_userList', meta: { title: '用户管理', roles: [1002] }
  }, {
    path: 'resetPwd', component: () => import('@/views/system/resetPwd'),
    name: 'system_resetPwd', meta: { title: '重置密码', roles: [1001] }
  }]
}
