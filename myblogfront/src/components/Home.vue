<template>
  <el-container>
    <title>请叫我算术嘉の博客 | {{$t('common.home')}}</title>
    <Menu></Menu>
    <el-main>
      <vue-canvas-nest></vue-canvas-nest>
      <div id="apphome">
        <el-dropdown>
          <span class="el-dropdown-link">
            {{$t('common.lang')}}<i class="el-icon-arrow-down el-icon--right"></i>
          </span>
        <el-dropdown-menu slot="dropdown">
        <el-dropdown-item @click.native = "switchLang('zh')">{{$t('common.lang-zh')}}</el-dropdown-item>
        <el-dropdown-item @click.native = "switchLang('en')">{{$t('common.lang-en')}}</el-dropdown-item>
        </el-dropdown-menu>
        </el-dropdown>
        <img src="../assets/logo.png">
        <br>
        <br>
        <br>
        <br>
        <br>
        <br>
        <br>
        <br>
        <p></p>
          <div>
            <span style="font-size: large">{{$t('common.home-word-up')}}</span>
            <el-divider></el-divider>
            <span style="font-size: large">{{$t('common.home-word-down')}}</span>
            </div>
        <br>
        <br>
        <br>
        <br>
        <br>
        <p><a style="text-decoration: none;font-size: large; color: #2C3E50"  href="https://www.guanacossj.com" target="_blank">https://www.guanacossj.com</a></p>
<!--        <el-link :underline="false" href="https://www.guanacossj.com" style="font-size: large" target="_blank">https://www.guanacossj.com</el-link>-->
      </div>
    </el-main>
  </el-container>
</template>

<script>
    import Me from "./Archive";
    import Menu from "./Menu";
    export default {
      name: "Home",
      components: { Me, Menu },
      data () {
          return {
            circleUrl: "https://www.guanacossj.com/media/jia/IMG_0323.JPG",
            reverse: true,
            activities: [{
              content: '活动按期开始',
              timestamp: '2018-04-15'
            }, {
              content: '通过审核',
              timestamp: '2018-04-13'
            }, {
              content: '创建成功',
              timestamp: '2018-04-11'
            }]
          }
        },
        watch: {
          '$i18n.locale'(newVal,oldVal) {
            document.title = '请叫我算术嘉の博客 | ' + this.$t('common.home')
          }
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
          handleCommand(command) {
            console.log(command)
            this.switchLang(command)
          },
          switchLang(val){
            this.$i18n.locale=val;//此处val为 zh 或者 en
            sessionStorage.setItem('lang', val);
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
  .el-menu{
    box-shadow: 0 4px 4px rgba(0, 0, 0, .30), 0 0 6px rgba(0, 0, 0, .04)
  }
  .el-main{
    /*margin-right: 150px;*/
    /*margin-right: 12%;*/
  }
  #apphome {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    /*color: #2c3e50;*/
    color: #4d4d4d;
    margin-top: 0;
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
</style>
