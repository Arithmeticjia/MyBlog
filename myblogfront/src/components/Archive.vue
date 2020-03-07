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
      <el-menu-item index="1">
        <template slot="title">
          <i class="el-icon-location"></i>
          <span style="font-weight: bold" @click="skiplocal('/#/home')">首页</span>
<!--          <el-link href="/#/home" :underline="false" style="color: white;font-weight: bold">首页</el-link>-->
        </template>
      </el-menu-item>
      <el-menu-item index="2">
        <template slot="title">
        <i class="el-icon-document"></i>
        <span style="font-weight: bold" @click="skiplocal('/#/archive')">归档</span>
<!--        <el-link href="/#/archive" :underline="false" style="color: white;font-weight: bold">归档</el-link>-->
        </template>
      </el-menu-item>
      <el-menu-item index="3">
        <i class="el-icon-menu"></i>
        <span slot="title" style="font-weight: bold" @click="notfinishalert">分类</span>
      </el-menu-item>
        <el-menu-item index="4">
        <i class="el-icon-search"></i>
        <span slot="title" style="font-weight: bold" @click="skiplocal('/#/bloglist')">搜索</span>
      </el-menu-item>
      <el-menu-item index="5">
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
        <el-menu-item id="myname">
          <div>
            <el-avatar  :size="120" shape="square" :src="circleUrl"></el-avatar>
          </div>
        </el-menu-item>
        </br>
        </br>
        </br>
        <el-menu-item id="myname">
          <i></i>
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
      <div id="appvuedjango" v-loading="loading" >
        <div class="grid-content bg-puprple-light" v-for="(value, key, index) in reverseblogList.slice((currentPage-1)*pageSize,currentPage*pageSize)">
            <el-row type="flex" class="row-bg" justify="space-around">
              <el-col :span="20">
                <div class="grid-content bg-puprple-light">
                  <h1>{{ value.fields.title }}</h1>
                  <h4>{{ value.fields.timestamp }}</h4>
                  <p>{{ value.fields.body.substring(0,100)+'......' }}</p>
                </div>
              </el-col>
            </el-row>
        </div>
      </div>
      <el-footer>
        </br>
        </br>
        <el-pagination
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
            blogList: [],
            currentPage:1,
            totalItems:0,
            pageSize:10,
            loading: true,
          }
        },
        computed: {
          reverseblogList() {
            return this.blogList.reverse();
          }
        },
        mounted: function () {
          this.showBlogs();
        },
        methods: {
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
          showBlogs () {
            this.$http.get('https://www.guanacossj.com/blog/showarticles/',{
                _timeout:5000,
                onTimeout :(request) => {
                    this.$message.error('请求超时');
                    this.loading = false
                  }
                }).then((response) => {
                var res = JSON.parse(response.bodyText);
                if (res.error_num === 0) {
                  this.loading = false;
                  this.blogList = res['list'];
                  console.log(this.blogList);
                  this.totalItems = this.blogList.length;
                  this.originblogList = this.blogList;
                } else {
                  this.$message.error('查询博客列表失败');
                }
              })
          },
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
  .el-footer {
    color: #333;
    text-align: center;
    line-height: 20px;
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
    background-color: #f9fafc;
    box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04)
  }
  .el-main{
    margin-right: 100px;
  }
  #appvuedjango {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
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
