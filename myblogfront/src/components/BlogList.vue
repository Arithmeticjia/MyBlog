<template>
  <el-container>
    <title>{{$t('common.search')}} | 请叫我算术嘉の博客</title>
<!--    <Menu></Menu>-->
    <NewMenu></NewMenu>
      <el-main>
        <div v-if="this.$store.state.Canvas">
        <vue-canvas-nest></vue-canvas-nest>
      </div>
        <el-dropdown>
          <span class="el-dropdown-link">
            {{$t('common.lang')}}<i class="el-icon-arrow-down el-icon--right"></i>
          </span>
        <el-dropdown-menu slot="dropdown">
        <el-dropdown-item @click.native = "switchLang('zh')">{{$t('common.lang-zh')}}</el-dropdown-item>
        <el-dropdown-item @click.native = "switchLang('en')">{{$t('common.lang-en')}}</el-dropdown-item>
        </el-dropdown-menu>
        </el-dropdown>
        <div id="appbloglist">
          <div class="input_search">
            <el-input
	            clearable
              @visible-change="resetTable"
              type="text"
              v-model="searchInfo"
              prefix-icon="el-icon-search"
              :placeholder="$t('common.search-placeholder')"
              size="small"
              style="width:180px;float: left">
            </el-input>
            <el-button class="search_btn" type="primary" size="small" icon="el-icon-search" @click="doFilter" style="float:left;margin-left: 10px"></el-button>
          </div>
<!--        <el-popover-->
<!--          placement="top-start"-->
<!--          v-model="visible"-->
<!--          trigger="hover"-->
<!--          style="float: left;margin-left: 5px">-->
<!--          <p>{{$t('common.tip')}}</p>-->
<!--          <div style="text-align: right;">-->
<!--            <el-button type="primary" size="mini" @click="visible = false">{{$t('common.know')}}</el-button>-->
<!--          </div>-->
<!--          <el-button type="text" icon="el-icon-refresh" slot="reference" @click="reFresh" style="margin-right: 10px"></el-button>-->
<!--        </el-popover>-->
      <el-table
        :height="table"
        :style="tableHeight"
        v-loading="loading"
        :element-loading-text="$t('common.load-text')"
        :default-sort = "{prop: 'date', order: 'ascending'}"
        :data="blogList.slice((currentPage-1)*pageSize,currentPage*pageSize)"
      >
        <el-table-column prop="date" :label="$t('common.table.post-id')" width="100">
          <template slot-scope="scope"> {{ scope.row.fields.rand_id }} </template>
        </el-table-column>
        <el-table-column prop="address" :label="$t('common.table.post-time')" sortable width="160">
          <template slot-scope="scope"> {{ scope.row.fields.timestamp | formatDate }} </template>
        </el-table-column>
        <el-table-column prop="name" :label="$t('common.table.post-title')" width="300">
          <template slot-scope="scope"><router-link style="color: #4D4D4D;text-decoration: none" :to="'/post/'+ scope.row.fields.rand_id"> {{ scope.row.fields.title }}</router-link></template>
        </el-table-column>
        <el-table-column prop="address" :label="$t('common.table.post-category')" width="100">
          <template slot-scope="scope"> <router-link style="color: #4D4D4D;text-decoration: none" :to="'/category/' + scope.row.fields.category"> {{ scope.row.fields.category }}</router-link> </template>
        </el-table-column>
        <el-table-column prop="address" :label="$t('common.table.post-tags')" width="150">
          <template slot-scope="scope"> {{ scope.row.fields.tags | tagsFilter }} </template>
        </el-table-column>
        <el-table-column prop="address" :label="$t('common.table.post-views')" width="90">
          <template slot-scope="scope"> {{ scope.row.fields.views }} </template>
        </el-table-column>
        <el-table-column prop="address" :label="$t('common.table.post-author')" width="120">
          <template slot-scope="scope"> {{ scope.row.fields.authorname }} </template>
        </el-table-column>
          <el-table-column prop="address" :label="$t('common.table.post-operation')" width="120" fixed="right">
        <template slot-scope="scope">
          <el-button type="text" @click="open(scope.row.fields.title,scope.row.fields.body)" size="small">{{$t('common.table.operation.overview')}}</el-button>
          <el-button @click="skip('https://www.guanacossj.com/blog/article/'+scope.row.pk+'/'+scope.row.fields.url_slug)" type="text" size="small">{{$t('common.table.operation.detail')}}</el-button>
        </template>
        </el-table-column>
      </el-table>
      <el-footer>
        <br>
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
        </div>
    </el-main>
  </el-container>
</template>

<script>
    import moment from "moment";
    import Menu from "./Menu";
    import NewMenu from "./NewMenu";
    export default {
      name: "BlogList",
      components: {NewMenu, Menu },
      data () {
          return {
            reverse: true,
            isCollapse: true,
            visible: false,
            currentPage: 1,
            totalItems: 0,
            pageSize: 20,
            blogList: [],
            originBlogList: [],
            searchInfo: '',
            filterTableDataEnd: [],
            flag: false,
            loading: true,
            search: "",
            tableHeight: {
              height:'',
            },
            table: window.innerHeight - 132
          }
        },
        created() {
          window.addEventListener('resize', this.getHeight);
          this.getHeight();
        },
        mounted: function () {
          this.showBlogs();
          document.title = this.$t('common.search') + '| 请叫我算术嘉の博客';
        },
        watch: {
          '$i18n.locale'(newVal,oldVal) {
            document.title = this.$t('common.search') + '| 请叫我算术嘉の博客';
          },
          searchInfo: function() {
            if (this.searchInfo.length === 0) {
              this.resetTable();
            }
          },
        },
        filters: {
	        tagsFilter(data) {
	        	return data.toString().replace('[','');
	        },
          formatDate:function(date) {
	        	return moment(date).format("YYYY-MM-DD HH:mm:ss");
	        }
        },
        destroyed(){
          window.removeEventListener('resize', this.getHeight);
        },
        methods: {
          resetTable() {
            this.showBlogs();
          },
          getHeight(){
            this.tableHeight.height = window.innerHeight - 132;
          },
          reFresh: function() {
            window.location.reload();
          },
          switchLang(val){
            this.$i18n.locale=val;//此处val为 zh 或者 en
          },
          doFilter: function() {
            if (this.searchInfo === "") {
              this.$message.warning({
                center: true,
                message: this.$t('common.warning.queryEmpty')});
              return;
            }
            this.filterTableDataEnd = [];
            this.originBlogList.forEach((value, index) => {
              if(value.fields.title){
                if(value.fields.title.indexOf(this.searchInfo)>=0){
                  this.filterTableDataEnd.push(value);
                }
              }
            });
            //页面数据改变重新统计数据数量和当前页
             this.currentPage = 1;
             this.totalItems = this.filterTableDataEnd.length;
             //渲染表格,根据值
             this.currentChangePage(this.filterTableDataEnd);
             //页面初始化数据需要判断是否检索过
             this.flag = true
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
             this.$confirm(body.substr(1,100)+'...', title, {
               center: true,
               type: 'info',
               iconClass: 'el-icon-document',
               cancelButtonText: this.$t('common.table.operation.cancel'),
               confirmButtonText: this.$t('common.table.operation.confirm'),
               // callback: action => {
               //   this.$message({
               //     type: 'info',
               //     message: `action: ${ action }`
               //   });
               // }
             });
          },
          skip(url){
            window.open(url, '_blank')
          },
          showBlogs () {
            this.$http.get('https://www.guanacossj.com/blog/getallarticle/',{
                _timeout:5000,
                onTimeout :(request) => {
                    this.$message.error({
                      message: this.$t('common.timeout'),
                      center: true
                    });
                    this.loading = false
                  }
                }).then((response) => {
                var res = JSON.parse(response.bodyText);
                if (res.error_num === 0) {
                  this.loading = false;
                  this.blogList = res['list'];
                  this.totalItems = this.blogList.length;
                  this.originBlogList = this.blogList;
                } else {
                  this.$message.error('查询博客列表失败');
                }
              })
          }
        },
    }
</script>

<style scoped>
  .el-footer {
    color: #333;
    text-align: center;
    line-height: 20px;
  }
  #appbloglist {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #4d4d4d;
    /*margin-top: 30px;*/
  }
  .el-main {
    color: #333;
    text-align: center;
    /*margin-right: 150px;*/
    /*margin-right: 12%;*/
  }
  .el-menu-item.is-active {
    background: rgb(67, 74, 80) !important;
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
</style>
