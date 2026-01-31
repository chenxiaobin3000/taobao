<template>
  <div>
    <!--
    <el-form :model="listQuery" label-position="left" label-width="70px" style="width: 100%; padding: 0 1% 0 1%;">
      <el-form-item label="店铺:" prop="shopName">
        <el-select v-model="listQuery.id" class="filter-item" placeholder="请选择店铺" @change="handleChange">
          <el-option v-for="item in shopList" :key="item.id" :label="item.name" :value="item.id" />
        </el-select>
      </el-form-item>
    </el-form>-->

    <!-- 销售数据 -->
    <el-row :gutter="40" class="panel-group">
      <div v-for="data in userdata.market" :key="'F'+data.id">
        <el-col :xs="6" :sm="6" :lg="6" class="card-panel-col">
          <div class="card-panel" @click="handleSelect(data.id)">
            <div class="card-panel-icon-wrapper icon-people">
              <div class="card-panel-text">{{ data.name }}</div>
            </div>
            <div class="card-panel-description">
              <div class="card-panel-text">平台</div>
            </div>
          </div>
        </el-col>
      </div>
    </el-row>

    <!-- 推广数据 -->
    <el-row :gutter="40" class="panel-group">
      <div v-for="data in userdata.shop" :key="'S'+data.id">
        <el-col :xs="6" :sm="6" :lg="6" class="card-panel-col">
          <div class="card-panel" @click="handleSelect(10000 + data.id)">
            <div class="card-panel-icon-wrapper icon-message">
              <div class="card-panel-text">{{ data.name }}</div>
            </div>
            <div class="card-panel-description">
              <div class="card-panel-text">店铺</div>
            </div>
          </div>
        </el-col>
      </div>
    </el-row>
  </div>
</template>

<script>

export default {
  data() {
    return {
      userdata: {}
    }
  },
  created() {
    this.userdata = this.$store.getters.userdata
  },
  methods: {
    handleSelect(id) {

    }
  }
}
</script>

<style scoped>
.panel-group {
  margin-top: 18px;

  .card-panel-col {
    margin-bottom: 32px;
  }

  .card-panel {
    height: 108px;
    cursor: pointer;
    font-size: 12px;
    position: relative;
    overflow: hidden;
    color: #666;
    background: #fff;
    box-shadow: 4px 4px 40px rgba(0, 0, 0, .05);
    border-color: rgba(0, 0, 0, .05);

    &:hover {
      .card-panel-icon-wrapper {
        color: #fff;
      }

      .icon-people {
        background: #40c9c6;
      }

      .icon-message {
        background: #36a3f7;
      }

      .icon-money {
        background: #f4516c;
      }

      .icon-shopping {
        background: #34bfa3
      }
    }

    .icon-people {
      color: #40c9c6;
    }

    .icon-message {
      color: #36a3f7;
    }

    .icon-money {
      color: #f4516c;
    }

    .icon-shopping {
      color: #34bfa3
    }

    .card-panel-icon-wrapper {
      float: left;
      margin: 14px 0 0 14px;
      padding: 16px;
      transition: all 0.38s ease-out;
      border-radius: 6px;
      font-weight: bold;

      .card-panel-text {
        line-height: 18px;
        color: rgba(0, 0, 0, 0.45);
        font-size: 16px;
        margin-bottom: 12px;
      }
    }

    .card-panel-description {
      float: right;
      margin: 26px;
      margin-left: 0px;
    }
  }
}

@media (max-width:550px) {
  .card-panel-description {
    display: none;
  }

  .card-panel-icon-wrapper {
    float: none !important;
    width: 100%;
    height: 100%;
    margin: 0 !important;

    .svg-icon {
      display: block;
      margin: 14px auto !important;
      float: none !important;
    }
  }
}
</style>
