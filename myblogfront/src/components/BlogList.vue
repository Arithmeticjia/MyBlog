<template>
  <div class="home">
    <el-row display="margin-top:10px">
        <el-input v-model="input" placeholder="请输入文章名" style="display:inline-table; width: 30%; float:left"></el-input>
        <el-button type="primary" @click="showBooks()" style="float:left; margin: 2px;">搜索</el-button>
    </el-row>
    <el-row>
        <el-table :data="bookList" style="width: 100%" border>
          <el-table-column prop="id" label="编号" min-width="100">
            <template scope="scope"> {{ scope.row.pk }} </template>
          </el-table-column>
          <el-table-column prop="book_name" label="文章名" min-width="100">
            <template scope="scope"> {{ scope.row.fields.title }} </template>
          </el-table-column>
          <el-table-column prop="add_time" label="分类" min-width="100">
            <template scope="scope"> {{ scope.row.fields.category }} </template>
          </el-table-column>
          <el-table-column prop="add_time" label="作者" min-width="100">
            <template scope="scope"> {{ scope.row.fields.authorname }} </template>
          </el-table-column>
        </el-table>
    </el-row>
  </div>

</template>

<script>
export default {
  name: 'home',
  data () {
    return {
      input: '',
      bookList: []
    }
  },
  mounted: function () {
    this.showBooks()
  },
  methods: {
    showBooks () {
      this.$http.get('https://www.guanacossj.com/blog/showarticles/')
        .then((response) => {
          var res = JSON.parse(response.bodyText);
          console.log(res);
          if (res.error_num === 0) {
            this.bookList = res['list']
          } else {
            this.$message.error('查询书籍失败');
            // console.log(res['msg'])
          }
        })
    }
  }
}
</script>

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
</style>
