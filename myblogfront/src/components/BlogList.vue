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
        <el-button type="primary" size="medium" icon="el-icon-search" @click="doFilter" style="float:right;"></el-button>
        <el-input
	        clearable
          type="text"
          v-model="searchinfo"
          placeholder="搜索"
          size="medium"
          style="width:160px;float: right;margin-right:10px">
        </el-input>
      <el-table height="550" v-loading="loading" :data="blogList.slice((currentPage-1)*pageSize,currentPage*pageSize)">
        <el-table-column prop="date" label="序号" width="50">
          <template scope="scope"> {{ scope.row.pk }} </template>
        </el-table-column>
        <el-table-column prop="name" label="标题" width="width: 100%">
          <template scope="scope"> {{ scope.row.fields.title }}</template>
        </el-table-column>
        <el-table-column prop="address" label="分类" width="width: 100%">
          <template scope="scope"> {{ scope.row.fields.category }} </template>
        </el-table-column>
        <el-table-column prop="address" label="标签" width="width: 100%">
          <template scope="scope"> {{ scope.row.fields.tags }} </template>
        </el-table-column>
        <el-table-column prop="address" label="作者" width="width: 100%">
          <template scope="scope"> {{ scope.row.fields.authorname }} </template>
        </el-table-column>
        <el-table-column prop="address" label="操作" width="width: 100%">
        <template slot-scope="scope">
          <el-button type="text" @click="open(scope.row.fields.title,scope.row.fields.body)" size="small">查看</el-button>
          <el-button @click="skip('https://www.guanacossj.com/blog/article/'+scope.row.pk+'/'+scope.row.fields.url_slug)" type="text" size="small">查看详情</el-button>
        </template>
        </el-table-column>
      </el-table>
      <el-footer>
<!--        <p></p>-->
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
            isCollapse: true,
            visible: false,
            currentPage:1,
            totalItems:0,
            pageSize:10,
            searchInfo: '',
            blogList: [],
            originblogList: [],
            searchinfo: '',
            filterTableDataEnd: [],
            flag:false,
            loading: true,
          }
        },
        mounted: function () {
          this.showBlogs();
        },
        methods: {
          reFresh: function() {
            window.location.reload();
          },
          doFilter: function() {
            if (this.searchinfo === "") {
              this.$message.warning("查询条件不能为空！");
              return;
            }
            this.filterTableDataEnd=[];
            this.originblogList.forEach((value, index) => {
              if(value.fields.title){
                if(value.fields.title.indexOf(this.searchinfo)>=0){
                  this.filterTableDataEnd.push(value);
                }
              }
            });
            //页面数据改变重新统计数据数量和当前页
             this.currentPage=1;
             this.totalItems=this.filterTableDataEnd.length;
             //渲染表格,根据值
             this.currentChangePage(this.filterTableDataEnd);
             //页面初始化数据需要判断是否检索过
             this.flag=true
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
          currentChangePage(list) {
             let from = (this.currentPage - 1) * this.pageSize;
             let to = this.currentPage * this.pageSize;
             this.blogList = [];
             if (to > list.length){
               for (; from < list.length; from++) {
                 if (list[from]) {
                   this.blogList.push(list[from]);
                 }
               }
             }else {
               for (; from < to; from++) {
                 if (list[from]) {
                   this.blogList.push(list[from]);
                 }
               }
             }
          },
          open(title,body) {
             this.$alert(body.substr(1,100)+'...', title, {
               confirmButtonText: '确定',
               // callback: action => {
               //   this.$message({
               //     type: 'info',
               //     message: `action: ${ action }`
               //   });
               // }
             });
          }     ,
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
          showBlogs () {
            this.$http.get('https://www.guanacossj.com/blog/getallarticle/',{
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
                  this.totalItems = this.blogList.length;
                  this.originblogList = this.blogList;
                } else {
                  this.$message.error('查询博客列表失败');
                }
              })
          }
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
  .el-footer {
    color: #333;
    text-align: center;
    line-height: 20px;
  }
  .el-main {
    color: #333;
    text-align: center;
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
