<template>
  <el-container style="height: 690px">
    <el-aside width="220px" style="margin-left: 130px">
      <el-menu
        class="el-menu-vertical-demo"
        background-color="#545c64"
        text-color="#fff"
        @open="handleOpen"
        active-text-color="#ffd04b"
        style="height: 370x">
<!--        </br>-->
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
      <el-menu-item index="3" @click="skiplocal('/#/category')">
        <i class="el-icon-menu"></i>
        <span slot="title" style="font-weight: bold">分类</span>
      </el-menu-item>
      <el-menu-item index="4" @click="skiplocal('/#/bloglist')">
        <i class="el-icon-search"></i>
        <span slot="title" style="font-weight: bold">搜索</span>
      </el-menu-item>
      <el-menu-item index="5" @click="skiplocal('/#/about')">
        <i class="el-icon-user"></i>
        <span slot="title" style="font-weight: bold">关于</span>
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
      <div id="appvuedjango" v-loading="this.loading" element-loading-text="拼命加载中">
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
            <div class="donate">
              <el-popover
                placement="bottom"
                trigger="click"
                width="210">
                <el-image
                  style="width:210px; height: 300px;text-align: center"
                  :src="wechatUrl"
                  :fit="none"></el-image>
                <el-button icon="el-icon-coin" type="info" slot="reference">打赏</el-button>
              </el-popover>
            </div>
            </div>
            </br>
            <el-row type="flex" class="row-bg" justify="space-around">
              <el-col :span="21">
                <div class="grid-content bg-puprple-light">
                  <p class="author-text"><b>版权声明：</b>本文为博主「请叫我算术嘉」的原创文章，遵循 CC 4.0 BY-SA 版权协议，禁止转载。</p>
                  <p class="author-text"><b>本文链接：</b><router-link style="color: #4D4D4D;" :to="this.$route.path">http://www.blog.guanacossj.com/#{{ this.$route.path }}</router-link></p>
                </div>
              </el-col>
            </el-row>
            <div class="prev-next">
              <div class="prev-article">
<!--                <i class="el-icon-back"></i>-->
<!--                <i class="el-icon-d-arrow-left"></i>-->
                <i class="el-icon-caret-left"></i>
              </div>
              <router-link :to="'/single/'+prev_article_id"><div class="prev-article" v-html="prev_article_title.substr(0,25)+'...'"></div></router-link>
              <div class="next-article">
<!--                <i class="el-icon-right"></i>-->
<!--                <i class="el-icon-d-arrow-right"></i>-->
                <i class="el-icon-caret-right"></i>
              </div>
              <router-link :to="'/single/'+next_article_id"><div class="next-article" v-html="next_article_title.substr(0,25)+'...'"></div></router-link>
            </div>
        </div>
      </div>
    </el-main>
  </el-container>
</template>

<script>
  import moment from 'moment';
  import "../assets/tango.css";
    export default {
        name: "Single",
        data () {
          return {
            circleUrl: "https://www.guanacossj.com/media/jia/IMG_0323.JPG",
            wechatUrl: "https://www.guanacossj.com/media/articlebodypics/wechatpay.png",
            singleId: 1,
            singleblog: [],
            markdownhtml: "",
            prev_article_title: "已经是第一篇了",
            next_article_title: "已经是最后一篇了",
            prev_article_id: 0,
            next_article_id: 0,
            loading: true
          }
        },
        created: function () {
          // this.getId();
        },
        watch: {
          '$route':'showSingleBlog'
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
                  if (res.prev_article_title !== ""){
                    this.prev_article_id = res.prev_article_id;
                    this.prev_article_title = res.prev_article_title;
                  }
                  if (res.next_article_title !== ""){
                    this.next_article_id = res.next_article_id;
                    this.next_article_title = res.next_article_title;
                  }
                  this.singleblog = res['list'];
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
    margin-right: 130px;
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
  .tag-links{
    height: 45px;
    text-align: center;
    font-size: 14px;
    line-height: 45px;
    width: 100%;
    color: #fff !important;
    /*margin: 0 auto;*/
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
  #tag-sign{
    text-align: center;
    font-size: small;
    color: #cdcdcd;
  }
  .el-menu-item.is-active {
    background: rgb(67, 74, 80) !important;
  }
  .el-submenu__title.is-active {
    background: #6db6ff !important;
  }
  .prev-next{
    display: inline;
  }
  .next-article {
    color: #4D4D4D;
    float: right;
    display: inline;
    font-size: 15px;
    font-weight: bold;
  }
  .prev-article {
    color: #4D4D4D;
    float: left;
    display: inline;
    font-size: 15px;
    font-weight: bold;
  }
  .author-text {
    text-align: left;
  }
</style>
