<template>
  <el-container style="height: 693px">
    <el-aside width="220px" style="margin-left: 130px">
      <el-menu
        default-active="1"
        class="el-menu-vertical-demo"
        background-color="#545c64"
        text-color="#fff"
        @open="handleOpen"
        active-text-color="#ffd04b"
        style="height: 370x">
<!--        </br>-->
<!--        <p></p>-->
        <div class="blogtitlebox">
          <div class="blogtitle">请叫我算术嘉の博客</div>
        </div>
        </br>
      <el-menu-item index="1" @click="skiplocal('/#/home')">
        <template slot="title">
          <i class="el-icon-location"></i>
          <span style="font-weight: bold">首页</span>
<!--          <el-link href="/#/home" :underline="false" style="color: white;font-weight: bold">首页</el-link>-->
        </template>
      </el-menu-item>
      <el-menu-item index="2" @click="skiplocal('/#/archive')">
        <template slot="title">
        <i class="el-icon-document"></i>
        <span style="font-weight: bold">归档</span>
<!--        <el-link href="/#/archive" :underline="false" style="color: white;font-weight: bold">归档</el-link>-->
        </template>
      </el-menu-item>
      <el-menu-item index="3" @click="notfinishalert">
        <i class="el-icon-menu"></i>
        <span slot="title" style="font-weight: bold">分类</span>
      </el-menu-item>
      <el-menu-item index="4" @click="skiplocal('/#/bloglist')">
        <i class="el-icon-search"></i>
        <span slot="title" style="font-weight: bold">搜索</span>
      </el-menu-item>
      <el-menu-item index="5" @click="skiplocal('/#/about')">
        <i class="el-icon-user"></i>
        <span slot="title" style="font-weight: bold">关于我</span>
      </el-menu-item>
    </el-menu>
      <p></p>
      <el-menu
      class="el-menu-vertical-demo"
      background-color="#545c64"
      text-color="#fff"
      style="height: 295px">
        </br>
        <div class="mypic">
            <el-avatar  :size="120" shape="square" :src="circleUrl"></el-avatar>
          </div>
        <p></p>
        <div class="myname">
          <span slot="title">请叫我算术嘉</span>
        </div>
        <p></p>
        <div id="tag-sign">
          <span>雨纷纷</span>
            <el-divider direction="vertical"></el-divider>
          <span>旧故里</span>
            <el-divider direction="vertical"></el-divider>
          <span>草木深</span>
        </div>
<!--        <el-menu-item id="tag-sign">-->
<!--          <span>雨纷纷</span>-->
<!--            <el-divider direction="vertical"></el-divider>-->
<!--          <span>旧故里</span>-->
<!--            <el-divider direction="vertical"></el-divider>-->
<!--          <span>草木深</span>-->
<!--        </el-menu-item>-->
        </br>
        <div class="tag-links">
<!--          &nbsp;-->
          <el-link icon="el-icon-link" style="color: white" class="el-link-github" href="https://github.com/Arithmeticjia" target="_blank" :underline="true">github</el-link>
          <el-divider direction="vertical"></el-divider>
<!--          &nbsp;-->
          <el-link icon="el-icon-message" style="color: white" class="el-link-email" href="mailto:1524126437@qq.com" target="_blank" :underline="false">e-mail</el-link>
<!--          <el-button icon="el-icon-message" @click="skip('https://www.guanacossj.com/')" type="text">mail</el-button>-->
        </div>
    </el-menu>
    </el-aside>
    <el-main>
      <div id="apphome">
        <img src="../assets/logo.png">
        </br>
        </br>
        </br>
        </br>
        </br>
        <p></p>
          <div>
            <span style="font-size: large">青春是一个短暂的美梦, 当你醒来时, 它早已消失无踪</span>
            <el-divider></el-divider>
            <span style="font-size: large">少量的邪恶足以抵消全部高贵的品质, 害得人声名狼藉</span>
            </div>
        </br>
        </br>
        </br>
        </br>
        <p><a style="text-decoration: none;font-size: large; color: #2C3E50"  href="https://www.guanacossj.com" target="_blank">https://www.guanacossj.com</a></p>
<!--        <el-link :underline="false" href="https://www.guanacossj.com" style="font-size: large" target="_blank">https://www.guanacossj.com</el-link>-->
      </div>
    </el-main>
  </el-container>
</template>

<script>
    export default {
        name: "Me",
        data () {
          return {
            circleUrl: "https://www.guanacossj.com/media/jia/IMG_0323.JPG",
            reverse: true,
            activities: [{
              content: '活动按期开始',
              timestamp: '2018-04-15'
            }, {
              content: '通过审核',
              timestamp: '2018-04-13'
            }, {
              content: '创建成功',
              timestamp: '2018-04-11'
            }]
          }
        },
        methods: {
          skip(url){
           window.open(url, target='_blank')
          },
          handleOpen(key, keyPath) {
            console.log(key, keyPath);
          },
          skiplocal(url){
            location.href = url
          },
          notfinishalert() {
            this.$alert('暂未开放，敬请期待，欢迎移步我的主页', {
              confirmButtonText: '确定',
              callback: action => {
                this.$message({
                  type: 'success',
                  message: `联系我吧!`
                });
              }
            });
          },
        }
    }
</script>

<style scoped>
  .el-menu{
    box-shadow: 0 4px 4px rgba(0, 0, 0, .30), 0 0 6px rgba(0, 0, 0, .04)
  }
  .el-main{
    margin-right: 130px;
  }
  #apphome {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    /*color: #2c3e50;*/
    color: #4d4d4d;
    margin-top: 0;
  }
  .blogtitlebox {
    text-align: center;
    font-size: larger;
    font-weight: bold;
    color: white;
    height: 75px;
    background-color: #292929;
    /*align-items: center;*/
    /*top:50%;*/
    /*position: absolute;*/
    line-height: 75px;
  }
  .blogtitle {
    display: inline-block;
    vertical-align: middle;
  }
  .myname {
    text-align: center;
    font-size: 16px;
    font-weight: bold;
    color: white;
  }
  .mypic {
    text-align: center;
  }
  #tag-sign{
    text-align: center;
    font-size: small;
    color: #cdcdcd;
  }
  .tag-links{
    height: 45px;
    text-align: center;
    font-size: 14px;
    line-height: 45px;
    width: 100%;
    color: #fff !important;
    /*margin: 0 auto;*/
  }
  .el-link--inner {
    color: #fff;
  }
  .el-link-github {
    color: #fff !important;
    font-size: 14px;
  }
  .el-link-github:hover {
    color: #ffd04b !important;
  }
  .el-link-email {
    font-size: 14px;
    color: #fff !important;
  }
  .el-link-email:hover {
    color: #ffd04b !important;
  }
  .el-menu-item.is-active {
    background: rgb(67, 74, 80) !important;
  }
  .el-submenu__title.is-active {
    background: #6db6ff !important;
  }
</style>
