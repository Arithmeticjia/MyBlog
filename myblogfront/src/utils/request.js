import axios from 'axios'             //引入 axios
import baseUrl from '../api/baseUrl'

// 创建 axios 实例
const service = axios.create({
  baseURL: baseUrl, // api 的 base_url
  timeout: 15000, // 请求超时时间
});

// 添加请求拦截器
service.interceptors.request.use(function (config) {
    return config;
  }, function (error) {
    return Promise.reject(error);
  });

// 添加响应拦截器
service.interceptors.response.use(function (response) {
    // 对响应数据做点什么
    return response;
  }, function (error) {
    // 对响应错误做点什么
    return Promise.reject(error);
  });

export default service
