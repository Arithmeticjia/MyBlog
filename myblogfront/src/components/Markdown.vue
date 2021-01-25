<template>
  <el-aside width="230px">
      <el-menu
        :default-active="$route.path"
        class="el-menu-vertical-demo"
        background-color="#545c64"
        text-color="#fff"
        active-text-color="#ffd04b"
        style="height: 440px">
        <div class="blogtitlebox">
          <div class="blogtitle">{{$t('common.blog-name')}}</div>
        </div>
        <br>
      <el-menu-item index="/home" @click="skiplocal('/home')">
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
      <el-menu-item index="/category" @click="skiplocal('/category')">
        <i class="el-icon-menu"></i>
        <span slot="title" style="font-weight: bold">{{$t('common.category')}}</span>
      </el-menu-item>
      <el-menu-item index="/list" @click="skiplocal('/list')">
        <i class="el-icon-search"></i>
        <span slot="title" style="font-weight: bold">{{$t('common.search')}}</span>
      </el-menu-item>
      <el-menu-item index="/about" @click="skiplocal('/about')">
        <i class="el-icon-user"></i>
        <span slot="title" style="font-weight: bold">{{$t('common.about')}}</span>
      </el-menu-item>
        <el-menu-item index="/love" @click="skiplocal('/love')">
        <i class="el-icon-ice-cream"></i>
        <span slot="title" style="font-weight: bold">{{$t('common.love')}}</span>
      </el-menu-item>
    </el-menu>
      <p></p>
      <el-menu
      class="el-menu-vertical-demo"
      background-color="#545c64"
      text-color="#fff">
          <p class="mulu">{{$t('common.index')}}</p>
          <div class="mulu_detail">
            <ul>
            <div style="color: #fff" v-for="(nav, index) in psMsg" :key="index"  @click="currentClick(index)"> <a href="javascript:" :class="{ 'active': activeIndex === index}" @click="pageJump(nav.title)">{{ nav.title }}</a>
             <div v-if="nav.children.length &gt; 0" class="menu-children-list" style="color: #fff">
              <div class="nav-list" style="color: #fff">
               <p style="color: #fff" v-for="(item, idx) in nav.children" :key="idx"  @click.stop="childrenCurrentClick(index, idx)"> <a href="javascript:" :class="{ 'activeChildren': ((childrenActiveIndex === idx) && (activeIndex === index))}" @click="pageJump(item.title)">{{ item.title }}</a></p>
              </div>
             </div>
            </div>
           </ul>
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
      navList: this.psMsg
    }
  },
  props: {
    psMsg: Array,
  },
  mounted() {
  },
  methods: {
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
      console.log(index, idx)
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
    box-shadow: 0 4px 4px rgba(0, 0, 0, .30), 0 0 6px rgba(0, 0, 0, .04)
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
    /*align-items: center;*/
    /*top:50%;*/
    /*position: absolute;*/
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
    font-size: 18px;
    padding-top: 15px;
  }
  .mulu_detail {
    width: 205px;
    padding-top: 10px;
    padding-bottom: 25px;
    font-size: 14px;
    font-weight: bold;
    line-height:25pt;
    color: white !important;
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
  .active {
    color: #ffd04b !important;
    font-weight: bold;
    font-size: 16px;
  }
  .nav-list {
    padding-left: 7px;
  }
</style>
