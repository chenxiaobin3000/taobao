<template>
  <div class="login-container">
    <el-form ref="loginForm" :model="loginForm" :rules="loginRules" class="login-form" autocomplete="on" label-position="left">

      <div class="title-container">
        <h3 class="title">集数助手 - 管理后台</h3>
      </div>

      <el-form-item prop="account">
        <span class="svg-container">
          <svg-icon icon-class="user" />
        </span>
        <el-input
          ref="account"
          v-model="loginForm.account"
          placeholder="请输入账号"
          type="text"
          tabindex="1"
          autocomplete="on"
        />
      </el-form-item>

      <el-tooltip v-model="capsTooltip" content="Caps lock is On" placement="right" manual>
        <el-form-item prop="password">
          <span class="svg-container">
            <svg-icon icon-class="password" />
          </span>
          <el-input
            :key="passwordType"
            ref="password"
            v-model="loginForm.password"
            :type="passwordType"
            placeholder="请输入密码"
            tabindex="2"
            autocomplete="on"
            @keyup.native="checkCapslock"
            @blur="capsTooltip = false"
          />
          <span class="show-pwd" @click="showPwd">
            <svg-icon :icon-class="passwordType === 'password' ? 'eye' : 'eye-open'" />
          </span>
        </el-form-item>
      </el-tooltip>

      <div style="padding-bottom: 20px;">
        <el-checkbox v-model="checked" class="login-check">记住密码</el-checkbox>
      </div>

      <el-button :loading="loading" class="login-btn" @click.native.prevent="handleLogin">登  陆</el-button>

      <div style="position:relative">
        <div class="tips">
          <span>新注册账号请尽快修改默认密码，以免导致信息泄露。</span>
        </div>
      </div>
    </el-form>

    <div class="footer">
      <a href="https://beian.miit.gov.cn/" target="_blank">闽ICP备2023001340号</a>
    </div>
  </div>
</template>

<script>
import { getAccount, setAccount, removeAccount, getPassword, setPassword, removePassword } from '@/utils/cache'

export default {
  name: 'Login',
  data() {
    const validateAccount = (rule, value, callback) => {
      if (value.length < 4) {
        callback(new Error('账号不能少于4个字符'))
      } else {
        callback()
      }
    }
    const validatePassword = (rule, value, callback) => {
      if (value.length < 6) {
        callback(new Error('密码不能少于6个字符'))
      } else {
        callback()
      }
    }
    return {
      loginForm: {
        account: '',
        password: ''
      },
      loginRules: {
        account: [{ required: true, trigger: 'blur', validator: validateAccount }],
        password: [{ required: true, trigger: 'blur', validator: validatePassword }]
      },
      passwordType: 'password',
      capsTooltip: false,
      checked: false,
      loading: false,
      redirect: undefined,
      otherQuery: {}
    }
  },
  watch: {
    $route: {
      handler: function(route) {
        const query = route.query
        if (query) {
          this.redirect = query.redirect
          this.otherQuery = this.getOtherQuery(query)
        }
      },
      immediate: true
    }
  },
  mounted() {
    // 如果之前有选择记住密码
    const account = getAccount()
    const password = getPassword()
    this.loginForm.account = account
    this.loginForm.password = password
    if (account === '') {
      this.$refs.account.focus()
    } else if (password === '') {
      this.$refs.password.focus()
    }
    if (account && account.length > 3 && password && password.length > 5) {
      this.checked = true
    }
  },
  methods: {
    checkCapslock(e) {
      const { key } = e
      this.capsTooltip = key && key.length === 1 && (key >= 'A' && key <= 'Z')
    },
    showPwd() {
      if (this.passwordType === 'password') {
        this.passwordType = ''
      } else {
        this.passwordType = 'password'
      }
      this.$nextTick(() => {
        this.$refs.password.focus()
      })
    },
    handleLogin() {
      if (this.checked === true) {
        setAccount(this.loginForm.account)
        setPassword(this.loginForm.password)
      } else {
        removeAccount()
        removePassword()
      }
      this.loading = true
      this.$store.dispatch('account/login', this.loginForm).then(() => {
        this.$router.push({ path: '/' })
        this.loading = false
      }).catch(() => {
        this.loading = false
      })
    },
    getOtherQuery(query) {
      return Object.keys(query).reduce((acc, cur) => {
        if (cur !== 'redirect') {
          acc[cur] = query[cur]
        }
        return acc
      }, {})
    }
  }
}
</script>

<style lang="scss">
$bg:#a8e08c;
$light_gray:#303030;
$cursor: #fff;

@supports (-webkit-mask: none) and (not (cater-color: $cursor)) {
  .login-container .el-input input {
    color: $cursor;
  }
}

/* reset element-ui css */
.login-container {
  .el-input {
    display: inline-block;
    height: 48px;
    width: 85%;

    input {
      background: transparent;
      border: 0px;
      -webkit-appearance: none;
      -webkit-text-fill-color: $light_gray;
      border-radius: 0px;
      padding: 12px 5px 12px 15px;
      height: 48px;
      caret-color: $cursor;

      &:-webkit-autofill {
        box-shadow: 0 0 0px 1000px $bg inset !important;
        -webkit-text-fill-color: $light_gray;
      }
    }
  }

  .el-form-item {
    border: 1px solid rgba(0, 0, 0, 0.8);
    background: rgba(0, 0, 0, 0.0);
    border-radius: 5px;
    color: #454545;
  }

  .footer {
    position: fixed;
    bottom: 2px;
    width: 100%;
    text-align: center;
    color: #999;
  }
}
</style>

<style lang="scss" scoped>
$bg:#a8e08c;
$dark_gray:#303030;

.login-container {
  min-height: 100%;
  width: 100%;
  background-color: $bg;
  overflow: hidden;

  .login-form {
    position: relative;
    width: 520px;
    max-width: 100%;
    padding: 160px 35px 0;
    margin: 0 auto;
    overflow: hidden;
  }

  .login-check {
    color: $dark_gray;
  }

  .login-btn {
    width: 100%;
    margin-bottom: 20px;
    font-size: 18px;
  }

  .tips {
    font-size: 14px;
    color: #303030;
    margin-bottom: 10px;

    span {
      &:first-of-type {
        margin-right: 16px;
      }
    }
  }

  .svg-container {
    padding: 6px 5px 6px 15px;
    color: $dark_gray;
    vertical-align: middle;
    width: 30px;
    display: inline-block;
  }

  .title-container {
    position: relative;

    .title {
      font-size: 26px;
      color: $dark_gray;
      margin: 0px auto 40px auto;
      text-align: center;
      font-weight: bold;
    }
  }

  .show-pwd {
    position: absolute;
    right: 10px;
    top: 7px;
    font-size: 16px;
    color: $dark_gray;
    cursor: pointer;
    user-select: none;
  }

  .thirdparty-button {
    position: absolute;
    right: 0;
    bottom: 6px;
  }

  @media only screen and (max-width: 470px) {
    .thirdparty-button {
      display: none;
    }
  }
}
</style>
