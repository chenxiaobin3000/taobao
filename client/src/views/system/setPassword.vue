<template>
  <div class="app-container">
    <el-form>
      <el-form-item label="旧密码">
        <el-input ref="oldPwd" v-model.trim="oldPwd" :type="oldPwdType" style="width: 260px; margin-left: 40px;">
          <i slot="suffix">
            <span class="show-pwd" @click="showOldPwd">
              <svg-icon :icon-class="oldPwdType === 'password' ? 'eye' : 'eye-open'" />
            </span>
          </i>
        </el-input>
      </el-form-item>
      <el-form-item label="新密码">
        <el-input ref="newPwd" v-model.trim="newPwd" :type="newPwdType" style="width: 260px; margin-left: 40px;">
          <i slot="suffix">
            <span class="show-pwd" @click="showNewPwd">
              <svg-icon :icon-class="newPwdType === 'password' ? 'eye' : 'eye-open'" />
            </span>
          </i>
        </el-input>
      </el-form-item>
      <el-form-item label="重复新密码">
        <el-input ref="newPwd2" v-model.trim="newPwd2" :type="newPwd2Type" style="width: 260px; margin-left:12px;">
          <i slot="suffix">
            <span class="show-pwd" @click="showNewPwd2">
              <svg-icon :icon-class="newPwd2Type === 'password' ? 'eye' : 'eye-open'" />
            </span>
          </i>
        </el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" style="margin-left:20px;" @click="submit">修改密码</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import md5 from 'js-md5'
import { mapState } from 'vuex'
import { setPassword } from '@/api/account'

export default {
  data() {
    return {
      oldPwd: '',
      oldPwdType: 'password',
      newPwd: '',
      newPwdType: 'password',
      newPwd2: '',
      newPwd2Type: 'password'
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
      this.$message({ type: 'error', message: '该页面不支持搜索操作!' })
    },
    create() {
      this.$message({ type: 'error', message: '该页面不支持新增操作!' })
    }
  },
  methods: {
    submit() {
      if (this.newPwd !== this.newPwd2) {
        this.$message({ type: 'error', message: '输入的新密码必须相同!' })
        return
      }
      if (this.newPwd === this.oldPwd) {
        this.$message({ type: 'error', message: '新旧密码不能一样!' })
        return
      }
      setPassword({
        id: this.$store.getters.userdata.user.id,
        oldpassword: md5(this.oldPwd),
        newpassword: md5(this.newPwd)
      }).then(response => {
        this.$message({ type: 'success', message: '修改成功!' })
      })
    },
    showOldPwd() {
      if (this.oldPwdType === 'password') {
        this.oldPwdType = ''
      } else {
        this.oldPwdType = 'password'
      }
      this.$nextTick(() => {
        this.$refs.oldPwd.focus()
      })
    },
    showNewPwd() {
      if (this.newPwdType === 'password') {
        this.newPwdType = ''
      } else {
        this.newPwdType = 'password'
      }
      this.$nextTick(() => {
        this.$refs.newPwd.focus()
      })
    },
    showNewPwd2() {
      if (this.newPwd2Type === 'password') {
        this.newPwd2Type = ''
      } else {
        this.newPwd2Type = 'password'
      }
      this.$nextTick(() => {
        this.$refs.newPwd2.focus()
      })
    }
  }
}
</script>
