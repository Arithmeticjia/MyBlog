<template>
  <el-aside width="230px" style="margin-left: 14%;">
      <el-menu
        :default-active="$route.path"
        class="el-menu-vertical-demo"
        background-color="#545c64"
        text-color="#fff"
        active-text-color="#ffd04b"
        style="height: 440px"
        router>
        <div class="blogtitlebox">
          <div class="blogtitle">{{$t('common.blog-name')}}</div>
        </div>
        <br>
      <el-menu-item index="/home">
        <template slot="title">
          <i class="el-icon-location"></i>
          <span style="font-weight: bold">{{$t('common.home')}}</span>
        </template>
      </el-menu-item>
      <el-menu-item index="/archive" @click="skiplocal('/archive')">
        <template slot="title">
        <i class="el-icon-document"></i>
        <span style="font-weight: bold">{{$t('common.archive')}}</span>
        </template>
      </el-menu-item>
      <el-menu-item index="/category">
        <i class="el-icon-menu"></i>
        <span slot="title" style="font-weight: bold">{{$t('common.category')}}</span>
      </el-menu-item>
      <el-menu-item index="/list">
        <i class="el-icon-search"></i>
        <span slot="title" style="font-weight: bold">{{$t('common.search')}}</span>
      </el-menu-item>
      <el-menu-item index="/about">
        <i class="el-icon-user"></i>
        <span slot="title" style="font-weight: bold">{{$t('common.about')}}</span>
      </el-menu-item>
        <el-menu-item index="/love">
        <i class="el-icon-lollipop"></i>
        <span slot="title" style="font-weight: bold">{{$t('common.love')}}</span>
      </el-menu-item>
    </el-menu>
      <p></p>
      <el-menu
      class="el-menu-vertical-demo"
      background-color="#545c64"
      text-color="#fff"
      style="height: 310px">
        <br>
        <div class="mypic">
            <el-avatar  :size="130" shape="square" :src="circleUrl"></el-avatar>
          </div>
        <p></p>
        <div class="myname">
          <span slot="title">{{$t('common.myName')}}</span>
        </div>
        <p></p>
        <div id="tag-sign">
          <span>{{$t('common.autograph-left')}}</span>
            <el-divider direction="vertical"></el-divider>
          <span>{{$t('common.autograph-middle')}}</span>
            <el-divider direction="vertical"></el-divider>
          <span>{{$t('common.autograph-right')}}</span>
        </div>
        <p></p>
        <div class="tag-links">
          <el-link icon="el-icon-link" class="el-link-github" href="https://github.com/Arithmeticjia" target="_blank" :underline="true">GitHub</el-link>
          <el-divider direction="vertical"></el-divider>
          <el-link icon="el-icon-message" class="el-link-email" href="mailto:1524126437@qq.com" target="_blank" :underline="false">E-Mail</el-link>
        </div>
    </el-menu>
    <p></p>
<!--    <el-menu-->
<!--      class="el-menu-vertical-demo"-->
<!--      background-color="#545c64"-->
<!--      text-color="#fff"-->
<!--      style="height: 40px">-->
<!--        <div class="bei-an">-->
<!--          <el-link type="info" style="color: white" href="https://beian.miit.gov.cn" target="_blank">苏ICP备19007197号</el-link>-->
<!--        </div>-->
<!--    </el-menu>-->
    </el-aside>
</template>

<script>
export default {
name: "Menu",
  data() {
    return {
      circleUrl: "https://www.guanacossj.com/media/jia/IMG_0323.JPG",
    }
  },
  methods: {
    skip(url){
      window.open(url, target='_blank')
    },
    skiplocal(url){
      sessionStorage.removeItem("detail");
      location.href = url
    },
  }
}
</script>

<style scoped>
  .el-menu{
    box-shadow: 0 4px 4px rgba(0, 0, 0, .30), 0 0 6px rgba(0, 0, 0, .04)
  }
  .el-menu-item:hover {
    color: #ffd04b !important;
  }
  .a{
    text-decoration: none;
  }
  .el-footer {
    color: #333;
    text-align: center;
    line-height: 20px;
  }
  .blogtitlebox {
    text-align: center;
    font-size: 21px;
    font-weight: bold;
    color: white;
    height: 80px;
    background-color: #222222;
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
    font-size: 17px;
    font-weight: bold;
    color: white;
  }
  .mypic {
    margin-top: 5px;
    text-align: center;
  }
  #tag-sign{
    text-align: center;
    font-size: 14px;
    color: #cdcdcd;
  }
  .tag-links{
    height: 45px;
    text-align: center;
    font-size: 14px;
    line-height: 45px;
    width: 100%;
    color: #fff !important;
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
  .el-dropdown {
    float: right;
  }
  .bei-an {
    text-align: center;
    vertical-align: middle;
    font-size: 13px;
    color: white;
    font-weight: bold;
    line-height: 40px;
    height: 40px;
  }
</style>
