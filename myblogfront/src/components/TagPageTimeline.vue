<template>
  <el-container>
    <title>请叫我算术嘉の博客 | {{$t('common.tag')}} | {{ this.$route.params.name }}</title>
<!--    <Menu></Menu>-->
    <NewMenu></NewMenu>
    <el-main>
      <div v-if="this.$store.state.Canvas">
        <vue-canvas-nest></vue-canvas-nest>
      </div>
      <el-dropdown>
          <span class="el-dropdown-link">
            {{$t('common.lang')}}<i class="el-icon-arrow-down el-icon--right"></i>
          </span>
        <el-dropdown-menu slot="dropdown">
        <el-dropdown-item @click.native = "switchLang('zh')">{{$t('common.lang-zh')}}</el-dropdown-item>
        <el-dropdown-item @click.native = "switchLang('en')">{{$t('common.lang-en')}}</el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
      <div id="apparchive" v-loading="loading" :element-loading-text="$t('common.load-text')" style="height: 555px">
        <h1>{{ this.$route.params.name }}</h1>
        <div class="category-box">
          <div class="block">
          <el-timeline>
          <el-timeline-item :timestamp="value.fields.timestamp | formatDateymd" placement="top"  v-for="(value, index) in reverseblogList.slice((currentPage-1)*pageSize,currentPage*pageSize)" :key="index">
            <el-card>
              <router-link style="color: #4D4D4D;text-decoration: none" :to="'/post'+'/'+ value.fields.rand_id"><h1 style="font-size: 16px">{{ value.fields.title }}</h1></router-link>
              <p>{{ value.fields.authorname }} 发表于 {{ value.fields.timestamp | formatDate }}</p>
            </el-card>
          </el-timeline-item>
          </el-timeline>
          </div>
          <div class="hide-pagination">
            <el-switch v-model="value">
            </el-switch>
          </div>
        </div>
      <el-footer>
        <br>
        <el-pagination
          v-show="showPagination"
          background
          :hide-on-single-page="value"
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
      <el-backtop target=".el-main"></el-backtop>
    </el-main>
  </el-container>
</template>

<script>
  import moment from 'moment';
  import Menu from "./Menu";
  import NewMenu from "./NewMenu";
    export default {
        name: "TagPageTimeline",
        components: { Menu, NewMenu },
        data () {
          return {
            reverse: true,
            blogList: [],
            currentPage: 1,
            totalItems: 0,
            pageSize: 10,
            value: false,
            loading: true,
            showPagination: false
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
	        },
          formatDateymd:function(date) {
	        	return moment(date).format("YYYY/MM/DD");
	        },
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
            this.$http.get('https://www.guanacossj.com/blog/gettagarticles/'+this.$route.params.name,{
                _timeout:5000,
                onTimeout :(request) => {
                    this.$message.error({
                      message: this.$t('common.timeout'),
                      center: true
                    });
                    this.loading = false
                  }
                }).then((response) => {
              const res = JSON.parse(response.bodyText);
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
          switchLang(val){
            this.$i18n.locale=val;//此处val为 zh 或者 en
            sessionStorage.setItem('lang', val);
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
    /*margin-right: 150px;*/
    /*margin-right: 12%;*/
  }
  #apparchive {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    /*color: #2c3e50;*/
    color: #4d4d4d;
    margin-top: 30px;
  }
  .category-box {
    text-align: left;
  }
  .hide-pagination {
    float: right;
    /*padding-right: 0 !important;*/
  }
  .el-dropdown {
    float: right;
  }
  .el-dropdown-link {
    cursor: pointer;
  }
  .el-icon-arrow-down {
    font-size: 12px;
  }
  /deep/ .el-timeline {
      padding-left: 10px;
      padding-right: 10px;
    }
    .el-timeline-item {
      padding-left: 10px;
    }
</style>
