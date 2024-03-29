// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import i18n from './i18n/index'
import Vuetify from 'vuetify'
import store from './store'
import echarts from 'echarts'
import ElementUI from 'element-ui'
import mavonEditor from 'mavon-editor'
import vueCanvasNest from 'vue-canvas-nest'
import VueTypedJs from 'vue-typed-js'
import axios from 'axios'
import 'mavon-editor/dist/css/index.css'
import './assets/articlemarkdown.css'
import './assets/global.css'
import locale from 'element-ui/lib/locale/lang/en'

Vue.use(ElementUI, { locale })
Vue.use(mavonEditor)
Vue.use(axios)
Vue.use(vueCanvasNest)
Vue.use(Vuetify)
Vue.use(VueTypedJs)
Vue.prototype.$echarts = echarts
Vue.config.productionTip = false
Vue.prototype.$axios = axios

/* eslint-disable no-new */
new Vue({
  el: '#app',
  i18n,
  store,
  router,
  vuetify: new Vuetify(),
  components: { App },
  template: '<App/>'
})


Vue.http.interceptors.push((request, next) => {
    let timeout;
    // 如果某个请求设置了_timeout,那么超过该时间，会终端该（abort）请求,并执行请求设置的钩子函数onTimeout方法，不会执行then方法。
    if (request._timeout) {
        timeout = setTimeout(() => {
            if(request.onTimeout) {
                request.onTimeout(request);
                request.abort()
            }
        }, request._timeout);
    }
    next((response) => {
       clearTimeout(timeout);
　　　　return response;
    })
})
