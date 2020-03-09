import Vue from 'vue'
import Router from 'vue-router'
import VueResource from 'vue-resource'
import HelloWorld from '@/components/HelloWorld'
import VueDjango from '@/components/VueDjango'
import BlogList from '@/components/BlogList'
import BlogIndex from '@/components/BlogIndex'
import Archive from '@/components/Archive'
import Home from '@/components/Home'
import Single from '@/components/Single'
import About from '@/components/About'
import ElementUI from 'element-ui'
// import 'element-ui/lib/theme-chalk/index.css'
import '../assets/element-#545C64/index.css'
import '../assets/iconfont/iconfont.css'
import '../assets/iconfont/iconfont.js'

Vue.use(VueResource)
Vue.use(Router)
Vue.use(ElementUI)


export default new Router({
  routes: [
    {
      path: '/blogindex',
      name: 'BlogIndex',
      component: BlogIndex
    },
    {
      path: '/bloglist',
      name: 'BlogList',
      component: BlogList
    },
    {
      path: '/',
      name: 'VueDjango',
      component: VueDjango
    },
    {
      path: '/home',
      name: 'home',
      component: Home
    },
    {
      path: '/archive',
      name: 'archive',
      component: Archive
    },
    {
      path: '/single/:id',
      name: 'single',
      component: Single
    },
    {
      path: '/about',
      name: 'about',
      component: About
    },
  ]
})
