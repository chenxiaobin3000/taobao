<template>
  <div class="app-container">
    <br>
    <span class="firstLine">{{ userdata.user.name }} ( {{ userdata.group.name }} ) :</span>
    <br><br>
    <span class="secondLine">超级管理员，您好！超管的权限很大，请谨慎操作！</span>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  data() {
    return {
      userdata: {}
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
    this.userdata = this.$store.getters.userdata
  }
}
</script>

<style scoped>
.app-container {
  padding: 32px;
  color: #666;
}

.firstLine {
  padding-left: 2%;
}

.secondLine {
  padding-left: 7%;
}
</style>
