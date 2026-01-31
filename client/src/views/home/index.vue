<template>
  <div class="app-container">
    <component :is="currentRole" />
  </div>
</template>

<script>
import { mapState } from 'vuex'
import companyPage from './components/company.vue'
import systemPage from './components/system.vue'
import userPage from './components/user.vue'

export default {
  components: { companyPage, systemPage, userPage },
  data() {
    return {
      currentRole: ''
    }
  },
  computed: {
    ...mapState({
      search: state => state.header.search,
      create: state => state.header.create
    })
  },
  watch: {
    search(newVal, oldVal) {
      this.$message({ type: 'error', message: '不支持搜索!' })
    },
    create() {
      this.$message({ type: 'error', message: '不支持新建!' })
    }
  },
  created() {
    const roles = this.$store.getters.roles
    if (roles.includes(20)) {
      this.currentRole = 'systemPage'
    } else if (roles.includes(10)) {
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
