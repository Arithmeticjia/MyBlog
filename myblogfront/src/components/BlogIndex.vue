<template>
<el-container style="height: 600px; border: 1px solid #eee">
  <el-header style="text-align: right; font-size: 12px">
    <el-input
	    suffix-icon="el-icon-search" clearable v-model="searchInfo" placeholder="搜索" size="medium" style="width:180px;margin-right: 20px;">
    </el-input>
    <el-dropdown>
        <i class="el-icon-caret-bottom" style="margin-right: 5px"></i>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item>登录</el-dropdown-item>
          <el-dropdown-item>退出</el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
      <span style="font-size: larger;font-family: 'Helvetica Neue',Helvetica,'PingFang SC','Hiragino Sans GB','Microsoft YaHei','微软雅黑',Arial,sans-serif;">请叫我算术嘉</span>
  </el-header>
  <el-container>
  <el-aside width="200px" style="background-color: rgb(238, 241, 246)">
    <el-menu :default-openeds="['1', '3']">
      <el-submenu index="1">
        <template slot="title"><i class="el-icon-message"></i>文章</template>
        <el-menu-item-group>
          <template slot="title">分组一</template>
          <el-menu-item index="1-1">选项1</el-menu-item>
          <el-menu-item index="1-2">选项2</el-menu-item>
        </el-menu-item-group>
        <el-menu-item-group title="分组2">
          <el-menu-item index="1-3">选项3</el-menu-item>
        </el-menu-item-group>
        <el-submenu index="1-4">
          <template slot="title">选项4</template>
          <el-menu-item index="1-4-1">选项4-1</el-menu-item>
        </el-submenu>
      </el-submenu>
      <el-submenu index="2">
        <template slot="title"><i class="el-icon-menu"></i>用户</template>
        <el-menu-item-group>
          <template slot="title">分组一</template>
          <el-menu-item index="2-1">选项1</el-menu-item>
          <el-menu-item index="2-2">选项2</el-menu-item>
        </el-menu-item-group>
        <el-menu-item-group title="分组2">
          <el-menu-item index="2-3">选项3</el-menu-item>
        </el-menu-item-group>
        <el-submenu index="2-4">
          <template slot="title">选项4</template>
          <el-menu-item index="2-4-1">选项4-1</el-menu-item>
        </el-submenu>
      </el-submenu>
      <el-submenu index="3">
        <template slot="title"><i class="el-icon-setting"></i>留言</template>
        <el-menu-item-group>
          <template slot="title">分组一</template>
          <el-menu-item index="3-1">选项1</el-menu-item>
          <el-menu-item index="3-2">选项2</el-menu-item>
        </el-menu-item-group>
        <el-menu-item-group title="分组2">
          <el-menu-item index="3-3">选项3</el-menu-item>
        </el-menu-item-group>
        <el-submenu index="3-4">
          <template slot="title">选项4</template>
          <el-menu-item index="3-4-1">选项4-1</el-menu-item>
        </el-submenu>
      </el-submenu>
    </el-menu>
  </el-aside>


  <el-container>
    <el-main>
      <el-table height="100%" :data="blogList.slice((currentPage-1)*pagesize,currentPage*pagesize)">
        <el-table-column prop="date" label="序号" width="50">
          <template scope="scope"> {{ scope.row.pk }} </template>
        </el-table-column>
        <el-table-column prop="name" label="标题" width="width: 100%">
          <template scope="scope"> {{ scope.row.fields.title }}</template>
        </el-table-column>
        <el-table-column prop="address" label="分类" width="width: 100%">
          <template scope="scope"> {{ scope.row.fields.category }} </template>
        </el-table-column>
        <el-table-column prop="address" label="作者" width="width: 100%">
          <template scope="scope"> {{ scope.row.fields.authorname }} </template>
        </el-table-column>
        <el-table-column prop="address" label="操作" width="width: 100%">
        <template slot-scope="scope">
          <el-button type="text" @click="open(scope.row.fields.title,scope.row.fields.body)" size="small">查看</el-button>
          <el-button @click="skip('https://www.guanacossj.com/blog/article/'+scope.row.pk+'/'+scope.row.fields.url_slug)" type="text" size="small">查看详情</el-button>
        </template>
        </el-table-column>
      </el-table>
    </el-main>
    <el-footer style="text-align: center">
      <el-pagination
        background
        :page-sizes="[5, 10, 20, 40]"
        :page-size="pagesize"
        @size-change="handleSizeChange"
        :total="blogList.length"
        @current-change="handleCurrentChange"
        layout="prev, pager, next">
      </el-pagination>
    </el-footer>
    </el-container>
  </el-container>
</el-container>
</template>

<style>
  .el-header {
    background-color: #B3C0D1;
    color: #333;
    line-height: 60px;
  }

  .el-aside {
    color: #333;
  }
</style>

<script>
export default {
  name: 'home',
  data () {
    return {
      input: '',
      currentPage:1,
      pagesize:10,
      searchInfo: '',
      blogList: []
    }
  },
  mounted: function () {
    this.showBlogs()
  },
  methods: {
     handleCurrentChange: function(currentPage){
       this.currentPage = currentPage;
       console.log(this.currentPage)  //点击第几页
     },
     handleSizeChange: function (size) {
       this.pagesize = size;
       console.log(this.pagesize)  //每页下拉显示数据
     },
     open(title,body) {
        this.$alert(body.substr(1,100)+'...', title, {
          confirmButtonText: '确定',
          // callback: action => {
          //   this.$message({
          //     type: 'info',
          //     message: `action: ${ action }`
          //   });
          // }
        });
    },
    skip(url){
      location.href = url
    },
    showBlogs () {
      this.$http.get('https://www.guanacossj.com/blog/showarticles/')
        .then((response) => {
          var res = JSON.parse(response.bodyText);
          console.log(res.list.length);
          if (res.error_num === 0) {
            this.blogList = res['list']
          } else {
            this.$message.error('查询书籍失败');
            // console.logs(res['msg'])
          }
        })
    }
  }
}
</script>
