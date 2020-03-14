<template>
  <el-container style="height: 693px">
    <el-aside width="220px" style="margin-left: 130px">
      <el-menu
        default-active="3"
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
      <div id="appcategory" v-loading="loading" element-loading-text="拼命加载中">
        <div class="category-box">
          <div class="grid-content bg-puprple-light">
            <el-row type="flex" class="row-bg" justify="space-around">
              <el-col :span="20">
                <div class="grid-content bg-puprple-light">
                  <h1 style="text-align: center">分类</h1>
                  <p style="text-align: center">当前共计{{ totalItems }}个分类</p>
                  <div class="me" v-for="(value, key, index) in categoryList.slice((currentPage-1)*pageSize,currentPage*pageSize)">
                    <router-link style="color: #4D4D4D" :to="'/category/'+value.fields.name"><p style="color: #4D4D4D; font-size: large;">{{ value.fields.name }}</p></router-link>
                  </div>
                </div>
              </el-col>
            </el-row>
          </div>
        </div>
        </br>
<!--        <p></p>-->
        <div class="hide-pagination">
          <el-switch v-model="value">
          </el-switch>
        </div>
      <el-footer>
<!--        </br>-->
<!--        </br>-->
          <el-pagination
            v-show="showpagination"
            :hide-on-single-page="value"
            background
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page="currentPage"
            :page-sizes="[1, 2, 3, 4]"
            :page-size="pageSize"
            :total="totalItems"
            layout="prev, pager, next, total">
          </el-pagination>
      </el-footer>
      </div>
    </el-main>
  </el-container>
</template>

<script>
    export default {
        name: "Category",
        data () {
          return {
            circleUrl: "https://www.guanacossj.com/media/jia/IMG_0323.JPG",
            reverse: true,
            value: false,
            categoryList: [],
            currentPage:1,
            totalItems:0,
            loading: true,
            pageSize:10,
          }
        },
        mounted() {
          this.showCategorys();
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
          handleSizeChange(val) {
             this.pageSize = val;
             this.handleCurrentChange(this.currentPage);
           },
          handleCurrentChange: function(currentPage){
             this.currentPage = currentPage;
             if(this.flag) {
               this.blogList = this.filterTableDataEnd
             }
          },
          showCategorys () {
            this.$http.get('https://www.guanacossj.com/blog/getallcategory/',{
                _timeout:5000,
                onTimeout :(request) => {
                    this.$message.error('请求超时');
                    this.loading = false
                  }
                }).then((response) => {
                var res = JSON.parse(response.bodyText);
                if (res.error_num === 0) {
                  this.loading = false;
                  this.showpagination = true;
                  this.categoryList = res['list'];
                  this.totalItems = this.categoryList.length;
                } else {
                  this.$message.error('查询分类列表失败');
                }
              })
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
  #appcategory {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    /*color: #2c3e50;*/
    color: #4d4d4d;
    margin-top: 0;
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
    /*box-shadow: 0 2px 4px rgba(0, 0, 0, .20), 0 0 6px rgba(0, 0, 0, .04)*/
    box-shadow: 0 4px 4px rgba(0, 0, 0, .30), 0 0 6px rgba(0, 0, 0, .04)
  }
  .category-box {
    text-align: left;
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
  .hide-pagination {
    float: right;
    /*padding-right: 0 !important;*/
  }
</style>
