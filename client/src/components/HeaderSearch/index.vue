<template>
  <div class="header-search">
    <el-input v-model="search" placeholder="请输入想查询的内容" class="header-search-input" @keyup.enter.native="handleSearch" />
    <svg-icon icon-class="search" class="header-search-button" @click.stop="handleSearch" />
  </div>
</template>

<script>
export default {
  name: 'HeaderSearch',
  data() {
    return {
      search: ''
    }
  },
  methods: {
    handleSearch() {
      this.$store.dispatch('header/search', this.search)
    }
  }
}
</script>

<style lang="scss" scoped>
.header-search {
  font-size: 0 !important;

  .header-search-input {
    font-size: 14px;
    width: 200px;
    margin-right: 0px;

    ::v-deep .el-input__inner {
      border-radius: 0;
      border: 0;
      border-bottom: 1px solid #d9d9d9;
    }
  }

  .header-search-button {
    cursor: pointer;
    font-size: 22px;
    vertical-align: middle;
    margin-bottom: 4px;
    margin-right: 0px;
  }

  .header-search-button:hover {
    cursor: pointer;
    color: #1086e0;
  }
}
</style>
