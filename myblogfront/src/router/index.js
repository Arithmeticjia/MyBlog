import Vue from 'vue'
import Router from 'vue-router'
import VueResource from 'vue-resource'
import ElementUI from 'element-ui'
import vueCanvasNest from 'vue-canvas-nest'
import '../assets/element-#545C64/index.css'
import '../assets/iconfont/iconfont.css'
import '../assets/iconfont/iconfont.js'

Vue.use(VueResource)
Vue.use(Router)
Vue.use(ElementUI)
Vue.use(vueCanvasNest)
// Vue.use(ElementUI, { locale })

Vue.component('vue-canvas-nest', vueCanvasNest)

//解决编程式路由往同一地址跳转时会报错的情况
const originalPush = Router.prototype.push
const originalReplace = Router.prototype.replace
//push
Router.prototype.push = function push(location, onResolve, onReject) {
    if (onResolve || onReject) return originalPush.call(this, location, onResolve, onReject)
    return originalPush.call(this, location).catch(err => err)
}
//replace
Router.prototype.replace = function push(location, onResolve, onReject) {
    if (onResolve || onReject) return originalReplace.call(this, location, onResolve, onReject)
    return originalReplace.call(this, location).catch(err => err)
}

const router = new Router({
  mode: 'history',  //去掉url中的#
  routes: [
    {
      path: '/index',
      name: 'Index',
      component: () => import('@/components/Index')
    },
    {
      path: '/hello',
      name: 'HelloWorld',
      component: () => import('@/components/HelloWorld')
    },
    {
      path: '/list',
      name: 'BlogList',
      component: () => import('@/components/BlogList')
    },
    {
      path: '/',
      name: 'VueDjango',
      component: () => import('@/components/VueDjango')
    },
    {
      path: '/home',
      name: 'home',
      component: () => import('@/components/Home')
    },
    {
      path: '/archive',
      name: 'archive',
      component: () => import('@/components/Archive')
    },
    {
      path: '/post/:id',
      name: 'post',
      component: () => import('@/components/Single')
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('@/components/About'),
    },
    {
      path: '*',
      name: 'notfound',
      component: () => import('@/components/NotFound')
    },
    {
      path: '/404',
      name: 'notfound',
      component: () => import('@/components/NotFound')
    },
    {
      path: '/category',
      name: 'category',
      component: () => import('@/components/Category')
    },
    {
      path: '/category/:name',
      name: 'categorypagetimeline',
      component: () => import('@/components/CategoryPageTimeline')
    },
    {
      path: '/tag/:name',
      name: 'tagpagetimeline',
      component: () => import('@/components/TagPageTimeline')
    },
    {
      path: '/categorytimeline/:name',
      name: 'categorypagetimeline',
      component: () => import('@/components/CategoryPage')
    },
    {
      path: '/love',
      name: 'love',
      meta: {
        requiresAuth: true  //需要登录才能访问
      },
      component: () => import('@/components/Love')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/components/Login')
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
    if(to.matched.some(record => record.meta.requiresAuth)) {
      if(!token){
        next('/login');
      }else {
        next();
      }
    }
    // if ((!token || isAuth) && to.matched.some(record => record.meta.requiresAuth)) {
    //   next('/login');
    // } else {
    //   next();
    // }
  }
  if (to.matched.length === 0) {  //如果未匹配到路由
    from.name ? next({ name:from.name }) : next('/404');   //如果上级也未匹配到路由则跳转登录页面，如果上级能匹配到则转上级路由
  } else {
    next();    //如果匹配到正确跳转
  }
});
export default router;
