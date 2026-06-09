<template>
  <div class="app-container">
    <el-form :model="temp" label-position="left" label-width="70px" style="width: 100%; padding: 0 1% 0 1%;">
      <el-row>
        <el-col :span="8">
          <el-form-item label="公司名称">
            <el-input v-model="temp.name" style="width: 220px;" @blur="submit" />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="负责人">
            <el-select v-model="temp.id" class="filter-item" placeholder="请选择负责人" style="width: 160px;" @change="submit">
              <el-option v-for="item in userList" :key="item.id" :label="item.name" :value="item.id" />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>

    <el-form>
      <el-form-item>
        <span class="receipt-title">公司发票登记</span>
        <el-button type="primary" size="mini" style="float:right;width:60px" @click="handleCreate">新增</el-button>
      </el-form-item>
    </el-form>

    <el-table ref="table" v-loading="loading" :data="list" height="250" style="width: 100%" border fit highlight-current-row>
      <el-table-column align="center" label="抬头">
        <template slot-scope="scope">
          {{ scope.row.company }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="税号" width="220px">
        <template slot-scope="scope">
          {{ scope.row.company_id }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="操作" width="100">
        <template slot-scope="{row}">
          <el-button type="danger" size="mini" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.num" @pagination="getReceiptOwnerList" />

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogVisible">
      <el-form :model="ownerTemp" label-position="left" label-width="70px" style="width: 100%; padding: 0 4% 0 4%;">
        <el-form-item label="抬头">
          <el-input v-model="ownerTemp.company" />
        </el-form-item>
        <el-form-item label="税号">
          <el-input v-model="ownerTemp.company_id" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="danger" @click="dialogVisible=false">取消</el-button>
        <el-button type="primary" @click="createData">确定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Pagination from '@/components/Pagination'
import { getUserList } from '@/api/system/user'
import { setCompany } from '@/api/system/company'
import { addReceiptOwner, delReceiptOwner, getReceiptOwnerList } from '@/api/system/receiptOwner'

export default {
  components: { Pagination },
  data() {
    return {
      userdata: {},
      list: null,
      total: 0,
      loading: false,
      userList: null,
      listQuery: {
        page: 1,
        num: 10
      },
      temp: {},
      oldTemp: {},
      ownerTemp: {},
      dialogVisible: false,
      dialogStatus: '',
      textMap: {
        create: '新增发票主体'
      }
    }
  },
  computed: {
    ...mapState({
      search: state => state.header.search
    })
  },
  watch: {
    search(newVal, oldVal) {
      this.$message({ type: 'error', message: '该页面不支持搜索操作!' })
    }
  },
  created() {
    this.userdata = this.$store.getters.userdata
    this.resetTemp()
    this.resetOwnerTemp()
    this.getUserList()
  },
  methods: {
    resetTemp() {
      this.temp = {
        id: this.userdata.company.user_id,
        name: this.userdata.company.name
      }
      this.oldTemp = Object.assign({}, this.temp)
    },
    resetOwnerTemp() {
      this.ownerTemp = {
        company: '',
        company_id: ''
      }
    },
    getUserList() {
      getUserList({
        id: this.userdata.company.id,
        page: 1,
        num: 1000
      }).then(response => {
        this.userList = response.data.data.list
        this.getReceiptOwnerList()
      })
    },
    getReceiptOwnerList() {
      this.loading = true
      getReceiptOwnerList(
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
    submit() {
      if (this.temp.name === this.oldTemp.name && this.temp.id === this.oldTemp.id) {
        return
      }
      setCompany({
        id: this.userdata.company.id,
        name: this.temp.name,
        uid: this.temp.id
      }).then(() => {
        this.oldTemp = Object.assign({}, this.temp)
        this.$message({ type: 'success', message: '修改成功!' })
      })
    },
    handleCreate() {
      this.resetOwnerTemp()
      this.dialogStatus = 'create'
      this.dialogVisible = true
    },
    createData() {
      addReceiptOwner({
        company: this.ownerTemp.company,
        company_id: this.ownerTemp.company_id
      }).then(() => {
        this.$message({ type: 'success', message: '新增成功!' })
        this.getReceiptOwnerList()
        this.dialogVisible = false
      })
    },
    handleDelete(row) {
      this.$confirm('确定要删除吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        delReceiptOwner({
          id: row.id
        }).then(() => {
          this.$message({ type: 'success', message: '删除成功!' })
          this.getReceiptOwnerList()
        })
      })
    }
  }
}
</script>

<style scoped>
.receipt-title {
  font-weight: bold;
}
</style>
