<template>
  <el-container>
    <title>请叫我算术嘉の博客 | {{$t('common.love')}}</title>
    <NewMenu></NewMenu>
    <el-main>
      <div v-if="this.$store.state.Canvas">
        <vue-canvas-nest></vue-canvas-nest>
      </div>
      <el-dropdown style="float:left;">
          <span class="el-dropdown-link">
            {{$t('common.Love.user')}} {{ username }}<i class="el-icon-arrow-down el-icon--right"></i>
          </span>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item @click.native="toLogout">{{$t('common.Login.logout')}}</el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
      <el-dropdown>
          <span class="el-dropdown-link">
            {{$t('common.lang')}}<i class="el-icon-arrow-down el-icon--right"></i>
          </span>
        <el-dropdown-menu slot="dropdown">
        <el-dropdown-item @click.native = "switchLang('zh')">{{$t('common.lang-zh')}}</el-dropdown-item>
        <el-dropdown-item @click.native = "switchLang('en')">{{$t('common.lang-en')}}</el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
      <div id="applove">
        <div class="grid-content bg-puprple-light">
          <div class="block">
            <h2>{{$t('common.Love.baby')}}</h2>
            <el-carousel :height="bannerHeight+'px'" >
              <el-carousel-item v-for="item in imgUrls" :key="item">
                <img
                  ref="bannerHeight"
                  @load="imgLoad"
                  style="width: 50%;"
                  :src="item"
                >
              </el-carousel-item>
            </el-carousel>
          </div>
        </div>
        <br>
        <div class="grid-content bg-puprple-light">
          <el-row type="flex" class="row-bg" justify="space-around">
            <el-col :span="20">
              <div class="grid-content bg-puprple-light">
                <h2>{{$t('common.Love.timeline')}}</h2>
                <div class="me">
                  <el-timeline :reverse="reverse">
                    <el-timeline-item
                      v-for="(activity, index) in activities"
                      :key="index"
                      :timestamp="activity.timestamp">
                      {{ activity.content }}
                    </el-timeline-item>
                  </el-timeline>
                </div>
              </div>
              <br>
            </el-col>
          </el-row>
        </div>
        <div class="grid-content bg-puprple-light">
          <el-row type="flex" class="row-bg" justify="space-around">
            <el-col :span="20">
              <div class="grid-content bg-puprple-light">
                <h2>{{$t('common.Love.poetry')}}</h2>
                <br>
                <div class="me">
                  <el-collapse>
                    <el-collapse-item title="To 范子祎" name="1">
                      <div style="font-size: 16px;color: #4d4d4d">
                        <p>原谅我不善言辞</p>
                        <p>只好在电脑上先打好草稿</p>
                        <p>你说你不喜欢标点符号</p>
                        <p>于是这就变成一首情诗</p>
                        <p>原谅我不善言辞</p>
                        <p>只好在电脑上先打好草稿</p>
                        <p>你说你不喜欢标点符号</p>
                        <p>于是这就变成一首情诗</p>
                        <p>文字不停地打了又删</p>
                        <p>伴随我的思绪回到从前</p>
                        <p>从未想过是这样一个开始</p>
                        <p>变得一发不可收拾</p>
                        <p>于人山人海中</p>
                        <p>随时间无涯的荒野</p>
                        <p>不早不晚</p>
                        <p>我们相遇了</p>
                        <p>梦里有你热烈的吻</p>
                        <p>我希望永远不要醒来</p>
                        <p>我以为五千年的中华文化所孕育出来的文字已足够成熟细腻</p>
                        <p>提笔却无法描述对你喜爱的万分之一</p>
                        <p>这份爱与思念</p>
                        <p>跨越1075.7公里（常州到北京）</p>
                        <p>只想紧紧抱住你</p>
                        <p>我是一个坚定的无神论者</p>
                        <p>佛前许下的每一个愿望都与你有关</p>
                        <p>你总说我想的太远</p>
                        <p>因为我没有你的日子会是难以想象的灾难</p>
                        <p>未来的日子很长</p>
                        <p>与你在一起</p>
                        <p>都是好时光</p>
                      </div>
                    </el-collapse-item>
                  </el-collapse>
                </div>
                <br>
              </div>
              <br>
            </el-col>
          </el-row>
        </div>
        <div class="grid-content bg-puprple-light" v-loading="loading">
            <el-row type="flex" class="row-bg" justify="space-around">
              <el-col :span="20">
                <div class="grid-content bg-puprple-light">
                  <h2>{{$t('common.Love.down-list')}}</h2>
                  <div class="me" v-for="value in downList">
                    <div v-html="compiledMarkdownDown(value.content)"></div>
                  </div>
                  <br>
                </div>
              </el-col>
            </el-row>
        </div>
        <div class="grid-content bg-puprple-light" v-loading="loading">
            <el-row type="flex" class="row-bg" justify="space-around">
              <el-col :span="20">
                <div class="grid-content bg-puprple-light">
                  <h2>{{$t('common.Love.todo-list')}}</h2>
                  <div class="me" v-for="value in todoList">
                    <div v-html="compiledMarkdownToDo(value.content)"></div>
                  </div>
                </div>
              </el-col>
            </el-row>
        </div>
        <el-button style="padding: 3px 0" type="text" @click="dialogFormVisible = true">{{$t('common.Love.click-to-add')}}</el-button>
        <!--编辑弹框-->
        <el-dialog :title="$t('common.Love.add')" :visible.sync="dialogFormVisible" :before-close="handleClose" width="40%">
          <el-form :model="form" :rules="rules" ref="form" :label-position="labelPosition" label-width="80px">
            <el-form-item :label="$t('common.Love.content')" prop="content">
              <el-input v-model="form.content" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item :label="$t('common.Love.type')" prop="type">
              <el-select v-model="form.type" :placeholder="$t('common.Love.placeholder')">
                <el-option :label="$t('common.Love.down-list')" value=0></el-option>
                <el-option :label="$t('common.Love.todo-list')" value=1></el-option>
                <el-option :label="$t('common.Love.timeline')" value=2></el-option>
              </el-select>
            </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button @click="dialogFormVisible = false">{{$t('common.Love.cancel')}}</el-button>
              <el-button type="primary" @click="submitForm('form')">{{$t('common.Love.confirm')}}</el-button>
            </div>
          </el-dialog>
      </div>
      <el-backtop target=".el-main"></el-backtop>
    </el-main>
  </el-container>
</template>

<script>
  import store from '../store';
  import axios from 'axios';
  import NewMenu from "./NewMenu";
  import { marked } from 'marked';
  import request from '@/utils/request'
    export default {
        name: "Love",
        components: { NewMenu },
        data () {
          return {
            username: store.getters.userName,
            loading: true,
            bannerHeight: "",
            dialogFormVisible: false,
            form: {
              content: '- ',
              type: '',
            },
            labelPosition: 'right',
            rules: {
              content: [
                {required: true, message: this.$t('common.Love.placeholder'), trigger: 'blur'},
                {min: 3, max: 20, message: this.$t('common.Love.length'), trigger: 'blur'}
              ],
              type: [
                {required: true, message: this.$t('common.Love.placeholder'), trigger: 'blur'},
                {min: 1, max: 1, message: this.$t('common.Love.length'), trigger: 'blur'}
              ],
            },
            downList: [],
            todoList: [],
            imgUrls: [
              'https://www.guanacossj.com/media/fzy/189531609426993_.pic_hd.jpg',
              'https://www.guanacossj.com/media/fzy/189521609426989_.pic_hd.jpg',
            ],
            poetry: '',
            reverse: false,
            activities: [{
              content: '牛客第一次对话',
              timestamp: '2020-10-21 14:58'
            }, {
              content: '加微信',
              timestamp: '2020-10-27 09:19'
            }, {
              content: '(๑′ᴗ‵๑)Ｉ Lᵒᵛᵉᵧₒᵤ❤在一起',
              timestamp: '2020-11-07 20:20'
            }, {
              content: '第一次见面（北京）',
              timestamp: '2020-12-21 19:31'
            }, {
              content: '第一次抱着睡💤',
              timestamp: '2020-12-23 22:50'
            }],
          }
        },
        beforeMount() {
          this.checkLogin();
        },
        mounted(){
          this.imgLoad();
          window.addEventListener('resize',() => {
            this.bannerHeight=this.$refs.bannerHeight[0].height * 0.5;
            this.imgLoad();
          },false)
          document.title = '请叫我算术嘉の博客 | ' + this.$t('common.love');
        },
        computed: {
          compiledMarkdownDown() {
            return function (value) {
              const htmlStr = marked(value, {
		              sanitize: true,
		          });
              return htmlStr.replace('<li>','').replace('</li>','')
              // return `<ul><input checked disabled type="checkbox">` + value + `</ul>`
            }
          },
          compiledMarkdownToDo() {
            return function (value) {
              const htmlStr = marked(value, {
		              sanitize: true,
		          });
              return htmlStr.replace('<li>','').replace('</li>','')
              // return `<ul><input disabled="" type="checkbox">` + value + `</ul>`
            }
          },
        },
        watch: {
          '$i18n.locale'(newVal, oldVal) {
            document.title = '请叫我算术嘉の博客 | ' + this.$t('common.love');
          }
        },
        methods: {
          toLogout() {
            localStorage.removeItem('Authorization');
            localStorage.removeItem('Username');
            this.$router.push(
              {
                path: "/login",
              }
            )
          },
          handleClose(done) {
            this.$confirm(this.$t('common.Love.close'))
              .then(_ => {
                done();
              })
              .catch(_ => {});
          },
          imgLoad(){
            this.$nextTick(()=>{
              this.bannerHeight=this.$refs.bannerHeight[0].height;
            })
          },
          switchLang(val){
            this.$i18n.locale=val;//此处val为 zh 或者 en
            sessionStorage.setItem('lang', val);
          },
          submitForm(formname) {
            this.$refs[formname].validate(valid => {
              if (valid) {
                this.loading = true;
                axios({
                  method: "post",
                  url: "https://www.guanacossj.com/blog/postlovefzy/",
                  headers: {
                    'Content-Type': 'application/json'
                  },
                  withCredentials: false,
                  data: this.form
                }).then((res)=>{
                  if(res.status === 200){
                    this.loading = false;
                    this.dialogFormVisible = false;
                    this.$message({
                      type: 'success',
                      message: `添加成功!`,
                      center: true
                    });
                    this.getDownList();
                    this.getToDOList();
                  } else {
                    this.$message({
                      type: 'error',
                      message: `服务器出了点问题，请稍后重试!`,
                      center: true
                    });
                  }
                });
              } else {
                console.log('error submit!!');
                return false
              }
            })
          },
          async checkLogin() {
            try {
              let ans = await request({
                url: "yunprophet/api/v1/check-login",
                headers: {
                'token': localStorage.getItem('Authorization')
              }});
              if (ans.data.code === 200) {
                await this.getDownList();
                // await this.getToDOList();
                await this.getToDOListNew();
              } else {
                this.$message.error({
                  message: '凭证已过期，请重新登录！',
                  center: true
                });
                await this.$router.push({
                  path: "/login",
                });
              }
            } catch (e) {
              this.$message.error({
                message: '页面出错了，请稍后再试！',
                center: true
              });
            }
          },
          async getToDOListNew() {
            try {
              const {data} = await request({
                baseURL: 'https://www.guanacossj.com',
                url: '/blog/getlovefzytodo/',
                method: 'get',
                headers: {
                  'Content-Type': 'application/json'
                },
              })
              this.todoList = data;
              this.loading = false;
            } catch (e) {
              this.$message.error({
                message: '请求用户数据失败，请稍后再试！',
                center: true
              });
            }
          },
          async getToDOList() {
            try {
              const {data} = await axios.get("https://www.guanacossj.com/blog/getlovefzytodo/");
              this.todoList = data;
              this.loading = false;
            } catch (e) {
              this.$message.error({
                message: '请求用户数据失败，请稍后再试！',
                center: true
              });
            }
          },
          async getDownList() {
            try {
              const {data} = await axios.get("https://www.guanacossj.com/blog/getlovefzydown/");
              this.downList = data;
              this.loading = false;
            } catch (e) {
              this.$message.error({
                message: '请求用户数据失败，请稍后再试！',
                center: true
              });
            }
          },
        }
    }
</script>

<style scoped>
  .el-main{
    /*margin-right: 150px; */
    /*margin-right: 12%;*/
  }
  #applove {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    /*color: #2c3e50;*/
    color: #4d4d4d;
    margin-top: 30px;
  }
  .me {
    background: #fff;
    width: 100%;
    height: 100%;
    text-align: left;
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
  .row-bg {
    padding: 10px 0;
    /*background-color: #f9fafc;*/
    background-color: rgba(255, 255, 255, 0);
    /*box-shadow: 0 2px 4px rgba(0, 0, 0, .20), 0 0 6px rgba(0, 0, 0, .04)*/
    box-shadow: 0 4px 4px rgba(0, 0, 0, .30), 0 0 6px rgba(0, 0, 0, .04)
  }
  .grid-content {
    border-radius: 4px;
    min-height: 36px;
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
  .layout-container {
    height: 100%;
  }
  .el-carousel__item h3 {
    color: #475669;
    font-size: 14px;
    opacity: 0.75;
    line-height: 150px;
    margin: 0;
  }

  .el-carousel__item:nth-child(2n) {
     background-color: #99a9bf;
  }

  .el-carousel__item:nth-child(2n+1) {
     background-color: #d3dce6;
  }
  .el-form {
    text-align: left;
  }

</style>
<style>
  .el-collapse-item__header {
    font-size: 16px !important;
    color: #4d4d4d !important;
  }
</style>
