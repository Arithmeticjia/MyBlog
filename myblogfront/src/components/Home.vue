<template>
  <el-container style="height: 693px">
    <el-aside width="220px" style="margin-left: 100px">
      <el-menu
      class="el-menu-vertical-demo"
      background-color="#545c64"
      text-color="#fff"
      active-text-color="#ffd04b"
      style="height: 355px">
<!--        </br>-->
        <p></p>
        <el-menu-item id="myblogname">
          请叫我算术嘉の博客
        </el-menu-item>
<!--        </br>-->
      <el-menu-item index="1" @click="skiplocal('/#/home')">
        <template slot="title">
          <i class="el-icon-location"></i>
          <span style="font-weight: bold" @click="skiplocal('/#/home')">首页</span>
<!--          <el-link href="/#/home" :underline="false" style="color: white;font-weight: bold">首页</el-link>-->
        </template>
      </el-menu-item>
      <el-menu-item index="2" @click="skiplocal('/#/archive')">
        <template slot="title">
        <i class="el-icon-document"></i>
        <span style="font-weight: bold" @click="skiplocal('/#/archive')">归档</span>
<!--        <el-link href="/#/archive" :underline="false" style="color: white;font-weight: bold">归档</el-link>-->
        </template>
      </el-menu-item>
      <el-menu-item index="3" @click="notfinishalert">
        <i class="el-icon-menu"></i>
        <span slot="title" style="font-weight: bold" @click="notfinishalert">分类</span>
      </el-menu-item>
      <el-menu-item index="4" @click="skiplocal('/#/bloglist')">
        <i class="el-icon-search"></i>
        <span slot="title" style="font-weight: bold" @click="skiplocal('/#/bloglist')">搜索</span>
      </el-menu-item>
      <el-menu-item index="5" @click="notfinishalert">
        <i class="el-icon-user"></i>
        <span slot="title" style="font-weight: bold" @click="notfinishalert">关于我</span>
      </el-menu-item>
    </el-menu>
      <p></p>
      <el-menu
      class="el-menu-vertical-demo"
      background-color="#545c64"
      text-color="#fff"
      style="height: 315px">
        </br>
          <div id="myname">
            <el-avatar  :size="120" shape="square" :src="circleUrl"></el-avatar>
          </div>
        <el-menu-item id="myname">
          <span slot="title">请叫我算术嘉</span>
        </el-menu-item>
        <el-menu-item id="tag-sign">
          <span>雨纷纷</span>
            <el-divider direction="vertical"></el-divider>
          <span>旧故里</span>
            <el-divider direction="vertical"></el-divider>
          <span>草木深</span>
        </el-menu-item>
        <el-menu-item id="tag-github">
          <el-link icon="el-icon-link" type="primary" href="https://github.com/Arithmeticjia" target="_blank" :underline="false">github</el-link>
            <el-divider direction="vertical"></el-divider>
          <el-link icon="el-icon-message" type="primary" href="https://github.com/Arithmeticjia" target="_blank" :underline="false">mail</el-link>
<!--          <el-button icon="el-icon-message" @click="skip('https://www.guanacossj.com/')" type="text">mail</el-button>-->
        </el-menu-item>
    </el-menu>
    </el-aside>
    <el-main>
      <div id="appvuedjango">
        <img src="../assets/logo.png">
        </br>
        </br>
        </br>
        </br>
        </br>
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
    margin-right: 100px;
  }
  #appvuedjango {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    /*color: #2c3e50;*/
    color: #4d4d4d;
    margin-top: 0;
  }
  #myblogname{
    text-align: center;
    font-size: larger;
    font-weight: bold;
  }
  #myname{
    text-align: center;
    font-size: 16px;
    font-weight: bold;
  }
  #tag-sign{
    text-align: center;
    font-size: small;
  }

</style>
