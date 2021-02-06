<template>
  <el-aside width="230px" style="margin-left: 14%;">
      <el-menu
        router
        :default-active="$route.path"
        class="el-menu-vertical-up"
        @select="handleSelect"
        >
        <div class="blog-title-box">
          <div class="blog-title">{{$t('common.blog-name')}}</div>
        </div>
      <el-menu-item index="/home">
        <template slot="title">
          <i class="el-icon-s-home"></i>
          <span style="font-weight: bold">{{$t('common.home')}}</span>
        </template>
      </el-menu-item>
      <el-menu-item index="/archive">
        <template slot="title">
        <i class="el-icon-s-order"></i>
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
        <i class="el-icon-user-solid"></i>
        <span slot="title" style="font-weight: bold">{{$t('common.about')}}</span>
      </el-menu-item>
        <el-menu-item index="/love">
        <i class="el-icon-s-opportunity"></i>
        <span slot="title" style="font-weight: bold">{{$t('common.love')}}</span>
      </el-menu-item>
    </el-menu>
      <p></p>
      <el-menu
      class="el-menu-vertical-down"
      style="height: 310px">
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
          <el-link icon="el-icon-message" class="el-link-email" href="mailto:1524126437@qq.com" target="_blank" :underline="true">E-Mail&nbsp;&nbsp;</el-link>
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
name: "NewMenu",
  data() {
    return {
      circleUrl: "https://www.guanacossj.com/media/jia/IMG_0323.JPG",
    }
  },
  methods: {
    handleSelect(key, keyPath) {
      if (key === '/archive') {
        sessionStorage.removeItem("detail");
      }
    },
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
  .el-menu-vertical-up {
    margin-left: 4px;
    width: 222px;
    box-shadow: -0 4px 4px rgba(0, 0, 0, .30),
                -4px 0 0 0 rgba(0, 0, 0, .04)
  }
  .el-menu-vertical-down {
    margin-left: 4px;
    width: 222px;
    box-shadow: 0 4px 4px rgba(0, 0, 0, .30),
                0 0 4px rgba(0, 0, 0, .04),
                -4px 0 0 0 rgba(0, 0, 0, .04)
  }
  .el-menu-item {
    font-size: 12px;
    /*transition: border-color .0s,background-color .0s,color .0s;*/
  }
  .el-menu-item.is-active {
    background: #f4f4f5;
  }
  .a{
    text-decoration: none;
  }
  .el-footer {
    color: #333;
    text-align: center;
    line-height: 20px;
  }
  .blog-title-box {
    margin-left: -1px;
    text-align: center;
    width: 225px;
    font-size: 18px;
    font-weight: bold;
    color: white;
    height: 70px;
    background-color: #222222;
    line-height: 70px;
  }
  .blog-title {
    display: inline-block;
    vertical-align: middle;
  }
  .myname {
    text-align: center;
    font-size: 17px;
    font-weight: bolder;
    color: #222222;
  }
  .mypic {
    padding-top: 30px;
    text-align: center;
  }
  #tag-sign{
    text-align: center;
    font-size: 13px;
    color: #999999;
    font-weight: bolder;
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
    /*color: #fff*/
    font-size: 14px;
  }
  .el-link-email {
    font-size: 14px;
    /*color: #fff*/
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
