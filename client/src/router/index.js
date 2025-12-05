import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/* Router Modules */
//import agreementRouter from './modules/agreement'
//import commodityRouter from './modules/commodity'
//import financeRouter from './modules/finance'
//import marketRouter from './modules/market'
//import offlineRouter from './modules/offline'
//import productRouter from './modules/product'
//import purchaseRouter from './modules/purchase'
//import reportRouter from './modules/report'
//import storageRouter from './modules/storage'
//import superRouter from './modules/super'
import systemRouter from './modules/system'
//import transportRouter from './modules/transport'

/**
 * Note: sub-menu only appear when route children.length >= 1
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'/'el-icon-x' the icon show in the sidebar
    noCache: true                if set true, the page will no be cached(default is false)
    affix: true                  if set true, the tag will affix in the tags-view
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [{
  path: '/login', hidden: true,
  component: () => import('@/views/home/login')
}, {
  path: '/404', hidden: true,
  component: () => import('@/views/error/index')
}]

/**
 * asyncRoutes
 * the routes that need to be dynamically loaded based on user roles
 */
export const asyncRoutes = [
  {
    path: '/',
    component: Layout,
    redirect: '/home',
    children: [{
      path: 'home', component: () => import('@/views/home/index'),
      name: 'home', meta: { title: '首页' }
    }]
  },

  /** when your routing map is too long, you can split it into small modules **/
  /*marketRouter,
  offlineRouter,
  purchaseRouter,
  storageRouter,
  productRouter,
  agreementRouter,
  transportRouter,
  reportRouter,
  commodityRouter,
  financeRouter,
  userRouter,*/
  systemRouter,

  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
