<template>
  <div class="app-container">
    <el-tree ref="treeRef" :data="departmentTree" style="width: 500px" node-key="id" default-expand-all :expand-on-click-node="false" :filter-node-method="filterTree">
      <template #default="{ node }">
        <span class="custom-tree-node">
          <span>{{ node.label }}</span>
          <span>
            <a @click="handleAppend(node)">追加</a>
            <a style="margin-left: 36px" @click="handleUpdate(node)">修改</a>
            <a style="margin-left: 36px" @click="handleDelete(node)">删除</a>
          </span>
        </span>
      </template>
    </el-tree>

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogVisible">
      <el-form :model="temp" label-position="left" label-width="70px" style="width: 100%; padding: 0 4% 0 4%;">
        <el-form-item label="部门名称" prop="label">
          <el-input v-model="temp.label" />
        </el-form-item>
        <el-form-item label="上级部门" prop="parent">
          <!-- 修改 -->
          <el-select v-if="dialogStatus!=='create'" v-model="temp.parent" class="filter-item" placeholder="请选择父部门" @change="changeSelect">
            <el-option v-for="item in departmentList" :key="item.id" :label="item.label" :value="item.id" />
          </el-select>
          <div v-else>
            <!-- 新增 -->
            <el-input v-if="dialogStatus2==='new'" v-model="defaultParent" :disabled="true" />
            <!-- 追加 -->
            <el-select v-else v-model="temp.parent" class="filter-item" placeholder="请选择父部门" @change="changeSelect">
              <el-option v-for="item in departmentList" :key="item.id" :label="item.label" :value="item.id" />
            </el-select>
          </div>
        </el-form-item>
        <el-form-item label="部门等级" prop="level">
          <span>{{ temp.level }}</span>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="dialogStatus==='create'?createData():updateData()">确定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import { getGroupDepartmentTree, addDepartment, setDepartment, delDepartment } from '@/api/department'

export default {
  data() {
    return {
      userdata: {},
      departmentTree: null,
      departmentList: null,
      temp: {},
      defaultParent: '根节点',
      dialogVisible: false,
      dialogStatus: '',
      dialogStatus2: '',
      textMap: {
        update: '修改部门',
        create: '新增部门'
      }
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
      this.$refs.treeRef.filter(newVal)
    },
    create() {
      this.resetTemp()
      this.dialogStatus = 'create'
      this.dialogStatus2 = 'new'
      this.dialogVisible = true
    }
  },
  created() {
    this.userdata = this.$store.getters.userdata
    this.resetTemp()
    this.getDepartmentList()
  },
  methods: {
    resetTemp() {
      this.temp = {
        id: 0,
        label: '',
        parent: 0,
        level: 1
      }
    },
    getDepartmentList() {
      this.loading = true
      getGroupDepartmentTree({
        id: this.userdata.user.id
      }).then(response => {
        this.departmentTree = response.data.data.list
        this.departmentList = [{
          id: 0,
          label: this.defaultParent
        }]
        this.generator(this.departmentTree)
        this.loading = false
      }).catch(error => {
        this.loading = false
        Promise.reject(error)
      })
    },
    generator(tree) {
      tree.forEach(v => {
        this.departmentList.push(v)
        if (v.children != null) {
          this.generator(v.children)
        }
      })
    },
    filterTree(value, data) {
      if (!value) return true
      return data.label.includes(value)
    },
    createData() {
      addDepartment({
        id: this.userdata.user.id,
        name: this.temp.label,
        parent: this.temp.parent,
        level: this.temp.level
      }).then(() => {
        this.$message({ type: 'success', message: '新增成功!' })
        this.getDepartmentList()
        this.dialogVisible = false
      })
    },
    changeSelect(id) {
      this.departmentList.forEach(v => {
        if (v.id === id) {
          this.temp.level = v.level + 1
        } else {
          this.temp.level = 1
        }
      })
    },
    handleAppend(row) {
      this.temp = {
        id: 0,
        label: '',
        parent: row.data.id,
        level: row.data.level + 1
      }
      this.dialogStatus = 'create'
      this.dialogStatus2 = 'append'
      this.dialogVisible = true
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row.data)
      this.dialogStatus = 'update'
      this.dialogVisible = true
    },
    updateData() {
      setDepartment({
        id: this.userdata.user.id,
        pid: this.temp.id,
        name: this.temp.label,
        parent: this.temp.parent,
        level: this.temp.level
      }).then(() => {
        this.$message({ type: 'success', message: '修改成功!' })
        this.getDepartmentList()
        this.dialogVisible = false
      })
    },
    handleDelete(row) {
      this.$confirm('确定要删除吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        delDepartment({
          id: this.userdata.user.id,
          pid: row.data.id
        }).then(() => {
          this.$message({ type: 'success', message: '删除成功!' })
          this.getDepartmentList()
        })
      })
    }
  }
}
</script>

<style>
.custom-tree-node {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 14px;
  padding-right: 8px;
}
</style>
