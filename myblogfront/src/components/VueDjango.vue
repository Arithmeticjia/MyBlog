<template>
  <div class="hello">
    <div id="app">
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
    </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  data () {
    return {
      msg: 'Welcome to My Vue.js & Django App',
      dialogVisible: false
    };
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
      }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
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
#app {
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
