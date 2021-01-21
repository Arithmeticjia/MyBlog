<template>
  <el-container>
    <Menu></Menu>
      <el-main>
        <vue-canvas-nest></vue-canvas-nest>
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
              type="text"
              v-model="searchinfo"
              :placeholder="$t('common.search-placeholder')"
              size="medium"
              style="width:180px;float: left">
            </el-input>
            <el-button class="search_btn" type="primary" size="medium" icon="el-icon-search" @click="doFilter" style="float:left;margin-left: 10px"></el-button>
          </div>
        <el-popover
          placement="top-start"
          v-model="visible"

          trigger="hover"
          style="float: left;margin-left: 5px">
          <p>{{$t('common.tip')}}</p>
          <div style="text-align: right;">
            <el-button type="primary" size="mini" @click="visible = false">{{$t('common.know')}}</el-button>
          </div>
          <el-button type="text" icon="el-icon-refresh" slot="reference" @click="reFresh" style="margin-right: 10px"></el-button>
        </el-popover>
      <el-table :height="table" :style="tableHeight" v-loading="loading" :element-loading-text="$t('common.load-text')" :data="blogList.slice((currentPage-1)*pageSize,currentPage*pageSize)">
        <el-table-column prop="date" :label="$t('common.table.post-id')" width="50">
          <template slot-scope="scope"> {{ scope.row.pk }} </template>
        </el-table-column>
        <el-table-column prop="name" :label="$t('common.table.post-title')" width="300">
          <template slot-scope="scope"><router-link style="color: #4D4D4D;text-decoration: none" :to="'/post/'+ scope.row.pk"> {{ scope.row.fields.title }}</router-link></template>
        </el-table-column>
        <el-table-column prop="address" :label="$t('common.table.post-category')" width="100">
          <template slot-scope="scope"> {{ scope.row.fields.category }} </template>
        </el-table-column>
        <el-table-column prop="address" :label="$t('common.table.post-tags')" width="130">
          <template slot-scope="scope"> {{ scope.row.fields.tags | tagsFilter }} </template>
        </el-table-column>
        <el-table-column prop="address" :label="$t('common.table.post-visit')" width="90">
          <template slot-scope="scope"> {{ scope.row.fields.views }} </template>
        </el-table-column>
        <el-table-column prop="address" :label="$t('common.table.post-author')" width="120">
          <template slot-scope="scope"> {{ scope.row.fields.authorname }} </template>
        </el-table-column>
        <el-table-column prop="address" :label="$t('common.table.post-time')" width="200">
          <template slot-scope="scope"> {{ scope.row.fields.timestamp | formatDate }} </template>
        </el-table-column>
          <el-table-column prop="address" :label="$t('common.table.post-operation')" width="150" fixed="right">
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
    export default {
      name: "BlogList",
      components: { Menu },
      data () {
          return {
            reverse: true,
            isCollapse: true,
            visible: false,
            currentPage:1,
            totalItems:0,
            pageSize:15,
            searchInfo: '',
            blogList: [],
            originblogList: [],
            searchinfo: '',
            filterTableDataEnd: [],
            flag: false,
            loading: true,
            tableHeight:{
              height:'',
            },
            table:window.innerHeight - 159
          }
        },
        created() {
          window.addEventListener('resize', this.getHeight);
          this.getHeight;
        },
        mounted: function () {
          this.showBlogs();
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
          getHeight(){
            this.tableHeight.height = window.innerHeight - 159;
          },
          reFresh: function() {
            window.location.reload();
          },
          switchLang(val){
            this.$i18n.locale=val;//此处val为 zh 或者 en
          },
          doFilter: function() {
            if (this.searchinfo === "") {
              this.$message.warning(this.$t('common.warning.queryEmpty'));
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
          skiplocal(url){
            location.href = url
          },
          showBlogs () {
            this.$http.get('https://www.guanacossj.com/blog/getallarticle/',{
                _timeout:5000,
                onTimeout :(request) => {
                    this.$message.error(this.$t('common.timeout'));
                    this.loading = false
                  }
                }).then((response) => {
                var res = JSON.parse(response.bodyText);
                if (res.error_num === 0) {
                  this.loading = false;
                  this.blogList = res['list'];
                  // this.blogList.push(res['list']) ;
                  this.totalItems = this.blogList.length;
                  this.originblogList = this.blogList;
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
  .el-main {
    color: #333;
    text-align: center;
    /*margin-right: 150px;*/
    /*margin-right: 12%;*/
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
</style>
