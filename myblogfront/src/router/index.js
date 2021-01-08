import Vue from 'vue'
import Router from 'vue-router'
import VueResource from 'vue-resource'
import VueDjango from '@/components/VueDjango'
import BlogList from '@/components/BlogList'
import Archive from '@/components/Archive'
import Home from '@/components/Home'
import Single from '@/components/Single'
import About from '@/components/About'
import NotFound from '@/components/NotFound'
import Category from '@/components/Category'
import CategoryPage from '@/components/CategoryPage'
import Calendar from '@/components/Calendar'
import CategoryPageTimeline from '@/components/CategoryPageTimeline'
import Love from '@/components/Love'
import Login from '@/components/Login'
import ElementUI from 'element-ui'
import axios from 'axios';
import '../assets/element-#545C64/index.css'
import '../assets/iconfont/iconfont.css'
import '../assets/iconfont/iconfont.js'

Vue.use(VueResource)
Vue.use(Router)
Vue.use(ElementUI)
// Vue.use(ElementUI, { locale })

const router = new Router({
  routes: [
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
    {
      path: '*',
      name: 'notfound',
      component: NotFound
    },
    {
      path: '/404',
      name: 'notfound',
      component: NotFound
    },
    {
      path: '/category',
      name: 'category',
      component: Category
    },
    {
      path: '/category/:name',
      name: 'categorypage',
      component: CategoryPageTimeline
    },
    {
      path: '/categorytimeline/:name',
      name: 'categorypagetimeline',
      component: CategoryPage
    },
    {
      path: '/calendar',
      name: 'calendar',
      component: Calendar
    },
    {
      path: '/love',
      name: 'love',
      meta: {
        requiresAuth: true  //需要登录才能访问
      },
      component: Love
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
  ]
});

// 导航守卫
// 使用 router.beforeEach 注册一个全局前置守卫，判断用户是否登陆
router.beforeEach((to, from, next) => {
  if (to.path === '/login' || to.path === '/home') {
    next();
  } else {
    let token = localStorage.getItem('Authorization');
    let isAuth = true;
    // axios.get("http://127.0.0.1:8089/zuul/api/v1/check-login/", {
    //     headers:{
    //       'token': token
    //     }
    //   }
    //   ).then(function(result) {
    //   if(result.status === 200){
    //     isAuth = true;
    //   }
    // })
    if (!token && to.matched.some(record => record.meta.requiresAuth)) {
      next('/login');
    } else {
      next();
    }
  }
  if (to.matched.length === 0) {  //如果未匹配到路由
    from.name ? next({ name:from.name }) : next('/404');   //如果上级也未匹配到路由则跳转登录页面，如果上级能匹配到则转上级路由
  } else {
    next();    //如果匹配到正确跳转
  }
});
export default router;
