<template>
  <el-container>
    <title>{{$t('common.category')}}</title>
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
      <div id="appcategory" v-loading="loading" :element-loading-text="$t('common.load-text')">
        <div class="category-box">
          <div class="grid-content bg-puprple-light">
            <el-row type="flex" class="row-bg" justify="space-around">
              <el-col :span="20">
                <div class="grid-content bg-puprple-light">
<!--                  <h1 style="text-align: center">分类</h1>-->
                  <p style="text-align: center">{{$t('common.cat-before')}}<span style="font-size: xxx-large;">{{ totalItems }}</span>{{$t('common.cat-after')}}</p>
                  <div class="category" v-for="(value, key, index) in categoryList.slice((currentPage-1)*pageSize,currentPage*pageSize)">
                    <p style="color: #4D4D4D; font-size: 20px"><router-link style="color: #4D4D4D" :to="'/category/'+value.fields.name"><span class="xi">{{ value.fields.name }}</span></router-link></p>
                  </div>
                  <br>
                </div>
              </el-col>
            </el-row>
          </div>
        </div>
        <br>
        <div class="hide-pagination">
          <el-switch v-model="value">
          </el-switch>
        </div>
      <el-footer>
          <el-pagination
            v-show="showpagination"
            :hide-on-single-page="value"
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
import Menu from "./Menu";
    export default {
        name: "Category",
        components: { Menu },
        data () {
          return {
            reverse: true,
            value: false,
            categoryList: [],
            currentPage: 1,
            totalItems: 0,
            loading: true,
            pageSize: 15,
          }
        },
        mounted() {
          this.showCategorys();
        },
        watch: {
          '$i18n.locale'(newVal,oldVal) {
            document.title = this.$t('common.category')
          }
        },
        methods: {
          skip(url){
           window.open(url, target='_blank')
          },
          handleOpen(key, keyPath) {
            console.log(key, keyPath);
          },
          skiplocal(url){
            location.href = url
          },
          switchLang(val){
            this.$i18n.locale=val;//此处val为 zh 或者 en
            sessionStorage.setItem('lang', val);
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
          showCategorys () {
            this.$http.get('https://www.guanacossj.com/blog/getallcategory/',{
                _timeout:5000,
                onTimeout :(request) => {
                    this.$message.error(this.$t('common.timeout'));
                    this.loading = false
                  }
                }).then((response) => {
                var res = JSON.parse(response.bodyText);
                if (res.error_num === 0) {
                  this.loading = false;
                  this.showpagination = true;
                  this.categoryList = res['list'];
                  this.totalItems = this.categoryList.length;
                } else {
                  this.$message.error('查询分类列表失败');
                }
              })
          },
        }
    }
</script>

<style scoped>
  .el-menu{
    box-shadow: 0 4px 4px rgba(0, 0, 0, .30), 0 0 6px rgba(0, 0, 0, .04)
  }
  #appcategory {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    /*color: #2c3e50;*/
    color: #4d4d4d;
    margin-top: 30px;
  }
  .el-col {
    border-radius: 4px;
  }
  .bg-purple-dark {
    background: #99a9bf;
  }
  .bg-purple {
    background: #d3dce6;
  }
  .bg-purple-light {
    background: #e5e9f2;
  }
  .grid-content {
    border-radius: 4px;
    min-height: 36px;
  }
  .row-bg {
    padding: 10px 0;
    /*background-color: #f9fafc;*/
    background-color: rgba(255, 255, 255, 0);
    /*box-shadow: 0 2px 4px rgba(0, 0, 0, .20), 0 0 6px rgba(0, 0, 0, .04)*/
    box-shadow: 0 4px 4px rgba(0, 0, 0, .30), 0 0 6px rgba(0, 0, 0, .04)
  }
  .category-box {
    text-align: left;
  }
  .hide-pagination {
    float: right;
    /*padding-right: 0 !important;*/
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
  .category {
    background: #fff;
    width: 100%;
    height: 100%;
    text-align: left;
  }
  .xi {
    text-decoration:none;
    border-bottom:1px solid #ccc; /* #ccc换成链接的颜色 */
    display: inline-block;
    padding-bottom:1px;  /*这里设置你要空的距离*/
  }
</style>
