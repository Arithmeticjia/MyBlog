<template>
  <div class="hello">
    <div id="app">
      <img src="../assets/logo.png">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
      <img src="../assets/django_logo.png">
    <h1>{{ msg }}</h1>
    <h2>Home Page</h2>
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
    <h2>Show</h2>
    <ul>
      <li>
        <a
          href="http://101.132.70.184:8090/#/bloglist"
          target="_blank"
        >
          bloglist
        </a>
      </li>
    </ul>
  </div>
    </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  data () {
    return {
      msg: 'Welcome to My Vue.js & Django App'
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
