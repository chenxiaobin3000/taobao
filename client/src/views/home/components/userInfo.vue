<template>
  <div class="app-container">
    <br>
    <span class="firstLine">你好，来自 ‘{{ userdata.company.name }}’ 的 {{ userdata.user.name }}！</span>
    <br><br>
    <span class="secondLine">已授权的平台: </span>
    <li v-for="data in userdata.market" :key="data.id" class="secondContext">
      <span class="secondLine">{{ data.name }}</span>
    </li>
    <br><br>
    <span class="secondLine">管理中的店铺: </span>
    <li v-for="data in userdata.shop" :key="data.id" class="secondContext">
      <span class="secondLine">{{ data.name }}</span>
    </li>
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
  padding-left: 2%;
}

.secondContext {
  padding-left: 2%;
  list-style: none;
}
</style>
