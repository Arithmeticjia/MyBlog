<template>
  <el-container>
    <title></title>
<!--    <Markdown :psMsg=navList @callFather="pageJump"></Markdown>-->
    <NewMarkdown :psMsg=navList @callFather="pageJump"></NewMarkdown>
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
      <div id="appsingle" v-loading="this.loading" :element-loading-text="$t('common.load-text')">
        <div class="grid-content bg-puprple-light" v-for="(value, key, index) in singleBlog">
            <el-row type="flex" class="row-bg" justify="space-around">
              <el-col :span="21">
                <div class="grid-content bg-puprple-light">
                  <h1>{{ value.fields.title }}</h1>
                  <div>
                    <span style="color: #7d7d7d;font-size: small"><i class="el-icon-date"></i> 发表于：{{ value.fields.timestamp | formatDate }}</span>
                    <el-divider direction="vertical"></el-divider>
                    <span style="color: #7d7d7d;font-size: small"><i class="el-icon-user"></i> 作者：{{ value.fields.authorname }}</span>
                    <el-divider direction="vertical"></el-divider>
                    <span style="color: #7d7d7d;font-size: small"><i class="el-icon-document"></i><router-link style="color: #7D7D7D" :to="'/category/'+ value.fields.category"> 分类：{{ value.fields.category }}</router-link></span>
                    <el-divider direction="vertical"></el-divider>
                    <span style="color: #7d7d7d;font-size: small"><i class="el-icon-view"></i> 阅读次数：{{ value.fields.views }}</span>
                  </div>
                  <br>
                  <span style="color: #7d7d7d;font-size: small"><i class="el-icon-collection-tag"></i> 标签：</span>
                  <div style="display: inline" v-for="(tag) in tags">
                    <el-tag size="mini"><router-link style="color: #7D7D7D" :to="'/tag/'+ tag">{{ tag }}</router-link></el-tag>&nbsp;
                  </div>
                  <br>
                  <div class="bodymarkdown" style="text-align: left;line-height: 2em;font-size: 17px" v-html="markdownhtml"></div>
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
                  <p class="author-text"><b>本文链接：</b><router-link style="color: #4D4D4D;" :to="this.$route.path">https://www.blog.guanacossj.com{{ this.$route.path }}</router-link></p>
                </div>
              </el-col>
            </el-row>
            <div class="back">
              <el-popover
                placement="top"
                title="返回上一页"
                width="200"
                trigger="hover"
                content="可返回上次浏览的归档列表。">
                <el-button slot="reference" type="text" icon="el-icon-back" @click="goBack" style="font-size: 16px">{{$t('common.Single.back')}}</el-button>
              </el-popover>
            </div>
            <div class="prev-next">
              <div class="prev-article">
                <i class="el-icon-caret-left" style="font-size: 20px;vertical-align: middle;"></i>
              </div>
              <router-link :to="'/post/'+prev_article_id"><div class="prev-article" v-html="prev_article_title.substr(0,25)+'...'"></div></router-link>
              <div class="next-article">
                <i class="el-icon-caret-right" style="font-size: 20px;vertical-align: middle;"></i>
              </div>
              <router-link :to="'/post/'+next_article_id"><div class="next-article" v-html="next_article_title.substr(0,25)+'...'"></div></router-link>
            </div>
        </div>
      <el-backtop target=".el-main"></el-backtop>
    </el-main>
  </el-container>
</template>

<script>
import moment from 'moment';
import "../assets/tango.css";
import Markdown from "./Markdown";
import marked from "marked";
import NewMarkdown from "./NewMarkdown";
import Clipboard from "clipboard"
import { removeWatermark, setWaterMark } from '../utils/watermark'

let rendererMD = new marked.Renderer();
  marked.setOptions({
    renderer: rendererMD,
    gfm: true,
    tables: true,
    breaks: false,
    pedantic: false,
    sanitize: false,
    smartLists: true,
    smartypants: false,
  });
    export default {
        name: "Single",
        components: {
          Markdown,
          NewMarkdown,
        },
        data () {
          return {
            wechatUrl: "https://www.guanacossj.com/media/articlebodypics/wechatpay.png",
            singleId: 1,
            singleBlog: [],
            titleName: "",
            markdownhtml: "s",
            prev_article_title: "已经是第一篇了",
            next_article_title: "已经是最后一篇了",
            prev_article_id: 0,
            next_article_id: 0,
            loading: true,
            tags: [],
            navList: [],
            activeIndex: 0,
            docsFirstLevels: [],
            docsSecondLevels: [],
            childrenActiveIndex: 0,
            html: "",
            copyBtn: null //存储初始化复制按钮事件
          }
        },
        created: function () {
          window.copyText = this.copyText;
        },
        watch: {
          '$route':'showSingleBlog'
        },
        mounted: function () {
          if(this.$route.params.id.length !== 8) {
            this.showSingleBlog();
          }else {
            this.getSingleBlog();
          }
          //setWaterMark('liergou', '李二狗');
        },
        filters: {
	        /*
	         时间格式自定义 只需把字符串里面的改成自己所需的格式
	        */
	        formatDate:function(date) {
	        	return moment(date).format("YYYY-MM-DD HH:mm:ss");
	        }
        },
        computed: {
          content() {
            return this.html;
          },
        //此函数将markdown内容进一步的转换
          compiledMarkdown: function() {
            let index = 0;
            rendererMD.heading = function(text, level) {
              //我比较习惯三级和四级目录，这里看你喜欢
              if (level <= 4) {
                return `<h${level} id="data-${index++}">${text}</h${level}>`;
              } else {
                return `<h${level}>${text}</h${level}>`;
              }
            };
            return marked(this.content);
          },
        },
        methods: {
          copyText() {
            const clipboard = new Clipboard(".copy_btn")
            clipboard.on('success', e => {
              this.$message({ type: 'success', message: this.$t('common.Single.copy_success'), center: true })
              // 释放内存
              clipboard.destroy()
            })
            clipboard.on('error', e => {
              // 不支持复制
              this.$message({ type: 'warning', message: this.$t('common.Single.copy_fail'), center: true})
              // 释放内存
              clipboard.destroy()
            })
          },
          goBack() {
            this.$router.go(-1);
          },
          switchLang(val){
            this.$i18n.locale=val;//此处val为 zh 或者 en
            sessionStorage.setItem('lang', val);
          },
          getId() {
            this.singleId = this.$route.params.id;
          },
          showSingleBlog () {
            sessionStorage.setItem("detail", true);
            this.$http.get('https://www.guanacossj.com/blog/getsinglearticle/' + this.$route.params.id,{
                _timeout:5000,
                onTimeout :(request) => {
                    this.$message.error({
                      message: this.$t('common.timeout'),
                      center: true
                    });
                    this.loading = false
                  }
                }).then((response) => {
                var res = JSON.parse(response.bodyText);
                if (res.error_num === 0) {
                  this.tags = res['list'][0]['fields']['tags'];
                  this.loading = false;
                  this.markdownhtml = res.markdown;
                  this.html = res['list'][0].fields.body;
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
                  this.singleBlog = res['list'];
                  document.title = res['list'][0].fields.title;
                  this.navList = this.handleNavTree();
                  if(this.navList.length === 0) {
                    this.navList[0] = {
                      title: "此页目录为空",
                      children: new Array(1)['length'] = 0
                    };
                  }
                  this.getDocsFirstLevels(0);
                } else {
                  this.$message.error('查询博客详情失败');
                }
              })
          },
          getSingleBlog () {
            sessionStorage.setItem("detail", true);
            this.$http.get('https://www.guanacossj.com/blog/single-article/' + this.$route.params.id,{
                _timeout:5000,
                onTimeout :(request) => {
                    this.$message.error({
                      message: this.$t('common.timeout'),
                      center: true
                    });
                    this.loading = false
                  }
                }).then((response) => {
                var res = JSON.parse(response.bodyText);
                if (res.error_num === 0) {
                  this.tags = res['list'][0]['fields']['tags'];
                  this.loading = false;
                  this.markdownhtml = res.markdown;
                  this.html = res['list'][0].fields.body;
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
                  this.singleBlog = res['list'];
                  document.title = res['list'][0].fields.title;
                  this.navList = this.handleNavTree();
                  if(this.navList.length === 0) {
                    this.navList[0] = {
                      title: "此页目录为空",
                      children: new Array(1)['length'] = 0
                    };
                  }
                  this.getDocsFirstLevels(0);
                } else {
                  this.$message.error('查询博客详情失败');
                }
              })
          },
          childrenCurrentClick(index) {
            this.childrenActiveIndex = index;
          },
          getDocsFirstLevels(times) {
            // 解决图片加载会影响高度问题
            setTimeout(() => {
              let firstLevels = [];
              Array.from(document.querySelectorAll("h3"), (element) => {
                firstLevels.push(element.offsetTop - 60);
              });
              this.docsFirstLevels = firstLevels;
              if (times < 8) {
                this.getDocsFirstLevels(times + 1);
              }
            }, 500);
          },
          getDocsSecondLevels(parentActiveIndex) {
            let idx = parentActiveIndex;
            let secondLevels = [];
            let navChildren = this.navList[idx].children;

            if (navChildren.length > 0) {
              secondLevels = navChildren.map((item) => {
                return this.$el.querySelector(`#data-${item.index}`).offsetTop - 60;
              });
              this.docsSecondLevels = secondLevels;
            }
          },
          getLevelActiveIndex(scrollTop, docsLevels) {
            let currentIdx = null;
            let nowActive = docsLevels.some((currentValue, index) => {
              if (currentValue >= scrollTop) {
                currentIdx = index;
                return true;
              }
            });

            currentIdx = currentIdx - 1;

            if (nowActive && currentIdx === -1) {
              currentIdx = 0;
            } else if (!nowActive && currentIdx === -1) {
              currentIdx = docsLevels.length - 1;
            }
            return currentIdx;
          },
          goAnchor(selector) {
            selector = selector.replace(/^\s+|\s+$/g,"").replace(/、|：|（|）|\.|\/|:|，|\[|]/g, "").replace(/\ /g, "-").toLowerCase();
            const anchor = document.getElementById(selector);//获取元素
            if(anchor) {
                setTimeout(()=>{//页面没有渲染完成时是无法滚动的，因此设置延迟
                    anchor.scrollIntoView(); //js的内置方法，可滚动视图位置至元素位置
                },100);
            }
          },
          pageJump(id) {
            this.titleClickScroll = true;
            //这里我与原作者的不太一样，发现原作者的scrollTop一直为0，所以使用了Vuetify自带的goTo事件
            // this.$vuetify.goTo(this.$el.querySelector(`#${id}`).offsetTop - 40);
            // setTimeout(() => (this.titleClickScroll = false), 100);
            this.goAnchor(id);
          },
          currentClick(index) {
            this.activeIndex = index;
            this.getDocsSecondLevels(index);
          },
          getTitle(content) {
            let nav = [];
            let tempArr = [];
            content.replace(/(#+)[^#][^\n]*?(?:\n)/g, function(match, m1) {
              let title = match.replace("\n", "");
              let level = m1.length;
              tempArr.push({
                title: title.replace(/^#+/, "").replace(/\([^)]*?\)/, ""),
                level: level,
                children: [],
              });
            });
            // 只处理二级到四级标题，以及添加与id对应的index值，这里还是有点bug,因为某些code里面的注释可能有多个井号
            nav = tempArr.filter((item) => item.level >= 2 && item.level <= 4);
            let index = 0;
            return (nav = nav.map((item) => {
              item.index = index++;
              return item;
            }));
          },
          handleNavTree() {
            const navs = this.getTitle(this.content)
            navs.forEach((item) => {
              item.parent = this.getParentIndex(navs, item.index);
            })
            return this.filterArray(navs);
          },
          filterArray(data, parent) {
            const self = this
            var tree = []
            var temp
            for (var i = 0; i < data.length; i++) {
              if (data[i].parent === parent) {
                var obj = data[i]
                temp = self.filterArray(data, data[i].index);
                if (temp.length > 0) {
                  obj.children = temp;
                }
                tree.push(obj);
              }
            }
            return tree;
          },
          find(arr, condition) {
            return arr.filter((item) => {
              for (let key in condition) {
                if (condition.hasOwnProperty(key) && condition[key] !== item[key]) {
                  return false;
                }
              }
              return true;
            });
          },
          getParentIndex(nav, endIndex) {
            for (var i = endIndex - 1; i >= 0; i--) {
              if (nav[endIndex].level > nav[i].level) {
                return nav[i].index;
              }
            }
          },
          appendToParentNav(nav, parentIndex, newNav) {
            let index = this.findIndex(nav, {
              index: parentIndex,
            });
            nav[index].children = nav[index].children.concat(newNav);
          },
          findIndex(arr, condition) {
            let ret = -1;
            arr.forEach((item, index) => {
              for (var key in condition) {
                if (condition.hasOwnProperty(key) && condition[key] !== item[key]) {
                  return false;
                }
              }
              ret = index;
            });
            return ret;
          },
        }
    }
</script>

<style scoped>
  .el-main{
    margin-bottom: 20px;
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
  .back {
    margin-bottom: 20px;
  }
  .el-page-header {

  }
  .author-text {
    text-align: left;
  }
  a {
    text-decoration: none;
  }
  .router-link-active {
    text-decoration: none;
  }
</style>
