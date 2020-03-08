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
        <div class="grid-content bg-puprple-light" v-for="(value, key, index) in singleblog">
            <el-row type="flex" class="row-bg" justify="space-around">
              <el-col :span="21">
                <div class="grid-content bg-puprple-light">
                  <h1>{{ value.fields.title }}</h1>
                  <div>
                    <span style="color: #7d7d7d;font-size: small"><i class="el-icon-date"></i> 发表于：{{ value.fields.timestamp | formatDate }}</span>
                    <el-divider direction="vertical"></el-divider>
                    <span style="color: #7d7d7d;font-size: small"><i class="el-icon-user-solid"></i> 作者：{{ value.fields.authorname }}</span>
                  </div>
                  </br>
                  <div class="bodymarkdown" style="text-align: left" v-html="markdownhtml"></div>
                </div>
              </el-col>
            </el-row>
        </div>
      </div>
    </el-main>
  </el-container>
</template>

<script>
  import moment from 'moment';
  import "../assets/tango.css";
    export default {
        name: "Me",
        data () {
          return {
            circleUrl: "https://www.guanacossj.com/media/jia/IMG_0323.JPG",
            singleId: 1,
            singleblog: [],
            markdownhtml: ""
          }
        },
        created: function () {
          // this.getId();
        },
        mounted: function () {
          this.showSingleBlog();
        },
        filters: {
	        /*
	         时间格式自定义 只需把字符串里面的改成自己所需的格式
	        */
	        formatDate:function(date) {
	        	return moment(date).format("YYYY-MM-DD HH:mm:ss");
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
          getId() {
            this.singleId = this.$route.params.id;
          },
          showSingleBlog () {
            this.$http.get('https://www.guanacossj.com/blog/getsinglearticle/'+this.$route.params.id,{
                _timeout:5000,
                onTimeout :(request) => {
                    this.$message.error('请求超时');
                    this.loading = false
                  }
                }).then((response) => {
                var res = JSON.parse(response.bodyText);
                if (res.error_num === 0) {
                  this.loading = false;
                  this.markdownhtml = res.markdown;
                  this.singleblog = res['list'];
                  console.log(this.markdownhtml)
                } else {
                  this.$message.error('查询博客详情失败');
                }
              })
          }
        }
    }
</script>

<style scoped>
  .el-main{
    margin-right: 100px;
  }
  .el-menu{
    box-shadow: 0 4px 4px rgba(0, 0, 0, .30), 0 0 6px rgba(0, 0, 0, .04)
  }
  .el-row {
    margin-bottom: 20px;
    &:last-child {
      margin-bottom: 0;
    }
  }
  .el-col {
    border-radius: 4px;
  }
  .bg-purple-dark {
    background: #99a9bf;
  }
  .bg-purple {
    background: #d3dce6;
  }
  .bg-purple-light {
    background: #e5e9f2;
  }
  .grid-content {
    border-radius: 4px;
    min-height: 36px;
  }
  .row-bg {
    padding: 10px 0;
    /*background-color: #f9fafc;*/
    background-color: rgba(255, 255, 255, 0);
    box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04)
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
