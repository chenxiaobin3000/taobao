<template>
  <component :is="currentRole" />
</template>

<script>
import { mapGetters } from 'vuex'
import reportPage from './components/report.vue'
import superPage from './components/super.vue'
import userInfoPage from './components/userInfo.vue'

export default {
  components: { reportPage, superPage, userInfoPage },
  data() {
    return {
      currentRole: 'userInfoPage'
    }
  },
  computed: {
    ...mapGetters([
      'roles'
    ])
  },
  created() {
    if (this.roles.includes(100)) {
      this.currentRole = 'reportPage'
    } else if (this.roles.includes(101)) {
      this.currentRole = 'superPage'
    }
  }
}
</script>
