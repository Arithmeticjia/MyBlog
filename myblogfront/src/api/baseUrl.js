let baseUrl = "";
switch (process.env.NODE_ENV) { //注意变量名是自定义的
  case 'development':
    // baseUrl = "http://127.0.0.1:8000"  //开发环境url
    baseUrl = "https://yun.guanacossj.com"   //生产环境url
    break
  case 'production':
    baseUrl = "https://yun.guanacossj.com"   //生产环境url
    break
}

export default baseUrl;
