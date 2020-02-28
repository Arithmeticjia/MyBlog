import Vue from 'vue'
import Router from 'vue-router'
import VueResource from 'vue-resource'
import HelloWorld from '@/components/HelloWorld'
import VueDjango from '@/components/VueDjango'
import BlogList from '@/components/BlogList'
import BlogIndex from '@/components/BlogIndex'
import VueWordCloud from '@/components/VueWordCloud'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import '../assets/iconfont/iconfont.css'
import '../assets/iconfont/iconfont.js'

Vue.use(VueResource)
Vue.use(Router)
Vue.use(ElementUI)


export default new Router({
  routes: [
    {
      path: '/blogindex',
      name: 'BlogList',
      component: BlogList
    },
    {
      path: '/bloglist',
      name: 'BlogIndex',
      component: BlogIndex
    },
    {
      path: '/',
      name: 'VueDjango',
      component: VueDjango
    },
    {
      path: '/vuewordcloud',
      name: 'VueDjango',
      component: VueWordCloud
    },
  ]
})
