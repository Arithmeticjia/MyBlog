<template>
    <div id="appvuedjango">
      <div id="mywordcloud" :style="{width: '1000px', height: '120px'}" :data="worddata" style="margin: 0 auto"></div>
      <el-row class="demo-avatar demo-basic">
        <el-col :span="12">
          <div class="sub-title"></div>
          <div class="demo-basic--circle">
            <div class="block"><el-avatar :size="50" :src="circleUrl"></el-avatar></div>
          </div>
        </el-col>
      </el-row>
      <img src="../assets/logo.png">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
      <img src="../assets/django_logo.png">
    <h1>{{ msg }}</h1>
    <div>
        <span><i class="el-icon-school">&nbsp;</i>南京邮电大学-本科-通信工程</span>
        <el-divider direction="vertical"></el-divider>
        <span>南京邮电大学-研究生-软件工程</span>
        <el-divider direction="vertical"></el-divider>
        <span><i class="el-icon-phone">&nbsp;</i>18351922995</span>
        <el-divider direction="vertical"></el-divider>
        <span><i class="el-icon-s-promotion">&nbsp;</i>bluesaltssj@gmail.com</span>
    </div>
      <ul>
        <li><h2>Home Page</h2>
          <ul>
            <li>
              <a
                href="https://www.guanacossj.com"
                target="_blank"
              >
                arithmeticjia
              </a>
            </li>
          </ul>
        </li>
        <li><h2>Demo Show</h2>
          <ul>
            <li>
              <a
                href="http://blog.guanacossj.com/#/bloglist"
                target="_blank"
              >
                bloglist
              </a>
            </li>
          </ul>
        </li>
      </ul>
      <el-button type="text" @click="dialogVisible = true"><h1>Who am i?</h1></el-button>
      <el-dialog
        title="我的名字叫"
        :visible.sync="dialogVisible"
        width="30%"
        :before-close="handleClose">
        <span style="font-size: 20px">单沙嘉(ShanShajia)</span>
        <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="dialogVisible = false">确 定</el-button>
        </span>
      </el-dialog>
  </div>
</template>

<script>
  import echarts from "echarts";
  import "echarts-wordcloud/dist/echarts-wordcloud";
  import "echarts-wordcloud/dist/echarts-wordcloud.min";
export default {
  name: 'HelloWorld',
  data () {
    return {
      circleUrl: "https://www.guanacossj.com/media/jia/IMG_0323.JPG",
      msg: 'Welcome to My Vue.js & Django App',
      dialogVisible: false,
      worddata: [
            {
              name: "Django",
              value: 14000
            },
            {
              name: "Vue.js",
              value: 9700
            },{
              name: "python",
              value: 8600
            },
            {
              name: "java",
              value: 7500
            },
            {
              name: "Hola",
              value: 7200
            },
            {
              name: "中华民族",
              value: 6300
            },
            {
              name: "Echarts",
              value: 6396
            },
            {
              name: "WordCloud",
              value: 6000
            },
            {
              name: "leetcode",
              value: 9000
            },
            {
              name: "帅",
              value: 8200
            },
            {
              name: "Ubuntu",
              value: 5000
            },
            {
              name: "SpringBoot",
              value: 4580
            },
            {
              name: "南京邮电大学",
              value: 4200
            },
            {
              name: "可口可乐",
              value: 4000
            },
            {
              name: "十九大",
              value: 3900
            },
            {
              name: "团结一致",
              value: 3500
            },
            {
              name: "arithmeticjia",
              value: 3570
            },
            {
              name: "实事求是",
              value: 3149
            },
            {
              name: "Hexo",
              value: 3190
            },
            {
              name: "Google",
              value: 3039
            },
            {
              name: "Wechat",
              value: 2900
            },
            {
              name: "Microsoft",
              value: 2800
            },
            {
              name: "Flask",
              value: 2600
            },
            {
              name: "Pytorch",
              value: 2500
            },
            {
              name: "Tensorflow",
              value: 2699
            },
            {
              name: "Chrome",
              value: 2402
            },
            {
              name: "Pycharm",
              value: 2050
            },
            {
              name: "从严治党",
              value: 3000
            },
            {
              name: "两学一做",
              value: 4060
            },
            {
              name: "爱党爱国",
              value: 1800
            },
            {
              name: "伟大复兴中国梦",
              value: 4650
            },
            {
              name: "中国特色社会主义",
              value: 5300
            },
            {
              name: "武汉加油",
              value: 1329
            },
            {
              name: "与你同在",
              value: 1300
            },
            {
              name: "薛定谔的猫",
              value: 1100
            },
            {
              name: "love",
              value: 1080
            },
            {
              name: "双缝干涉",
              value: 1070
            },
            {
              name: "天才和小可爱",
              value: 1060
            },
            {
              name: "HelloWorld",
              value: 3099
            },
            {
              name: "一国两制",
              value: 1000
            },
            {
              name: "apple music",
              value: 1010
            },
            {
              name: "mojave",
              value: 980
            },
            {
              name: "catalina",
              value: 980
            },
            {
              name: "lidata",
              value: 930
            },
            {
              name: "429",
              value: 900
            },
            {
              name: "Windows10",
              value: 980
            },
            {
              name: "MacOS",
              value: 1980
            },
            {
              name: "tornado",
              value: 990
            },
            {
              name: "facebook",
              value: 1000
            },
            {
              name: "CentOS",
              value: 710
            },
            {
              name: "IDEA",
              value: 697
            },
            {
              name: "Keras",
              value: 880
            },
            {
              name: "Marval",
              value: 869
            },
            {
              name: "Nike",
              value: 820
            },
            {
              name: "Bing",
              value: 810
            },
            {
              name: "Visual Studio Code",
              value: 800
            },
            {
              name: "Xcode",
              value: 800
            },
            {
              name: "世界杯",
              value: 719
            },
          ]
    };
  },
  mounted(){
        // 定时刷新页面
        this.initChart();
        if (this.timer) {
          clearInterval(this.timer)
        }else {
          this.timer = setInterval(()=>{
            this.initChart();
            },5000
          )
        }
        // this.initChart();
      },
  destroyed() {
    clearInterval(this.timer)
  },
  methods: {
    handleClose(done) {
        this.$confirm('确认关闭？')
          .then(_ => {
            done();
          })
          .catch(_ => {});
    },
    open() {
        this.$alert('单沙嘉', {
          confirmButtonText: '确定',
          callback: action => {
            this.$message({
              type: 'success',
              message: `联系我吧`
            });
          }
        });
      },
    initChart() {
          // this.chart = echarts.init(document.getElementById("mywordcloud"));
          let chart = echarts.init(document.getElementById("mywordcloud"));
          let maskImage = new Image;
          maskImage.src = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOUAAACCCAYAAAC5OA/0AAAEC0lEQVR4Xu3TsW0bURRE0c/ADShUH+7DBbgUFaFSVJVT5Y4MBgIEOBpwL8DgLKDscYc44r0dDwECTyVwe6pv48sQIHBE6UdA4MkERPlk/xBfh8BXlD/OOe8Bx+s559e39/4553wEO15JoBT4ec65/30999/w/bd89fN2zvn8HuXfqxe8jwCBSeBFlJOXYwK5gChzYgMENgFRbl6uCeQCosyJDRDYBES5ebkmkAuIMic2QGATEOXm5ZpALiDKnNgAgU1AlJuXawK5gChzYgMENgFRbl6uCeQCosyJDRDYBES5ebkmkAuIMic2QGATEOXm5ZpALiDKnNgAgU1AlJuXawK5gChzYgMENgFRbl6uCeQCosyJDRDYBES5ebkmkAuIMic2QGATEOXm5ZpALiDKnNgAgU1AlJuXawK5gChzYgMENgFRbl6uCeQCosyJDRDYBES5ebkmkAuIMic2QGATEOXm5ZpALiDKnNgAgU1AlJuXawK5gChzYgMENgFRbl6uCeQCosyJDRDYBES5ebkmkAuIMic2QGATEOXm5ZpALiDKnNgAgU1AlJuXawK5gChzYgMENgFRbl6uCeQCosyJDRDYBES5ebkmkAuIMic2QGATEOXm5ZpALiDKnNgAgU1AlJuXawK5gChzYgMENgFRbl6uCeQCosyJDRDYBES5ebkmkAuIMic2QGATEOXm5ZpALiDKnNgAgU1AlJuXawK5gChzYgMENgFRbl6uCeQCosyJDRDYBES5ebkmkAuIMic2QGATEOXm5ZpALiDKnNgAgU1AlJuXawK5gChzYgMENgFRbl6uCeQCosyJDRDYBES5ebkmkAuIMic2QGATEOXm5ZpALiDKnNgAgU1AlJuXawK5gChzYgMENgFRbl6uCeQCosyJDRDYBES5ebkmkAuIMic2QGATEOXm5ZpALiDKnNgAgU1AlJuXawK5gChzYgMENgFRbl6uCeQCosyJDRDYBES5ebkmkAuIMic2QGATEOXm5ZpALiDKnNgAgU1AlJuXawK5gChzYgMENgFRbl6uCeQCosyJDRDYBES5ebkmkAuIMic2QGATEOXm5ZpALiDKnNgAgU1AlJuXawK5gChzYgMENgFRbl6uCeQCosyJDRDYBES5ebkmkAuIMic2QGATEOXm5ZpALiDKnNgAgU1AlJuXawK5gChzYgMENgFRbl6uCeQCosyJDRDYBES5ebkmkAuIMic2QGATEOXm5ZpALiDKnNgAgU1AlJuXawK5gChzYgMENgFRbl6uCeQCosyJDRDYBES5ebkmkAuIMic2QGATEOXm5ZpALiDKnNgAgU3gvyh/b593TYDAxQIf55zP28Uv9ToCBB4UEOWDgD5O4GoBUV4t6n0EHhT4Bx4T+oMmQXEtAAAAAElFTkSuQmCC";
          const option = {
            title: {
              text: "",
              x: "center"
            },
            backgroundColor: "#fff",
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
                sizeRange: [11, 50],
                // Text rotation range and step in degree. Text will be rotated randomly in range [-90,                                                                             90] by rotationStep 45
                //用来调整词的旋转方向，，[0,0]--代表着没有角度，也就是词为水平方向，需要设置角度参考注释内容
                // rotationRange: [-45, 0, 45, 90],
                // rotationRange: [ 0,90],
                rotationRange: [0, 0],
                //随机生成字体颜色
                // maskImage: maskImage,
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
                left: "center",
                top: "center",
                right: null,
                bottom: null,
                width: "100%",
                // height: "100%",
                //数据
                data: this.worddata
              }
            ]
          };
          // this.chart.setOption(option);
          chart.setOption(option);
          // maskImage.onload = function () {
          //   chart.setOption(option);
          // };
          window.addEventListener("resize",function(){
            this.chart.resize();
          });
        },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
.el-row{
  float: right;
  display: inline;
  position:absolute;
  top:15px;
  right:40px;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
#appvuedjango {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0;
}
@font-face {
  font-family: 'iconfont';  /* project id 1039987 */
  src: url('//at.alicdn.com/t/font_1039987_gpct6j96g1g.eot');
  src: url('//at.alicdn.com/t/font_1039987_gpct6j96g1g.eot?#iefix') format('embedded-opentype'),
  url('//at.alicdn.com/t/font_1039987_gpct6j96g1g.woff2') format('woff2'),
  url('//at.alicdn.com/t/font_1039987_gpct6j96g1g.woff') format('woff'),
  url('//at.alicdn.com/t/font_1039987_gpct6j96g1g.ttf') format('truetype'),
  url('//at.alicdn.com/t/font_1039987_gpct6j96g1g.svg#iconfont') format('svg');
}
</style>
