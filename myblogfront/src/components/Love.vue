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
      <div id="appabout">
        <div class="grid-content bg-puprple-light">
            <div class="block">
<!--              <span class="demonstration" style="font-size: larger">祎祎大宝贝</span>-->
              <h2>嘉嘉の祎祎大宝贝</h2>
              <el-carousel :height="bannerHeight+'px'" >
                <el-carousel-item v-for="item in imgUrls" :key="item">
                  <img
                    ref="bannerHeight"
                    @load="imgLoad" style="width: 100%"
                    :src="item"
                  >
                </el-carousel-item>
              </el-carousel>
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
                        {{activity.content}}
                      </el-timeline-item>
                    </el-timeline>
                  </div>
                  </div>
                  <br>
              </el-col>
            </el-row>
        </div>
        </div>
        <div class="grid-content bg-puprple-light">
            <el-row type="flex" class="row-bg" justify="space-around">
              <el-col :span="20">
                <div class="grid-content bg-puprple-light">
                  <h2>{{$t('common.Love.down-list')}}</h2>
                  <div class="me">
                    <div class="me">
                    <div v-html="compiledMarkdownToDo"></div>
                  </div>
<!--                    <el-transfer-->
<!--                      style="text-align: left; display: inline-block"-->
<!--                      v-model="value4"-->
<!--                      filterable-->
<!--                      :left-default-checked="[2, 3]"-->
<!--                      :right-default-checked="[1]"-->
<!--                      :titles="['Source', 'Target']"-->
<!--                      :button-texts="['到左边', '到右边']"-->
<!--                      :format="{-->
<!--                        noChecked: '${total}',-->
<!--                        hasChecked: '${checked}/${total}'-->
<!--                      }"-->
<!--                      @change="handleChange"-->
<!--                      :data="data">-->
<!--                      <span slot-scope="{ option }">{{ option.key }} - {{ option.label }}</span>-->
<!--                      <el-button class="transfer-footer" slot="left-footer" size="small">操作</el-button>-->
<!--                      <el-button class="transfer-footer" slot="right-footer" size="small">操作</el-button>-->
<!--                    </el-transfer>-->
                  </div>
                  <br>
                </div>
              </el-col>
            </el-row>
        </div>
        <div class="grid-content bg-puprple-light">
            <el-row type="flex" class="row-bg" justify="space-around">
              <el-col :span="20">
                <div class="grid-content bg-puprple-light">
                  <h2>{{$t('common.Love.todo-list')}}</h2>
                  <div class="me">
                    <div v-html="compiledMarkdownDown"></div>
                  </div>
                </div>
              </el-col>
            </el-row>
        </div>
      </div>
      <el-backtop target=".el-main"></el-backtop>
    </el-main>
  </el-container>
</template>

<script>
  import echarts from "echarts";
  import "echarts-wordcloud/dist/echarts-wordcloud";
  import "echarts-wordcloud/dist/echarts-wordcloud.min";
  import Menu from "./Menu";
    export default {
        name: "Love",
        components: { Menu },
        data () {
          return {
            bannerHeight: "",
            output: "- 吃一次螺蛳粉\n" +
              "- 吃草莓味的DQ\n" +
              "- 夜游秦淮河",
            input: "- 拥抱\n" +
              "- 牵手\n" +
              "- 接吻\n" +
              "- 吃烤鸭\n" +
              "- 雍和宫还愿\n" +
              "- 爱国主义教育（圆明园\n" +
              "- 看电影",
            circleUrl: "https://www.guanacossj.com/media/jia/IMG_0323.JPG",
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
              content: '在一起',
              timestamp: '2020-11-07 20:20'
            },
            {
              content: '第一次见面（北京）',
              timestamp: '2020-12-21 19:31'
            }],
          }
        },
        mounted(){
          this.initChart();
          this.imgLoad();
            window.addEventListener('resize',() => {
                this.bannerHeight=this.$refs.bannerHeight[0].height;
                this.imgLoad();
            },false)
        },
        computed: {
          compiledMarkdownToDo: function() {
            return marked(this.input, { sanitize: true });
          },
          compiledMarkdownDown: function() {
            return marked(this.output, { sanitize: true });
          }
        },
        methods: {
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
          initChart() {
          // this.chart = echarts.init(document.getElementById("mywordcloud"));
          let chart = echarts.init(document.getElementById("mywordcloud"));
          let maskImage = new Image;
          maskImage.src = "data:image/png;base64,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";
          const option = {
            title: {
              text: "",
              x: "center"
            },
            backgroundColor: "#fff",
            // backgroundColor: "#B3C0D1",
            tooltip: {
              show: true
            },
            series: [
              {
                type: "wordCloud",
                //用来调整词之间的距离
                gridSize: 6,
                shape:'smooth',  //平滑
                //用来调整字的大小范围
                // Text size range which the value in data will be mapped to.
                // Default to have minimum 12px and maximum 60px size.
                sizeRange: [12, 60],
                // Text rotation range and step in degree. Text will be rotated randomly in range [-90,                                                                             90] by rotationStep 45
                //用来调整词的旋转方向，，[0,0]--代表着没有角度，也就是词为水平方向，需要设置角度参考注释内容
                // rotationRange: [-45, 0, 45, 90],
                // rotationRange: [ 0,90],
                rotationRange: [0, 0],
                //随机生成字体颜色
                maskImage: maskImage,
                textStyle: {
                  normal: {
                    color: function() {
                      return (
                        "rgb(" +
                        Math.round(Math.random() * 255) +
                        ", " +
                        Math.round(Math.random() * 255) +
                        ", " +
                        Math.round(Math.random() * 255) +
                        ")"
                      );
                    }
                  }
                },
                //位置相关设置
                // Folllowing left/top/width/height/right/bottom are used for positioning the word cloud
                // Default to be put in the center and has 75% x 80% size.
                left: null,
                top: null,
                right: null,
                bottom: null,
                width: "150%",
                height: "150%",
                //数据
                data: this.worddata,
                // data: this.randomworddata
              }
            ]
          };
          // this.chart.setOption(option);
          chart.setOption(option);
          maskImage.onload = function () {
            chart.setOption(option);
          };
          // window.onresize("resize",function(){
          //   chart.resize();
          // });
        },
        }
    }
</script>

<style scoped>
  .el-menu{
    box-shadow: 0 4px 4px rgba(0, 0, 0, .30), 0 0 6px rgba(0, 0, 0, .04)
  }
  .el-main{
    /*margin-right: 150px; */
    margin-right: 10%;
  }
  #appabout {
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
  .blogtitle {
    display: inline-block;
    vertical-align: middle;
  }
  .myname {
    text-align: center;
    font-size: 16px;
    font-weight: bold;
    color: white;
  }
  .mypic {
    text-align: center;
  }
  #tag-sign{
    text-align: center;
    font-size: small;
    color: #cdcdcd;
  }
  .tag-links{
    height: 45px;
    text-align: center;
    font-size: 14px;
    line-height:45px;
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
  .el-menu-item.is-active {
    background: rgb(67, 74, 80) !important;
  }
  .el-submenu__title.is-active {
    background: #6db6ff !important;
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

</style>
