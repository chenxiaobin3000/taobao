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
    name: 'system_setPassword', meta: { title: '修改密码', roles: [1005] }
  }, {
    path: 'storage', component: () => import('@/views/system/storage'),
    name: 'system_storage', meta: { title: '仓库管理', roles: [1006] }
  }, {
    path: 'department', component: () => import('@/views/system/department'),
    name: 'system_department', meta: { title: '部门管理', roles: [1002] }
  }, {
    path: 'roleList', component: () => import('@/views/system/roleList'),
    name: 'system_roleList', meta: { title: '角色管理', roles: [1003] }
  }, {
    path: 'userList', component: () => import('@/views/system/userList'),
    name: 'system_userList', meta: { title: '用户管理', roles: [1004] }
  }, {
    path: 'resetPwd', component: () => import('@/views/system/resetPwd'),
    name: 'system_resetPwd', meta: { title: '重置密码', roles: [1001] }
  }]
}
