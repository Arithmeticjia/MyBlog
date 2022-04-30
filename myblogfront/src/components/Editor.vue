<template>
  <div id="appeditor" class="backtop" style="margin-top: 30px">
   <el-backtop target=".backtop"></el-backtop>
   <el-form label-width="80px" :model="formLabelAlign" ref="formLabelAlign" :rules="rules">
    <el-form-item label="文章标题">
      <el-col :span="8">
        <el-input
          placeholder="请输入文章标题"
          v-model="formLabelAlign.title"
          clearable
          ></el-input>
      </el-col>
    </el-form-item>
    <el-form-item label="文章内容">
      <mavon-editor v-model="formLabelAlign.content"/>
    </el-form-item>
    <el-form-item label="文章分类">
      <el-select v-model="formLabelAlign.category" clearable placeholder="请选择文章分类">
        <el-option
          v-for="item in categoryList"
          :key="item.name"
          :value="item.name">
        </el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="文章标签">
      <el-select
        v-model="formLabelAlign.tags"
        multiple
        filterable
        allow-create
        default-first-option
        placeholder="请选择文章标签">
        <el-option
          v-for="item in tagsList"
          :key="item.value"
          :label="item.label"
          :value="item.fields.name">
        </el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="文章状态">
      <el-radio-group v-model="formLabelAlign.status">
        <el-radio label="有效">公开</el-radio>
        <el-radio label="DEL">删除</el-radio>
      </el-radio-group>
    </el-form-item>
    <el-form-item label="是否原创">
      <el-radio-group v-model="formLabelAlign.isOrigin">
        <el-radio label="1">原创</el-radio>
        <el-radio label="2">转载</el-radio>
      </el-radio-group>
    </el-form-item>
    <el-form-item label="封面图" style="width: 500px">
      <el-upload
        class="upload-demo"
        drag
        :file-list="fileList"
        list-type="picture"
        action="https://jsonplaceholder.typicode.com/posts/"
        multiple>
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
        <div class="el-upload__tip" slot="tip">只能上传jpg/png文件，且不超过500kb</div>
      </el-upload>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitForm('formLabelAlign')">保存</el-button>
      <el-button>取消</el-button>
    </el-form-item>
  </el-form>
  </div>
</template>

<script>
import axios from "_axios@0.21.4@axios";

export default {
  name: "Editor",
  data() {
      return {
        fileList: [
          {
            name: 'cover image.jpg',
            url: '',
          },
        ],
        singleBlog: [],
        formLabelAlign: {
          title: '',
          content: '',
          category: '',
          tags: [],
          isOrigin: '1',
          pic: null,
          status: ''
        },
        rules: {
          title: [
            { required: true, message: '请输入文章标题', trigger: 'blur' },
            { min: 3, max: 5, message: '长度在 1 到 50 个字符', trigger: 'blur' }
          ],
          category: [
            { type: 'array', required: true, message: '请至少选择一个文章分类', trigger: 'change' }
          ],
          tags: [
            { type: 'array', required: true, message: '请至少选择一个文章标签', trigger: 'change' }
          ],
        },
        categoryList: [],
        tagsList: [],
        value: ''
      }
    },
    mounted() {
      this.showCategories();
      this.showTags();
      this.getSingleBlog();
    },
    beforeCreate() {
      document.querySelector('body').setAttribute('style', 'overflow-y:scroll;')
      document.getElementById('app').setAttribute('style', 'overflow-y:scroll;')
    },
    beforeDestroy() {
        document.body.removeAttribute('style')
    },
    methods: {
      handlePreview(file) {
        this.formLabelAlign.pic = file
      },
      resetForm(formName) {
        this.$refs[formName].resetFields();
      },
      getSingleBlog () {
        sessionStorage.setItem("detail", true);
        this.$http.get('https://www.guanacossj.com/blog/single-article/' + this.$route.params.id,{
          _timeout:5000,
          onTimeout :(request) => {
              this.$message.error({
                message: this.$t('common.timeout'),
                center: true
              });
              this.loading = false
            }
          }).then((response) => {
          const res = JSON.parse(response.bodyText);
          if (res.error_num === 0) {
            this.tags = res['list'][0]['fields']['tags'];
            this.loading = false;
            this.markdownhtml = res.markdown;
            this.html = res['list'][0].fields.body;
            if (res.prev_article_title !== ""){
              this.prev_article_rand_id = res.prev_article_rand_id;
              this.prev_article_title = res.prev_article_title;
            } else {
              this.prev_article_title = "已经是第一篇了"
            }
            if (res.next_article_title !== ""){
              this.next_article_rand_id = res.next_article_rand_id;
              this.next_article_title = res.next_article_title;
            } else {
              this.next_article_title = "已经是最后一篇了"
            }
            this.singleBlog = res['list'][0];
            this.formLabelAlign.title = this.singleBlog.fields.title;
            this.formLabelAlign.content = this.singleBlog.fields.body;
            this.formLabelAlign.category = this.singleBlog.fields.category;
            this.formLabelAlign.tags = this.singleBlog.fields.tags;
            this.formLabelAlign.status = this.singleBlog.fields.status;
            this.fileList[0].url = 'https://www.guanacossj.com/media/' + this.singleBlog.fields.pic;
            document.title = res['list'][0].fields.title;
            this.navList = this.handleNavTree();
            if(this.navList.length === 0) {
              this.navList[0] = {
                title: "此页目录为空",
                children: new Array(1)['length'] = 0
              };
            }
            this.getDocsFirstLevels(0);
          } else {
            this.$message.error('查询博客详情失败');
          }
        })
      },
      submitForm(formName) {
        this.$refs[formName].validate(valid => {
          if (valid) {
            this.loading = true;
            axios({
              method: "post",
              url: "https://www.guanacossj.com/blog/api/edit/article/" + this.$route.params.id + "/",
              headers: {
                'Content-Type': 'application/json'
              },
              withCredentials: false,
              data: this.formLabelAlign
            }).then((res)=>{
              if(res.status === 200){
                this.loading = false;
                this.dialogFormVisible = false;
                this.$message({
                  type: 'success',
                  message: `编辑成功!`,
                  center: true
                });
                this.$router.push("/post/" + this.$route.params.id + "/");
              } else {
                this.$message({
                  type: 'error',
                  message: `服务器出了点问题，请稍后重试!`,
                  center: true
                });
              }
            });
          } else {
            this.$message({
              type: 'error',
              message: `提交表单异常`,
              center: true
            });
            return false
          }
        })
      },
      showTags () {
        this.$http.get('https://www.guanacossj.com/blog/tags/',{
          _timeout:5000,
          onTimeout :(request) => {
              this.$message.error({
                message: this.$t('common.timeout'),
                center: true
              });
              this.loading = false
            }
          }).then((response) => {
          const res = JSON.parse(response.bodyText);
          this.tagsList = res['data'];
        })
      },
      showCategories () {
        this.$http.get('https://www.guanacossj.com/blog/getallcategory/',{
          _timeout:5000,
          onTimeout :(request) => {
              this.$message.error({
                message: this.$t('common.timeout'),
                center: true
              });
              this.loading = false
            }
          }).then((response) => {
          const res = JSON.parse(response.bodyText);
          if (res.error_num === 0) {
            this.categoryList = res['list'];
          } else {
            this.$message.error('查询分类列表失败');
          }
        })
      },
      remoteMethod(query) {
        if (query !== '') {
          this.loading = true;
          setTimeout(() => {
            this.loading = false;
            this.options = this.list.filter(item => {
              return item.label.toLowerCase()
                .indexOf(query.toLowerCase()) > -1;
            });
          }, 200);
        } else {
          this.options = [];
        }
      }
    }
}
</script>

<style scoped>
  #appeditor {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    color: #4d4d4d;
    margin-top: 30px;
  }
</style>
