<template>
  <div>
    <el-card class="login-form-layout">
      <el-form
        autocomplete="on"
        :model="loginForm"
        ref="loginForm"
        label-position="left"
        :rules="rules"
      >
        <div style="text-align: center">
<!--          <svg-icon icon-class="login-mall" style="width: 56px;height: 56px;color: #409EFF"></svg-icon>-->
        </div>
        <h2 class="login-title color-main">登录</h2>
        <el-form-item prop="username">
          <el-input
            name="username"
            type="text"
            v-model="loginForm.username"
            autocomplete="on"
            placeholder="请输入用户名"
          >
            <span slot="prefix">
              <svg-icon icon-class="user" class="color-main"></svg-icon>
            </span>
          </el-input>
        </el-form-item >
        <el-form-item prop="password">
          <el-input
            name="password"
            :type="pwdType"
            @keyup.enter.native="handleLogin"
            v-model="loginForm.password"
            autocomplete="on"
            placeholder="请输入密码"
          >
            <span slot="prefix">
              <svg-icon icon-class="password" class="color-main"></svg-icon>
            </span>
            <span slot="suffix" @click="showPwd">
              <svg-icon icon-class="eye" class="color-main"></svg-icon>
            </span>
          </el-input>
        </el-form-item>
        <el-form-item style="margin-bottom: 20px">
          <el-button
            style="width: 100%"
            type="primary"
            :loading="loading"
            @click.native.prevent="handleLogin('loginForm')"
          >登录</el-button>
        </el-form-item>
      </el-form>
      <p style="text-align: center;font-size: small"><router-link style="color: #7D7D7D" :to="'/home'">返回首页</router-link></p>
      <p style="text-align: center;font-size: small">Powered by SpringBoot</p>
    </el-card>
  </div>
</template>

<script>
  import { mapMutations } from 'vuex';
  export default {
    name: "Login",
    data() {
      return {
        loginForm: {
          username: "",
          password: ""
        },
        userName:"",
        userToken: "",
        loading: false,
        pwdType: "password",
        rules: {
          username: [
            {required: true, message: '请输入用户名', trigger: 'blur'},
            {min: 1, max: 20, message: '长度在 1 到 20 个字符', trigger: 'blur'}
          ],
          password: [
            {required: true, message: '请输入密码', trigger: 'blur'},
            {min: 1, max: 20, message: '长度在 1 到 20 个字符', trigger: 'blur'}
          ],
        }
      };
    },
    mounted() {
      document.title = "请叫我算术嘉の博客 | " + this.$t('common.Login.login');
    },
    watch: {
      '$i18n.locale'(newVal,oldVal) {
        document.title = "请叫我算术嘉の博客 | " + this.$t('common.Login.login');
      }
    },
    methods: {
      ...mapMutations(['changeLogin']),
      showPwd() {
        if (this.pwdType === "password") {
          this.pwdType = "";
        } else {
          this.pwdType = "password";
        }
      },
      handleLogin(formName) {
        this.$refs[formName].validate(valid => {
          if (valid) {
            this.loading = true;
            this.$store
              .dispatch("Login", this.loginForm)
              .then(response => {
                this.loading = false;
                let code = response.data.code;
                if (code === 200) {
                  this.userToken = response.data.data.token;
                  this.userName  = response.data.data.username;
                  this.changeLogin
                  ({ Authorization: this.userToken, Username: this.userName });
                  this.$message.success({
                    message: '登录成功',
                    center: true
                  });
                  this.$router.push({
                    path: "/love",
                    query: { user: response.data.data.username }
                  });
                } else {
                  this.$message.error({
                    message: '用户名或密码不正确',
                    center: true
                  });
                }
              })
              .catch(() => {
                this.loading = false;
              });
          } else {
            // eslint-disable-next-line no-console
            console.log("参数验证不合法！");
            return false;
          }
        });
      }
    }
  };
</script>

<style scoped>
  .login-form-layout {
    position: absolute;
    left: 0;
    right: 0;
    width: 360px;
    margin: 140px auto;
    /*border-top: 10px solid #4D4D4D;*/
  }

  .login-title {
    text-align: center;
  }

  .login-center-layout {
    background: #409eff;
    width: auto;
    height: auto;
    max-width: 100%;
    max-height: 100%;
    margin-top: 200px;
  }
</style>
