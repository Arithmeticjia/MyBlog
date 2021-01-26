<template>
  <el-aside width="230px">
      <el-menu
        :default-active="$route.path"
        class="el-menu-vertical-up"
        background-color="#545c64"
        text-color="#fff"
        active-text-color="#ffd04b"
        router>
        <div class="blogtitlebox">
          <div class="blogtitle">{{$t('common.blog-name')}}</div>
        </div>
        <br>
      <el-menu-item index="/home">
        <template slot="title">
          <i class="el-icon-location"></i>
          <span style="font-weight: bold">{{$t('common.home')}}</span>
        </template>
      </el-menu-item>
      <el-menu-item index="/archive" @click="skiplocal('/archive')">
        <template slot="title">
        <i class="el-icon-document"></i>
        <span style="font-weight: bold">{{$t('common.archive')}}</span>
        </template>
      </el-menu-item>
      <el-menu-item index="/category">
        <i class="el-icon-menu"></i>
        <span slot="title" style="font-weight: bold">{{$t('common.category')}}</span>
      </el-menu-item>
      <el-menu-item index="/list">
        <i class="el-icon-search"></i>
        <span slot="title" style="font-weight: bold">{{$t('common.search')}}</span>
      </el-menu-item>
      <el-menu-item index="/about">
        <i class="el-icon-user"></i>
        <span slot="title" style="font-weight: bold">{{$t('common.about')}}</span>
      </el-menu-item>
        <el-menu-item index="/love">
        <i class="el-icon-lollipop"></i>
        <span slot="title" style="font-weight: bold">{{$t('common.love')}}</span>
      </el-menu-item>
    </el-menu>
      <p></p>
      <el-menu
      class="el-menu-vertical-down"
      background-color="#545c64"
      text-color="#fff">
          <el-tooltip class="item" effect="dark" content="点击可重置目录" placement="top">
            <p class="mulu" @click="reSetIdex">{{$t('common.index')}}</p>
          </el-tooltip>
          <div class="mulu-detail">
            <div ref="element" style="color: #fff;margin-left: 20px;margin-right: 20px" v-for="(nav, index) in psMsg" :key="index"  @click="currentClick(index)"> <a href="javascript:" :class="{ 'active': activeIndex === index}" @click="pageJump(nav.title)">{{ nav.title }}</a>
             <div v-if="nav.children.length &gt; 0" class="menu-children-list" style="color: #fff">
              <div class="nav-list" style="color: #fff">
               <p style="color: #fff" v-for="(item, idx) in nav.children" :key="idx"  @click.stop="childrenCurrentClick(index, idx)"> <a href="javascript:" :class="{ 'activeChildren': ((childrenActiveIndex === idx) && (activeIndex === index))}" @click="pageJump(item.title)">{{ item.title }}</a></p>
              </div>
             </div>
            </div>
          </div>
    </el-menu>
    </el-aside>
</template>

<script>
export default {
name: "Markdown",
  data() {
    return {
      circleUrl: "https://www.guanacossj.com/media/jia/IMG_0323.JPG",
      activeIndex: -1,
      childrenActiveIndex: -1,
      docsFirstLevels: [],
      docsSecondLevels: [],
      navList: this.psMsg,
      clientHeight: 0
    }
  },
  props: {
    psMsg: Array,
  },
  mounted() {
  },
  methods: {
    reSetIdex() {
      this.activeIndex = -1;
      this.childrenActiveIndex = -1;
    },
    skip(url){
      window.open(url, target='_blank');
    },
    skiplocal(url){
      sessionStorage.removeItem("detail");
      location.href = url;
    },
    currentClick(index) {
      this.activeIndex = index;
      // this.getDocsSecondLevels(index);
    },
    childrenCurrentClick(index, idx) {
      this.childrenActiveIndex = idx;
      this.activeIndex = index;
    },
    pageJump(id) {
      this.titleClickScroll = true;
      //这里我与原作者的不太一样，发现原作者的scrollTop一直为0，所以使用了Vuetify自带的goTo事件
      this.$emit('callFather', id);
      // this.$vuetify.goTo(this.$el.querySelector('#app').offsetTop - 40);
      // setTimeout(() => (this.titleClickScroll = false), 100);
    },
    getDocsSecondLevels(parentActiveIndex) {
      let idx = parentActiveIndex;
      let secondLevels = [];
      let navChildren = this.navList[idx].children;

      if (navChildren.length > 0) {
        secondLevels = navChildren.map((item) => {
          let tar = item.title.replace(/^\s+|\s+$/g,"").replace(/、|：|（|）|\.|\/|:|，|\[|]/g, "").replace(/\ /g, "-").toLowerCase();
          return document.getElementById(tar).scrollIntoView();
        });
        this.docsSecondLevels = secondLevels;
      }
    },
  }
}
</script>

<style scoped>
  .el-menu{
    box-shadow: 0 4px 4px rgba(0, 0, 0, .30), 0 0 6px rgba(0, 0, 0, .04);
  }
  .el-menu-vertical-up {
    height: 440px;
    position: fixed;
    width: 230px;
  }
  .el-menu-vertical-down {
    margin-top: 440px;
    position: fixed;
    width: 230px;
    height: 310px;
    overflow: hidden;
  }
  .el-aside {
    margin-bottom: 20px;
    margin-left: 14%;
  }
  .el-menu-item:hover {
    color: #ffd04b !important;
  }
  a{
    text-decoration: none;
    color: white;
  }
  .el-footer {
    color: #333;
    text-align: center;
    line-height: 20px;
  }
  .blogtitlebox {
    text-align: center;
    font-size: 21px;
    font-weight: bold;
    color: white;
    height: 80px;
    background-color: #222222;
    line-height: 75px;
  }
  .blogtitle {
    display: inline-block;
    vertical-align: middle;
  }
  .mulu {
    text-align: center;
    font-weight: bold;
    color: #ffd04b;
    font-size: 17px;
    padding-top: 10px;
    cursor:pointer;
  }
  .mulu-detail {
    width: 230px;
    padding-bottom: 10px;
    font-size: 14px !important;
    font-weight: bold;
    line-height:40px;
    overflow-y: auto;
    overflow-x: auto;
    color: white;
    height: 210px !important;
  }
  .mulu-detail::-webkit-scrollbar{
    background: #545C64;
    width:9px
  }
  .mulu-detail::-webkit-scrollbar-thumb {
    background: #545C64;
    border-radius: 5px;
  }
  .mulu-detail::-webkit-scrollbar-thumb:hover{
    background: #909399;
  }
  .mulu-detail p{
    width: 170px;
  }
  .el-menu-item.is-active {
    background: rgb(67, 74, 80) !important;
  }
  .el-submenu__title.is-active {
    background: #6db6ff !important;
  }
  .el-dropdown {
    float: right;
  }
  a {
    text-decoration: none;
  }
  .activeChildren {
    color: #ffd04b;
    font-size: 15px;
    font-weight: bold;
  }
  .activeChildren p{
    color: #ffd04b;
    font-size: 15px;
    font-weight: bold;
  }
  .active {
    color: #ffd04b !important;
    font-weight: bold;
    font-size: 16px;
  }
  .nav-list {
    padding-left: 7px;
    font-size: 13px;
    line-height: 1.7em;
  }
</style>
