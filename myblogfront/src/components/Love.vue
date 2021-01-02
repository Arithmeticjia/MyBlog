<template>
  <el-container class="layout-container">
    <Menu></Menu>
    <el-main>
      <el-dropdown style="float:left;">
          <span class="el-dropdown-link">
            {{$t('common.Love.user')}} {{ username }}<i class="el-icon-arrow-down el-icon--right"></i>
          </span>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item @click.native="toLogout">退出</el-dropdown-item>
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
<!--              <span class="demonstration" style="font-size: larger">祎祎大宝贝</span>-->
              <h2>{{$t('common.Love.baby')}}</h2>
              <el-carousel :height="bannerHeight+'px'" >
                <el-carousel-item v-for="item in imgUrls" :key="item">
                  <img
                    ref="bannerHeight"
                    @load="imgLoad" style="width: 50%"
                    :src="item"
                  >
                </el-carousel-item>
              </el-carousel>
<!--              <el-carousel :interval="4000" type="card" height="200px">-->
<!--                  <el-carousel-item v-for="item in imgUrls" :key="item">-->
<!--                    <img-->
<!--                    ref="bannerHeight"-->
<!--                    @load="imgLoad" style="width: 50%"-->
<!--                    :src="item"-->
<!--                  >-->
<!--                  </el-carousel-item>-->
<!--              </el-carousel>-->
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
        </div>
        <div class="grid-content bg-puprple-light" v-loading="loading">
            <el-row type="flex" class="row-bg" justify="space-around">
              <el-col :span="20">
                <div class="grid-content bg-puprple-light">
                  <h2>{{$t('common.Love.down-list')}}</h2>
                  <div class="me">
                    <div class="me" v-for="value in downList">
                    <div v-html="compiledMarkdownNew(value.content)"></div>
                  </div>
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
                  <div class="me">
                    <div class="me" v-for="value in todoList">
                    <div v-html="compiledMarkdownNew(value.content)"></div>
                  </div>
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
  import Menu from "./Menu";
    export default {
        name: "Love",
        components: { Menu },
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
            output: "- 吃一次螺蛳粉\n" +
              "- 吃草莓味的DQ\n" +
              "- 夜游秦淮河\n" +
              "- 吃一次火锅",
            input: "- 拥抱\n" +
              "- 牵手\n" +
              "- 接吻\n" +
              "- 吃烤鸭\n" +
              "- 雍和宫还愿\n" +
              "- 爱国主义教育（圆明园\n" +
              "- 看电影",
            imgUrls: [
              'https://www.guanacossj.com/media/fzy/189531609426993_.pic_hd.jpg',
              'https://www.guanacossj.com/media/fzy/189521609426989_.pic_hd.jpg',
            ],
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
            },
            {
              content: '第一次见面（北京）',
              timestamp: '2020-12-21 19:31'
            },
            {
              content: '第一次抱着睡💤',
              timestamp: '2020-12-23 22:50'
            }],
          }
        },
        mounted(){
          this.getToDOList();
          this.getDownList();
          this.imgLoad();
            window.addEventListener('resize',() => {
                this.bannerHeight=this.$refs.bannerHeight[0].height * 0.5;
                this.imgLoad();
            },false)
        },
        computed: {
          compiledMarkdownToDo: function() {
            return marked(this.input, { sanitize: true });
          },
          compiledMarkdownNew() {
            return function (value) {
              return marked(value, {sanitize: true});
            }
          },
          compiledMarkdownDown: function() {
            return marked(this.output, { sanitize: true });
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
                console.log(this.$refs.bannerHeight[0].height);
            })
          },
          skip(url){
           window.open(url, target='_blank')
          },
          update: _.debounce(function(e) {
            this.input = e.target.value;
          }, 300),
          switchLang(val){
            this.$i18n.locale=val;//此处val为 zh 或者 en
          },
          handleOpen(key, keyPath) {
            console.log(key, keyPath);
          },
          skiplocal(url){
            location.href = url
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
                      message: `添加成功!`
                    });
                    this.getDownList();
                    this.getToDOList();
                  }else {
                    this.$message({
                      type: 'error',
                      message: `服务器出了点问题，请稍后重试!`
                    });
                  }
                });
              } else {
                console.log('error submit!!');
                return false
              }
            })
          },
          async getToDOList() {
            try {
              const {data} = await axios.get("https://www.guanacossj.com/blog/getlovefzytodo/");
              this.todoList = data;
              this.loading = false;
            } catch (e) {
              this.$message.error("请求用户数据失败，请稍后再试！");
            }
          },
          async getDownList() {
            try {
              const {data} = await axios.get("https://www.guanacossj.com/blog/getlovefzydown/");
              this.downList = data;
              this.loading = false;
            } catch (e) {
              this.$message.error("请求用户数据失败，请稍后再试！");
            }
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
  .el-main{
    /*margin-right: 150px; */
    margin-right: 10%;
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
    /*background: #4D4D4D;*/
    width: 100%;
    height: 100%;
    text-align: left;
    /*color: white;*/
    /*padding: 10px;*/
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
