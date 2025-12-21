<template>
  <div class="app-container">
    
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  components: { },
  data() {
    return {
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
      this.listQuery.search = newVal
    },
    create() {
      this.$message({ type: 'error', message: '不支持新建!' })
    }
  },
  mounted: function() {
  },
  created() {
    
  },
  methods: {
    
  }
}
</script>
