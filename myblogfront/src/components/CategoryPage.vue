<template>
  <el-container style="height: 690px">
    <Menu></Menu>
    <el-main>
      <div id="apparchive" v-loading="loading" element-loading-text="拼命加载中" style="height: 555px">
        <h1>{{ this.$route.params.name }}</h1>
        <div class="grid-content bg-puprple-light" v-for="(value, key, index) in reverseblogList.slice((currentPage-1)*pageSize,currentPage*pageSize)">
            <el-row type="flex" class="row-bg" justify="space-around">
              <el-col :span="20">
                <div class="grid-content bg-puprple-light">
                  <h1><a style="text-decoration: none;color: #4D4D4D" :href="'/#/single'+ '/' + value.pk">{{ value.fields.title }}</a></h1>
                  <div>
                    <span style="color: #7d7d7d;font-size: small"><i class="el-icon-date"></i> 发表于：{{ value.fields.timestamp | formatDate }}</span>
                    <el-divider direction="vertical"></el-divider>
                    <span style="color: #7d7d7d;font-size: small"><i class="el-icon-view"></i> 阅读次数：{{ value.fields.views }}</span>
                  </div>
                  <br>
                  <p>{{ value.fields.body.substring(0,100)+'......' }}</p>
                  <br>
                  <el-button style="border-radius: 0;" size="medium" @click="skiplocal('/#/single'+ '/' + value.pk)">阅读全文 >></el-button>
                </div>
                <br>
              </el-col>
            </el-row>
        </div>
      <el-footer>
        <br>
        <el-pagination
          v-show="showpagination"
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
  import moment from 'moment'
  import Menu from "./Menu";
    export default {
        name: "CategoryPage",
        components: { Menu },
        data () {
          return {
            circleUrl: "https://www.guanacossj.com/media/jia/IMG_0323.JPG",
            reverse: true,
            blogList: [],
            currentPage:1,
            totalItems:0,
            pageSize:10,
            loading: true,
            showpagination: false
          }
        },
        computed: {
          reverseblogList() {
            return this.blogList.reverse();
          }
        },
        filters: {
	        /*
	         时间格式自定义 只需把字符串里面的改成自己所需的格式
	        */
	        formatDate:function(date) {
	        	return moment(date).format("YYYY-MM-DD HH:mm:ss");
	        }
        },
        watch: {
          '$route':'showBlogs'
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
            this.$http.get('https://www.guanacossj.com/blog/getcategoryarticles/'+this.$route.params.name,{
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
                  this.blogList = res['list'];
                  this.totalItems = this.blogList.length;
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
        }
    }
</script>

<style scoped>
  .el-menu{
    box-shadow: 0 4px 4px rgba(0, 0, 0, .30), 0 0 6px rgba(0, 0, 0, .04)
  }
  .a{
    text-decoration: none;
  }
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
    /*background-color: #f9fafc;*/
    background-color: rgba(255, 255, 255, 0);
    /*box-shadow: 0 2px 4px rgba(0, 0, 0, .20), 0 0 6px rgba(0, 0, 0, .04)*/
    box-shadow: 0 4px 4px rgba(0, 0, 0, .30), 0 0 6px rgba(0, 0, 0, .04)
  }
  .el-main{
    margin-right: 130px;
  }
  #apparchive {
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
