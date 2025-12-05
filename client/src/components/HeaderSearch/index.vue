<template>
  <div class="header-search">
    <el-input v-model="search" placeholder="请输入想查询的内容" class="header-search-input" @keyup.enter.native="handleSearch" />
    <svg-icon icon-class="search" class="header-search-button" @click.stop="handleSearch" />
    <el-button class="header-create-button" @click="handleCreate">
      <i class="el-icon-circle-plus" />
    </el-button>
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
    },
    handleCreate() {
      this.$store.dispatch('header/create')
    }
  }
}
</script>

<style lang="scss" scoped>
.header-search {
  font-size: 0 !important;

  .header-search-input {
    font-size: 14px;
    width: 180px;
    margin-right: 2px;

    ::v-deep .el-input__inner {
      border-radius: 0;
      border: 0;
      border-bottom: 1px solid #d9d9d9;
    }
  }

  .header-search-button {
    cursor: pointer;
    font-size: 20px;
    vertical-align: middle;
    margin-bottom: 2px;
    margin-right: 14px;
  }

  .header-search-button:hover {
    cursor: pointer;
    color: #1086e0;
  }

  .header-create-button {
    padding: 0;
    text-align: center;
    vertical-align: middle;
    margin-bottom: 2px;
    margin-right:6px;
    font-size: 23px;
    color: #5a5e66;
    border-radius: 0;
    border: 0;
  }

  .header-create-button:hover {
    border-radius: 0;
    border: 0;
    color: #1086e0;
    background-color: #fff;
  }

  .header-create-button:focus {
    border-radius: 0;
    border: 0;
    color: #1086e0;
    background-color: #fff;
  }
}
</style>
