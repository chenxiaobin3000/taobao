const getters = {
  sidebar: state => state.app.sidebar,
  size: state => state.app.size,
  device: state => state.app.device,
  visitedViews: state => state.tagsView.visitedViews,
  cachedViews: state => state.tagsView.cachedViews,
  token: state => state.account.token,
  id: state => state.account.id,
  roles: state => state.account.roles,
  userdata: state => state.account.userdata,
  routes: state => state.permission.routes,
  search: state => state.header.search,
  create: state => state.header.create
}
export default getters
