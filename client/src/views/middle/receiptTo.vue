<template>
  <div class="app-container">
    <div class="receipt-import-row">
      <div class="receipt-upload" :class="{ disabled: uploading }" @click="handleClickUpload" @drop="handleDrop" @dragover="handleDragover" @dragenter="handleDragover">
        <span>{{ uploading ? '正在识别发票，请稍候' : '拖拽发票文件到这里' }}<em v-if="!uploading">浏览本地</em></span>
        <input ref="receiptFile" type="file" accept="application/pdf,.pdf" @change="handleFileChange">
      </div>
    </div>
    <el-form :model="listQuery" label-position="left" label-width="50px" style="width: 100%; padding: 0 1% 0 1%;">
      <el-row>
        <el-col :span="6">
          <el-form-item label="店铺:">
            <el-select v-model="listQuery.id" class="filter-item" placeholder="请选择店铺" @change="handleChange">
              <el-option v-for="item in shopList" :key="item.id" :label="item.name" :value="item.id" />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>

    <el-table ref="table" v-loading="loading" :data="list" :height="tableHeight" style="width: 100%" border fit highlight-current-row>
      <el-table-column align="center" label="项目名称" width="200px">
        <template slot-scope="scope">
          {{ projectId2Name(scope.row.project_id) }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="数量" width="60px">
        <template slot-scope="scope">
          {{ scope.row.project_num }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="金额" width="80px">
        <template slot-scope="scope">
          {{ scope.row.amount }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="税额" width="60px">
        <template slot-scope="scope">
          {{ scope.row.tax }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="税率" width="60px">
        <template slot-scope="scope">
          {{ scope.row.tax_rate }}%
        </template>
      </el-table-column>
      <el-table-column align="center" label="抬头" width="240px">
        <template slot-scope="scope">
          {{ scope.row.company }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="税号" width="180px">
        <template slot-scope="scope">
          {{ scope.row.company_id }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="填报人" width="80px">
        <template slot-scope="scope">
          {{ userId2Name(scope.row.user_id) }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="备注">
        <template slot-scope="scope">
          {{ scope.row.receipt_note }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="日期" width="140px">
        <template slot-scope="scope">
          {{ scope.row.create_date }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="操作" width="80">
        <template slot-scope="{row}">
          <el-button type="danger" size="mini" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.num" @pagination="getReceiptToList" />

  </div>
</template>

<script>
import Pagination from '@/components/Pagination'
import { getOwnShopList } from '@/api/system/shop'
import { getUserList } from '@/api/system/user'
import { getReceiptItemList } from '@/api/middle/receiptItem'
import { addReceiptTo, delReceiptTo, getReceiptToList } from '@/api/middle/receiptTo'

export default {
  components: { Pagination },
  data() {
    return {
      userdata: {},
      tableHeight: 600,
      list: null,
      total: 0,
      loading: false,
      uploading: false,
      shopList: [],
      userList: [],
      projectList: [],
      listQuery: {
        id: 0,
        page: 1,
        num: 10
      }
    }
  },
  mounted: function() {
    setTimeout(() => {
      if (this.$refs.table) {
        this.tableHeight = window.innerHeight - this.$refs.table.$el.offsetTop - 78
      }
    }, 1000)
  },
  created() {
    this.userdata = this.$store.getters.userdata
    this.listQuery.id = this.$store.getters.shop
    this.getOwnShopList()
  },
  methods: {
    getReceiptToList() {
      this.loading = true
      getReceiptToList(
        this.listQuery
      ).then(response => {
        this.total = response.data.data.total
        this.list = response.data.data.list
        this.loading = false
      }).catch(error => {
        this.loading = false
        Promise.reject(error)
      })
    },
    getOwnShopList() {
      getOwnShopList({
        id: this.userdata.company.id,
        uid: this.userdata.user.id
      }).then(response => {
        this.shopList = response.data.data
        if (this.listQuery.id === 0 && this.shopList.length > 0) {
          this.listQuery.id = this.shopList[0].id
        }
        this.getUserList()
      })
    },
    getUserList() {
      getUserList({
        id: this.userdata.company.id,
        page: 1,
        num: 1000
      }).then(response => {
        this.userList = response.data.data.list
        this.loadReceiptItemList()
      })
    },
    loadReceiptItemList(loadList = true) {
      return getReceiptItemList({
        page: 1,
        num: 1000
      }).then(response => {
        this.projectList = response.data.data.list || []
        if (loadList) {
          this.getReceiptToList()
        }
      })
    },
    userId2Name(id) {
      for (let i = 0; i < this.userList.length; ++i) {
        if (this.userList[i].id === id) {
          return this.userList[i].name
        }
      }
      return '异常'
    },
    projectId2Name(id) {
      for (let i = 0; i < this.projectList.length; ++i) {
        if (this.projectList[i].id === id) {
          return this.projectList[i].project_name
        }
      }
      return '异常'
    },
    handleChange() {
      this.listQuery.page = 1
      this.$store.commit('header/SET_HEADER_SHOP', this.listQuery.id)
      this.getReceiptToList()
    },
    handleClickUpload() {
      if (this.uploading) {
        return
      }
      this.$refs.receiptFile.click()
    },
    handleFileChange(e) {
      const file = e.target.files[0]
      e.target.value = ''
      this.uploadReceipt(file)
    },
    handleDragover(e) {
      e.preventDefault()
      e.stopPropagation()
    },
    handleDrop(e) {
      e.preventDefault()
      e.stopPropagation()
      if (this.uploading) {
        return
      }
      const file = e.dataTransfer.files[0]
      this.uploadReceipt(file)
    },
    checkUploadFile(file) {
      if (!file) {
        return false
      }
      const isPdf = file.type === 'application/pdf' || file.name.toLowerCase().endsWith('.pdf')
      if (!isPdf) {
        this.$message({ type: 'error', message: '请上传PDF文件!' })
      }
      return isPdf
    },
    async uploadReceipt(file) {
      if (!this.checkUploadFile(file)) {
        return
      }
      const data = new FormData()
      data.append('id', this.listQuery.id)
      data.append('file', file)
      this.uploading = true
      try {
        await addReceiptTo(data)
        this.$message({ type: 'success', message: '识别成功!' })
        await this.loadReceiptItemList()
      } catch (error) {
        const message = error.response && error.response.data && error.response.data.msg ? error.response.data.msg : '识别失败!'
        this.$message({ type: 'error', message })
      } finally {
        this.uploading = false
      }
    },
    handleDelete(row) {
      this.$confirm('确定要删除吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        delReceiptTo({
          id: row.id
        }).then(() => {
          this.$message({ type: 'success', message: '删除成功!' })
          this.getReceiptToList()
        })
      })
    }
  }
}
</script>

<style scoped>
.receipt-import-row {
  position: sticky;
  top: 0;
  z-index: 9;
  min-height: 48px;
  padding: 6px 1%;
  margin-bottom: 8px;
  background: #fff;
  border-bottom: 1px solid #d8dce5;
}

.receipt-upload {
  width: 100%;
  height: 36px;
  line-height: 34px;
  text-align: center;
  cursor: pointer;
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  box-sizing: border-box;
}

.receipt-upload:hover {
  border-color: #409eff;
}

.receipt-upload.disabled {
  cursor: not-allowed;
  background: #f5f7fa;
}

.receipt-upload span {
  font-size: 13px;
  color: #606266;
}

.receipt-upload em {
  color: #409eff;
  font-style: normal;
}

.receipt-upload input {
  display: none;
}
</style>
