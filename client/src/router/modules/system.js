import Layout from '@/layout'

export default {
  path: '/system',
  component: Layout,
  name: 'system',
  meta: {
    title: '系统功能',
    roles: [1000]
  },
  children: [{
    path: 'setPassword', component: () => import('@/views/system/setPassword'),
    name: 'system_setPassword', meta: { title: '修改密码', roles: [1001] }
  }]
}
