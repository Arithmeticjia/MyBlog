let baseUrl = "";
switch (process.env.NODE_ENV) { //注意变量名是自定义的
  case 'development':
    baseUrl = "http://localhost:8085/"  //开发环境url
    break
  case 'production':
    baseUrl = "https://localhost:8085/"   //生产环境url
    break
}

export default baseUrl;
