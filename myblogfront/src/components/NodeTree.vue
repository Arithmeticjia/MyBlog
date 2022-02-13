<template>
  <div class="comment-item" >
        <div class="comments-content">
            <div class="post__author author vcard">
                <div class="author-date">
                  <div class="author">{{ node.user[0] }} :</div>
                    <div class="post__date" style="display: inline;font-weight: normal">
                        <time class="published" datetime="node.created_at">
                          {{ node.created_time | formatDate }}
                        </time>
                    </div>
                </div>
            </div>
            <p style="margin-left: 20px" v-html="node.body"></p>
            <span style="font-size: 14px;margin-left: 20px"><i class="el-icon-thumb"></i>赞</span>
          <el-button type="text" style="font-size: 14px;margin-left: 20px" @click="dialogVisible = true"><i class="el-icon-chat-dot-square"></i>回复</el-button>
            <el-dialog
              title="评论"
              :visible.sync="dialogVisible"
              width="30%"
              :before-close="handleClose">
              <span slot="footer" class="dialog-footer">
                <el-button @click="dialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="dialogVisible = false">确 定</el-button>
              </span>
              <el-form :model="form" :rules="rules" ref="form">
                <el-form-item>
                  <el-input placeholder="说点好听的" type="textarea" v-model="form.content" autocomplete="off"></el-input>
                </el-form-item>
              </el-form>
            </el-dialog>
        </div>
  </div>
</template>

<script>
import moment from "moment";

export default {
  name: "node",
  props: {
    node: Object
  },
  data() {
      return {
        dialogVisible: false,
        form: {
          content: ""
        },
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
    submitForm(formname) {
      this.$refs[formname].validate(valid => {
        if (valid) {
          this.loading = true;
          axios({
            method:"post",
            url:"http://localhost:8085/yunprophet/serverapi/addServer",
            headers: {
              'Content-Type': 'application/json'
            },
            withCredentials:false,
            data:this.form
          }).then((res)=>{
            if(res.data.code === 200){
              this.loading = false;
              this.dialogFormVisible = false;
              this.$message({
                type: 'success',
                message: `添加成功!`
              });
              this.showVmServer();
            }else {
              this.$message({
                type: 'error',
                message: `服务器出了点问题，请稍后重试!`
              });
            }
          });
        } else {
          console.log('error submit!!');
          return false
        }
      })
    },
  },
  filters: {
	        /*
	         时间格式自定义 只需把字符串里面的改成自己所需的格式
	        */
	        formatDate: function(date) {
	        	return moment(date).format("YYYY-MM-DD HH:mm:ss");
	        },
          numberFormat: function (value) {
            return value.toString().replace(/(\d)(?=(?:\d{3})+$)/g, '$1,')
          }
        },
};
</script>

<style scoped>
.comment-item {
  text-align: left;
  font-size: 15px;
}
.author {
  display: inline;
  font-weight: bolder;
  font-size: 15px;
}
.published {
  font-size: 14px;
  color: #7D7D7D;
}
</style>
