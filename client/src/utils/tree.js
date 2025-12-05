import path from 'path'

export const treeGenerate = {
  generateRoutes(routes, basePath = '/') {
    const res = []
    for (let route of routes) {
      // skip some route
      if (route.hidden) { continue }

      const onlyOneShowingChild = this.onlyOneShowingChild(route.children, route)
      if (route.children && onlyOneShowingChild && !route.alwaysShow) {
        route = onlyOneShowingChild
      }

      const data = {
        path: path.resolve(basePath, route.path),
        title: route.meta && route.meta.title
      }

      if (route.children) {
        data.children = this.generateRoutes(route.children, data.path)
      }
      res.push(data)
    }
    return res
  },
  generateArr(routes, basePath = '/') {
    let data = []
    routes.forEach(route => {
      const fullPath = path.resolve(basePath, route.path)
      data.push({
        path: fullPath,
        title: route.meta && route.meta.title
      })
      if (route.children) {
        const temp = this.generateArr(route.children, fullPath)
        if (temp.length > 0) {
          data = [...data, ...temp]
        }
      }
    })
    return data
  },
  generateTree(routes, basePath = '/', checkedKeys) {
    const res = []
    for (const route of routes) {
      const routePath = path.resolve(basePath, route.path)
      let sub = false
      if (route.children) {
        const children = this.generateTree(route.children, routePath, checkedKeys)
        if (children && children.length > 0) {
          children.forEach(role => {
            res.push(role)
          })
          sub = true
        }
      }
      if (sub || checkedKeys.includes(routePath)) {
        if (route.meta && route.meta.roles) {
          route.meta.roles.forEach(role => {
            res.push(role)
          })
        }
      }
    }
    return res
  },
  // 若节点只存在一个子节点，就用子节点代替父节点
  onlyOneShowingChild(children = [], parent) {
    let onlyOneChild = null
    const showingChildren = children.filter(item => !item.hidden)

    // When there is only one child route, the child route is displayed by default
    if (showingChildren.length === 1) {
      onlyOneChild = showingChildren[0]
      onlyOneChild.path = path.resolve(parent.path, onlyOneChild.path)
      return onlyOneChild
    }

    // Show parent if there are no child route to display
    if (showingChildren.length === 0) {
      onlyOneChild = { ... parent, path: '', noShowingChildren: true }
      return onlyOneChild
    }
    return false
  },
  // 以下是从store/permision拷贝过来
  hasPermission(roles, route) {
    if (route.meta && route.meta.roles) {
      return roles.some(role => route.meta.roles.includes(role))
    } else {
      return true
    }
  },
  filterAsyncRoutes(routes, roles) {
    const res = []
    routes.forEach(route => {
      const tmp = { ...route }
      if (this.hasPermission(roles, tmp)) {
        if (tmp.children) {
          tmp.children = this.filterAsyncRoutes(tmp.children, roles)
        }
        res.push(tmp)
      }
    })
    return res
  }
}
