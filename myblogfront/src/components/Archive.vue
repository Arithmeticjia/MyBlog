<template>
  <el-container>
    <title>{{$t('common.archive')}} | 请叫我算术嘉の博客</title>
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
        <div v-for="(value, key, index) in reverseblogList.slice((currentPage-1)*pageSize,currentPage*pageSize)" >
            <el-row type="flex" class="row-bg" justify="space-around">
              <el-col :span="20">
                <el-dropdown  @command="handleCommand">
                  <span class="el-dropdown-link"><i class="el-icon-share el-icon--right"></i>
                  </span>
                  <el-dropdown-menu slot="dropdown">
                    <el-dropdown-item icon="el-icon-plus" :command="composeValue(value.fields.rand_id,value.fields.title, 'weibo')">新浪微博</el-dropdown-item>
                    <el-dropdown-item icon="el-icon-circle-plus" :command="composeValue(value.fields.rand_id,value.fields.title,'qq_zone')">QQ空间</el-dropdown-item>
                    <el-dropdown-item icon="el-icon-circle-plus-outline" :command="composeValue(value.fields.rand_id,value.fields.title, 'copyLink')">复制链接</el-dropdown-item>
                  </el-dropdown-menu>
                </el-dropdown>
                <div class="grid-content bg-puprple-light">
                  <h1 style="font-size: 20px"><a style="text-decoration: none;color: #4D4D4D" :href="'/post'+ '/' + value.fields.rand_id">{{ value.fields.title }}</a></h1>
                  <div>
                    <span style="color: #7d7d7d;font-size: small"><i class="el-icon-date"></i> 发表于：{{ value.fields.timestamp | formatDate }}</span>
                    <el-divider direction="vertical"></el-divider>
                    <span style="color: #7d7d7d;font-size: small"><i class="el-icon-view"></i> 阅读次数：{{ value.fields.views | numberFormat }}</span>
                    <el-divider direction="vertical"></el-divider>
                    <span style="color: #7d7d7d;font-size: small"><i class="el-icon-reading"></i> 字数：{{ value.fields.words_number | numberFormat }}</span>
                  </div>
                  <br>
                  <p style="font-size: 17px">{{ value.fields.body.substring(0,100)+'......' }}</p>
                  <br>
                  <el-button style="border-radius: 0;" size="medium"><router-link style="color: #4D4D4D;text-decoration: none" :to="'/post'+ '/' + value.fields.rand_id">{{$t('common.Archive.read-more')}} >></router-link></el-button>
                </div>
                <br>
              </el-col>
            </el-row>
        </div>
        <el-footer>
          <el-pagination
            v-show="showPagination"
            background
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page.sync="currentPage"
            :page-sizes="[1, 2, 3, 4]"
            :page-size="pageSize"
            :total="totalItems"
            v-if="totalItems !== 0"
            layout="prev, pager, next, total">
          </el-pagination>
          <br>
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
        name: "Archive",
        components: { Menu, NewMenu },
        data () {
          return {
            reverse: true,
            blogList: [],
            currentPage: 1,
            totalItems: 0,
            pageSize: 10,
            loading: true,
            showPagination: false,
            centerDialogVisible: false
          }
        },
        watch: {
          '$i18n.locale'(newVal,oldVal) {
            document.title = this.$t('common.archive') + ' | 请叫我算术嘉の博客'
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
	        formatDate: function(date) {
	        	return moment(date).format("YYYY-MM-DD HH:mm:ss");
	        },
          numberFormat: function (value) {
            return value.toString().replace(/(\d)(?=(?:\d{3})+$)/g, '$1,')
          }
        },
        mounted: function () {
          this.showBlogs();
          this.getLastPage();
          document.title = this.$t('common.archive') + ' | 请叫我算术嘉の博客';
        },
        destroyed(){
          sessionStorage.removeItem("detail");
        },
        created() {
        },
        methods: {
          composeValue(token, title, command) {
            return {
              'token': token,
              'title': title,
              'command': command
            }
          },
          handleCommand(command) {
            switch (command.command) {
              case "copyLink":
                this.copyLink(command.token);
                return;
              case "weibo":
                this.shareWeibo(command.token, command.title)
                return;
              case "qq_zone":
                this.shareQQZone(command.token, command.title)
                return;
            }
          },
          shareWeibo(token, title) {
            const wb_appkey = "2841315419",
              wb_ralateUid = "5155692052",
              wb_pic = "",
              wb_language = "zh_cn";
            window.open("http://service.weibo.com/share/share.php?url="+"https://blog.guanacossj.com/post/"+token+"&appkey="+wb_appkey+"&title="+title+"&pic="+wb_pic+"&ralateUid="+wb_ralateUid+"&language="+wb_language+"", '_blank');
          },
          shareQQZone(token, title) {
            window.open("http://sns.qzone.qq.com/cgi-bin/qzshare/cgi_qzshare_onekey?url="+"https://blog.guanacossj.com/post/"+token+"&title="+title, '_blank');
          },
          copyLink(val) {
            let shareUrl = 'https://www.blog.guanacossj.com/post/'+ val;
            let oInput = document.createElement("input");
            oInput.value = shareUrl;
            document.body.appendChild(oInput);
            oInput.select(); // 选择对象
            document.execCommand("Copy"); // 执行浏览器复制命令
            oInput.className = "oInput";
            oInput.style.display = "none";
             this.$confirm("链接已复制，快去分享给好友吧！！！", "恭喜！", {
               center: true,
               type: 'success',
               iconClass: 'el-icon-check',
               cancelButtonText: this.$t('common.table.operation.cancel'),
               confirmButtonText: this.$t('common.table.operation.confirm'),
             });
          },
          handleSizeChange(val) {
             this.pageSize = val;
             this.handleCurrentChange(this.currentPage);
           },
          switchLang(val){
            this.$i18n.locale = val;//此处val为 zh 或者 en
            sessionStorage.setItem('lang', val);
          },
          handleCurrentChange: function(currentPage){
             this.currentPage = currentPage;
             sessionStorage.setItem('currentPage', currentPage);
             if(this.flag) {
               this.blogList = this.filterTableDataEnd
             }
          },
          getLastPage(){
      　　　　//当从详情页返回的时候，先获取详情页中存下来的detall标识，在列表页中，把获取到的分页页码重新赋值赋值，用以返回前的页面，保持不变
            if(sessionStorage.getItem('detail')){
              // console.log(Number(sessionStorage.getItem("currentPage")));
              //如果有这个就读取缓存里面的数据
              this.currentPage = Number(sessionStorage.getItem("currentPage"));
            }else{
              this.currentPage = 1;
              //这个主要是从其他页面第一次进入列表页，清掉缓存里面的数据
              sessionStorage.removeItem("currentPage");
            }
          },
          showBlogs () {
            this.$http.get('https://www.guanacossj.com/blog/getallarticle/',{
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
                    this.showPagination = true;
                    this.blogList = res['list'];
                    this.totalItems = this.blogList.length;
                    this.handleCurrentChange(this.currentPage)
                } else {
                    this.$message.error('查询博客列表失败');
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
  #apparchive {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    /*color: #2c3e50;*/
    color: #4d4d4d;
    margin-top: 30px;
  }
  .el-dropdown {
    float: right;
    /*margin-top: 0;*/
    /*position: absolute;*/
    /*z-index: 10;*/
    /*margin-left: 760px;*/
  }
  .el-dropdown-link {
    cursor: pointer;
  }
  .el-icon-arrow-down {
    font-size: 12px;
  }
</style>
