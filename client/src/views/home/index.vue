<template>
  <div class="app-container">
    <component :is="currentRole" />
  </div>
</template>

<script>
import { mapState } from 'vuex'
import companyPage from './components/company.vue'
import userPage from './components/user.vue'

export default {
  components: { companyPage, userPage },
  data() {
    return {
      currentRole: ''
    }
  },
  computed: {
    ...mapState({
      search: state => state.header.search
    })
  },
  watch: {
    search(newVal, oldVal) {
      this.$message({ type: 'error', message: '不支持搜索!' })
    }
  },
  created() {
    const roles = this.$store.getters.roles
    if (roles.includes(10)) {
      this.currentRole = 'companyPage'
    } else {
      this.currentRole = 'userPage'
    }
  }
}
</script>

<style scoped>
.app-container {
  padding: 32px;
  color: #666;
}
</style>
