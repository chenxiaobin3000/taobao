<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App',
  onBeforeUnmount() {
    // 必须手动注销监听
    window.removeEventListener('beforeunload', this.beforeunloadHandler)
  },
  created() {
    // 监听刷新事件
    window.addEventListener('beforeunload', this.beforeunloadHandler)

    // 初始化页面时读取数据
    const store = JSON.parse(sessionStorage.getItem('store'))
    if (store) {
      this.$store.commit('header/SET_HEADER_SHOP', store.shop)
    }
  },
  methods: {
    beforeunloadHandler() {
      // 页面刷新之前保存数据
      if (this.$store.getters.shop > 0) {
        sessionStorage.setItem('store', JSON.stringify({
          shop: this.$store.getters.shop
        }))
      }
    }
  }
}
</script>
