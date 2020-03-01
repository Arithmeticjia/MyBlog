<template>
<el-container style="height: 600px; border: 1px solid #eee">
  <el-backtop target="#app" :visibility-height="100"></el-backtop>
  <el-header>
    <el-input
	    clearable
      type="text"
      v-model="searchinfo"
      placeholder="搜索"
      size="medium"
      style="width:160px;">
    </el-input>
    <el-button type="primary" size="medium" icon="el-icon-search" @click="doFilter" style="margin-right: 10px"></el-button>
    <el-popover
      placement="top-start"
      v-model="visible"
      trigger="hover">
      <p>点击刷新页面</p>
      <div style="text-align: right; margin: 0">
    <el-button type="primary" size="mini" @click="visible = false">我知道了</el-button>
  </div>
    <el-button type="text" icon="el-icon-refresh" slot="reference" @click="reFresh" style="margin-right: 10px"></el-button>
    </el-popover>
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
    <el-menu :default-openeds="['1', '2']">
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
      <el-table height="100%" v-loading="loading" :data="blogList.slice((currentPage-1)*pageSize,currentPage*pageSize)">
        <el-table-column prop="date" label="序号" width="50">
          <template scope="scope"> {{ scope.row.pk }} </template>
        </el-table-column>
        <el-table-column prop="name" label="标题" width="width: 100%">
          <template scope="scope"> {{ scope.row.fields.title }}</template>
        </el-table-column>
        <el-table-column prop="address" label="分类" width="width: 100%">
          <template scope="scope"> {{ scope.row.fields.category }} </template>
        </el-table-column>
        <el-table-column prop="address" label="标签" width="width: 100%">
          <template scope="scope"> {{ scope.row.fields.tags }} </template>
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
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-sizes="[1, 2, 3, 4]"
        :page-size="pageSize"
        :total="totalItems"
        layout="prev, pager, next, total">
      </el-pagination>
    </el-footer>
    </el-container>
  </el-container>
</el-container>
</template>

<style>
  .el-header, .el-footer {
    color: #333;
    text-align: center;
    line-height: 60px;
  }
  .el-main {
    color: #333;
    text-align: center;
  }
  .el-header {
    background-color: #B3C0D1;
    /*background: #4FC08D;*/
    color: #333;
    line-height: 60px;
    text-align: right;
    font-size: 12px
  }
  body > .el-container {
    margin-bottom: 40px;
  }
  .el-container:nth-child(5) .el-aside,
  .el-container:nth-child(6) .el-aside {
    line-height: 260px;
  }
  .el-container:nth-child(7) .el-aside {
    line-height: 320px;
  }
  .el-aside {
    color: #333;
    background-color: #D3DCE6;
  }
</style>

<script>
export default {
  name: 'home',
  data () {
    return {
      isCollapse: true,
      visible: false,
      currentPage:1,
      totalItems:0,
      pageSize:10,
      searchInfo: '',
      blogList: [],
      originblogList: [],
      searchinfo: '',
      filterTableDataEnd: [],
      flag:false,
      loading: true,
    }
  },
  mounted: function () {
    this.showBlogs();
  },
  methods: {
     reFresh: function() {
       window.location.reload();
     },
     doFilter: function() {
       if (this.searchinfo === "") {
         this.$message.warning("查询条件不能为空！");
         return;
       }
       this.filterTableDataEnd=[];
       this.originblogList.forEach((value, index) => {
         if(value.fields.title){
           if(value.fields.title.indexOf(this.searchinfo)>=0){
             this.filterTableDataEnd.push(value);
           }
         }
       });
       //页面数据改变重新统计数据数量和当前页
        this.currentPage=1;
        this.totalItems=this.filterTableDataEnd.length;
        //渲染表格,根据值
        this.currentChangePage(this.filterTableDataEnd);
        //页面初始化数据需要判断是否检索过
        this.flag=true
     },
     handleSizeChange(val) {
        this.pageSize = val;
        this.handleCurrentChange(this.currentPage);
      },
     handleCurrentChange: function(currentPage){
        this.currentPage = currentPage;
        if(this.flag) {
          this.blogList = this.filterTableDataEnd
        }
     },
     currentChangePage(list) {
        let from = (this.currentPage - 1) * this.pageSize;
        let to = this.currentPage * this.pageSize;
        this.blogList = [];
        if (to > list.length){
          for (; from < list.length; from++) {
            if (list[from]) {
              this.blogList.push(list[from]);
            }
          }
        }else {
          for (; from < to; from++) {
            if (list[from]) {
              this.blogList.push(list[from]);
            }
          }
        }
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
      this.$http.get('https://www.guanacossj.com/blog/showarticles/',{
          _timeout:5000,
          onTimeout :(request) => {
              this.$message.error('请求超时');
              this.loading = false
            }
          }).then((response) => {
          var res = JSON.parse(response.bodyText);
          if (res.error_num === 0) {
            this.loading = false;
            this.blogList = res['list'];
            this.totalItems = this.blogList.length;
            this.originblogList = this.blogList;
          } else {
            this.$message.error('查询博客列表失败');
          }
        })
    }
  }
}
</script>
