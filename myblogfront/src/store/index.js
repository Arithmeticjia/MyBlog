import Vue from 'vue'
import Vuex from 'vuex'
import user from './modules/user'

Vue.use(Vuex);

const store = new Vuex.Store({
  modules: {
    user, //使用 user.js 中的 action
  },
  state: {
    // 存储token
    Authorization: localStorage.getItem('Authorization') ? localStorage.getItem('Authorization') : '',
    // 存储用户名
    Username: localStorage.getItem('Username') ? localStorage.getItem('Username') : '',
    // 存储粒子特效开关状态
    Canvas: true
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
    },
    changeCanvas (state) {
      state.Canvas = false;
    }
  },
});

export default store
