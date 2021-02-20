<template>
  <el-container>
    <title>请叫我算术嘉の博客 | {{$t('common.home')}}</title>
    <NewMenu></NewMenu>
    <el-main>
      <div v-if="this.$store.state.Canvas">
        <vue-canvas-nest></vue-canvas-nest>
      </div>
      <div id="apphome">
<!--        <el-dropdown>-->
<!--          <span class="el-dropdown-link">-->
<!--            {{$t('common.lang')}}<i class="el-icon-arrow-down el-icon&#45;&#45;right"></i>-->
<!--          </span>-->
<!--        <el-dropdown-menu slot="dropdown">-->
<!--        <el-dropdown-item @click.native = "switchLang('zh')">{{$t('common.lang-zh')}}</el-dropdown-item>-->
<!--        <el-dropdown-item @click.native = "switchLang('en')">{{$t('common.lang-en')}}</el-dropdown-item>-->
<!--        </el-dropdown-menu>-->
<!--        </el-dropdown>-->
        <el-button class="setting" size="medium" type="text" icon="el-icon-s-tools" @click="drawer = true">{{$t('common.setting')}}</el-button>
        <div class="drawer-style">
          <el-drawer
            :title="$t('common.setting')"
            :visible.sync="drawer"
            :direction="direction"
            >
            <div class="langSelect">
              <p>{{$t('common.lang')}}</p>
              <el-radio v-model="radio" @change="switchLang" label="zh">{{$t('common.lang-zh')}}</el-radio>
              <el-radio v-model="radio" @change="switchLang" label="en">{{$t('common.lang-en')}}</el-radio>
            </div>
            <br>
            <div class="calendar-style">
              <p>{{$t('common.calendar')}}</p>
              <el-tooltip class="item" effect="dark" content="点击打开日历" placement="right">
                <el-button type="text" icon="el-icon-date" @click="innerDrawer = true" style="font-size: 20px"></el-button>
              </el-tooltip>
            </div>
            <br>
            <div class="color-style">
              <p>{{$t('common.color')}}</p>
              <el-color-picker
                v-model="color1"
                size="mini"
                show-alpha
                :predefine="predefineColors"
              ></el-color-picker>
            </div>
             <el-drawer
               :title="$t('common.calendar')"
               :append-to-body="true"
               :before-close="handleClose"
               :visible.sync="innerDrawer">
               <el-calendar v-model="value">
               </el-calendar>
             </el-drawer>
             <br>
             <div class="langSelect">
              <p>{{$t('common.canvas')}}</p>
              <el-switch
                @change="changeCanvas"
                v-model="canvasNest">
              </el-switch>
            </div>
          </el-drawer>
        </div>
<!--        <img src="../assets/logo.png">-->
        <div style="padding-top: 295px;text-align: center">
          <span style="font-size: large">{{$t('common.home-word-up')}}</span>
          <el-divider></el-divider>
          <span style="font-size: large">{{$t('common.home-word-down')}}</span>
        </div>
        <br>
        <br>
        <br>
        <br>
        <br>
        <p style="text-align: center;"><a style="text-decoration: none;font-size: large; color: #2C3E50"  href="https://www.guanacossj.com" target="_blank">https://www.guanacossj.com</a></p>
<!--        <el-link :underline="false" href="https://www.guanacossj.com" style="font-size: large" target="_blank">https://www.guanacossj.com</el-link>-->
      </div>
    </el-main>
  </el-container>
</template>

<script>
    import Me from "./Archive";
    import Menu from "./Menu";
    import NewMenu from "./NewMenu";
    export default {
      name: "Home",
      components: { Me, NewMenu },
      data () {
          return {
            circleUrl: "https://www.guanacossj.com/media/jia/IMG_0323.JPG",
            reverse: true,
            drawer: false,
            innerDrawer: false,
            direction: 'rtl',
            canvasNest: this.$store.state.Canvas,
            radio: this.$i18n.locale,
            value: new Date(),
            color1: '#4D4D4D',
            predefineColors: [
              '#ff4500',
              '#ff8c00',
              '#ffd700',
              '#90ee90',
              '#00ced1',
              '#1e90ff',
              '#c71585',
              'rgba(255, 69, 0, 0.68)',
              'rgb(255, 120, 0)',
              'hsv(51, 100, 98)',
              'hsva(120, 40, 94, 0.5)',
              'hsl(181, 100%, 37%)',
              'hsla(209, 100%, 56%, 0.73)',
              '#c7158577'
            ],
            activities: [{
              content: '活动按期开始',
              timestamp: '2018-04-15'
            }, {
              content: '通过审核',
              timestamp: '2018-04-13'
            }, {
              content: '创建成功',
              timestamp: '2018-04-11'
            }],
            langOptions: [{
              value: 'zh',
              label: this.$t('common.lang-zh')
            }, {
              value: 'en',
              label: this.$t('common.lang-en')
            }],
          }
        },
        mounted() {
          document.title = '请叫我算术嘉の博客 | ' + this.$t('common.home');
        },
        watch: {
          '$i18n.locale'(newVal,oldVal) {
            document.title = '请叫我算术嘉の博客 | ' + this.$t('common.home');
          }
        },
        methods: {
          changeCanvas() {
            this.$store.state.Canvas = this.canvasNest;
          },
          handleClose(done) {
            this.$confirm(this.$t('common.Love.close'))
              .then(_ => {
                done();
              })
              .catch(_ => {});
          },
          handleOpen(key, keyPath) {
            console.log(key, keyPath);
          },
          handleCommand(command) {
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
    /*text-align: center;*/
    color: #4d4d4d;
    margin-top: 0;
  }
  .el-dropdown {
    /*float: right;*/
  }
  .el-dropdown-link {
    cursor: pointer;
  }
  .el-icon-arrow-down {
    font-size: 12px;
  }
  .setting {
    float: right;
    padding: 0;
  }
  .langSelect {
    margin-left: 20px;
  }
  .calendar-style {
    margin-left: 20px;
  }
  .color-style {
    margin-left: 20px;
  }
  .demonstration {
    font-size: 14px;
  }
  .el-drawer__body {
    color: #4d4d4d;
  }
  .drawer-style >>> .el-button {
    color: #4d4d4d;
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
  }
</style>
