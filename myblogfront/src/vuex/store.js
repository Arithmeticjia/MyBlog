import Vue from 'vue'
import Vuex from 'vuex'
Vue.use(Vuex)

const state = {
    count: 0,
    adminleftnavnum:"/"  //管理后台左侧导航
}
const mutations = {
    increment (state) {
        state.count++
    }
}
// const actions = {...}
//注册Store
export default new Vuex.Store({
    state,
    mutations
});
