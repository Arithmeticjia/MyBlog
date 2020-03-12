<template>
    <div class="notfound">
      404
      <div class="notfound-text">
        <router-link to="/home" style="color: #4D4D4D;text-decoration: none">
          返回首页
        </router-link>
      </div>
    </div>
</template>

<script>
    export default {
        name: "notfound"
    }
</script>

<style scoped>
  html,body {
    width: 100%;
    height: 100%;
    margin: 0;
    padding: 0;
  }
  .notfound {
    text-align: center;
    font-size: 150px;
    width: 300px;
    height: 300px;
    position: relative;
    margin: 0 auto;
    top: 50%;
    color: #4D4D4D;
    /*transform: translateY(-50%);*/
    margin-top: 150px;
  }
  .notfound-text {
    /*background-color: #0d8464;*/
    font-size: 20px;
    color: #4D4D4D;
  }

</style>
