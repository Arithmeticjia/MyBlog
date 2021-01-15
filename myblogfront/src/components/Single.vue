<template>
  <el-container class="layout-container">
    <Menu></Menu>
    <el-main>
      <el-dropdown>
          <span class="el-dropdown-link">
            {{$t('common.lang')}}<i class="el-icon-arrow-down el-icon--right"></i>
          </span>
        <el-dropdown-menu slot="dropdown">
        <el-dropdown-item @click.native = "switchLang('zh')">{{$t('common.lang-zh')}}</el-dropdown-item>
        <el-dropdown-item @click.native = "switchLang('en')">{{$t('common.lang-en')}}</el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
      <div id="appsingle" v-loading="this.loading" :element-loading-text="$t('common.load-text')">
        <div class="grid-content bg-puprple-light" v-for="(value, key, index) in singleblog">
            <el-row type="flex" class="row-bg" justify="space-around">
              <el-col :span="21">
                <div class="grid-content bg-puprple-light">
                  <h1>{{ value.fields.title }}</h1>
                  <div>
                    <span style="color: #7d7d7d;font-size: small"><i class="el-icon-date"></i> 发表于：{{ value.fields.timestamp | formatDate }}</span>
                    <el-divider direction="vertical"></el-divider>
                    <span style="color: #7d7d7d;font-size: small"><i class="el-icon-user-solid"></i> 作者：{{ value.fields.authorname }}</span>
                    <el-divider direction="vertical"></el-divider>
                    <span style="color: #7d7d7d;font-size: small"><i class="el-icon-document"></i> 分类：{{ value.fields.category }}</span>
                  </div>
                  <br>
                  <span style="color: #7d7d7d;font-size: small"><i class="el-icon-collection-tag"></i> 标签：</span>
                  <div style="display: inline" v-for="(tag) in tags">
                    <el-tag size="small"><router-link style="color: #4D4D4D" :to="'/tag/'+ tag">{{ tag }}</router-link></el-tag>&nbsp;
                  </div>
                  <br>
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
                <el-button icon="el-icon-coin" type="info" slot="reference">{{$t('common.Single.donate')}}</el-button>
              </el-popover>
            </div>
            </div>
            <br>
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
      <el-backtop target=".el-main"></el-backtop>
    </el-main>
  </el-container>
</template>

<script>
  import moment from 'moment';
  import Menu from "./Menu";
  import "../assets/tango.css";
    export default {
        name: "Single",
        components: { Menu },
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
            loading: true,
            tags: []
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
          switchLang(val){
            this.$i18n.locale=val;//此处val为 zh 或者 en
          },
          getId() {
            this.singleId = this.$route.params.id;
          },
          showSingleBlog () {
            this.$http.get('https://www.guanacossj.com/blog/getsinglearticle/'+this.$route.params.id,{
                _timeout:5000,
                onTimeout :(request) => {
                    this.$message.error(this.$t('common.timeout'));
                    this.loading = false
                  }
                }).then((response) => {
                var res = JSON.parse(response.bodyText);
                if (res.error_num === 0) {
                  this.tags = res['list'][0]['fields']['tags'];
                  this.loading = false;
                  this.markdownhtml = res.markdown;
                  if (res.prev_article_title !== ""){
                    this.prev_article_id = res.prev_article_id;
                    this.prev_article_title = res.prev_article_title;
                  }else {
                    this.prev_article_title = "已经是第一篇了"
                  }
                  if (res.next_article_title !== ""){
                    this.next_article_id = res.next_article_id;
                    this.next_article_title = res.next_article_title;
                  }else {
                    this.next_article_title = "已经是最后一篇了"
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
    /*margin-right: 150px;*/
    margin-right: 10%;
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
  #appsingle {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    /*color: #2c3e50;*/
    color: #4d4d4d;
    margin-top: 30px;
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
  .prev-next{
    display: inline;
  }
  .el-dropdown {
    float: right;
  }
  .el-dropdown-link {
    cursor: pointer;
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
  .layout-container {
    height: 100%;
  }
  a {
  text-decoration: none;
  }

  .router-link-active {
    text-decoration: none;
  }
</style>
