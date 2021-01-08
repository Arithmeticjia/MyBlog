import Vue from 'vue' //引入 Vue
import Vuex from 'vuex' //引入 Vuex
import user from './modules/user' //引入 user module
import VueLocalStorage from 'vue-localstorage'

Vue.use(Vuex);

const store = new Vuex.Store({
  modules: {
    user, //使用 user.js 中的 action
  },
  state: {
    // 存储token
    Authorization: localStorage.getItem('Authorization') ? localStorage.getItem('Authorization') : '',
    // 存储用户名
    Username: localStorage.getItem('Username') ? localStorage.getItem('Username') : ''
  },
  getters: {
    userName: (state) => state.Username,
    Authorization: (state) => state.Authorization
  },
  mutations: {
    // 修改token，并将token存入localStorage
    changeLogin (state, user) {
      state.Authorization = user.Authorization;
      state.Username = user.Username;
      localStorage.setItem('Authorization',user.Authorization);
      localStorage.setItem('Username', user.Username);
    }
  },
});
export default store
