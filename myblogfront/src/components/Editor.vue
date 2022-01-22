<template>
  <div id="main" style="margin-top: 30px">
   <el-form :label-position="labelPosition" label-width="80px" :model="formLabelAlign">
    <el-form-item label="文章标题">
      <el-col :span="8">
        <el-input
          placeholder="请输入内容"
          v-model="formLabelAlign.name"
          clearable
          ></el-input>
      </el-col>
    </el-form-item>
    <el-form-item label="文章内容">
      <mavon-editor v-model="value"/>
    </el-form-item>
    <el-form-item label="文章分类">
      <el-select v-model="value" clearable placeholder="请选择">
    <el-option
      v-for="item in options"
      :key="item.value"
      :label="item.label"
      :value="item.value">
    </el-option>
  </el-select>
    </el-form-item>
  </el-form>

  </div>
</template>

<script>
export default {
  name: "Editor",
  data() {
      return {
        input: '',
        formLabelAlign: {
          name: '',
          region: '',
          type: ''
        },
        options: [{
          value: '选项1',
          label: '黄金糕'
        }, {
          value: '选项2',
          label: '双皮奶'
        }, {
          value: '选项3',
          label: '蚵仔煎'
        }, {
          value: '选项4',
          label: '龙须面'
        }, {
          value: '选项5',
          label: '北京烤鸭'
        }],
        value: ''
      }
    },
    mounted() {
      this.list = this.states.map(item => {
        return { value: `value:${item}`, label: `label:${item}` };
      });
    },
    methods: {
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

</style>
