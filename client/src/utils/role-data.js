export const MyRoleData = [{
  path: '/', meta: { title: '首页报表', roles: [100] }
}, {
  path: '/system', meta: { title: '系统管理', roles: [1000] },
  children: [{
    path: 'setPassword', meta: { title: '修改密码', roles: [1005] }
  }, {
    path: 'storage', meta: { title: '仓库管理', roles: [1006] }
  }, {
    path: 'department', meta: { title: '部门管理', roles: [1002] }
  }, {
    path: 'roleList', meta: { title: '角色管理', roles: [1003] }
  }, {
    path: 'userList', meta: { title: '用户管理', roles: [1004] }
  }, {
    path: 'resetPwd', meta: { title: '重置密码', roles: [1001] }
  }]
}]
