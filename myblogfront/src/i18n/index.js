import Vue from 'vue'
import VueI18n from 'vue-i18n'
import ElementLocale from 'element-ui/lib/locale'
import enLocale from 'element-ui/lib/locale/lang/en'
import zhLocale from 'element-ui/lib/locale/lang/zh-CN'
import langZh from "@/assets/languages/zh.js"
import langEN from "@/assets/languages/en.js"


Vue.use(VueI18n)

let lang = window.sessionStorage.getItem('lang')||'zh'

const i18n = new VueI18n({

  locale: lang,
  messages: {
    'zh': {...langZh,...zhLocale},
    'en': {...langEN,...enLocale}
  }
})
// Vue.use(VueI18n)
//
// let lang = window.sessionStorage.getItem('lang')||'zh'
//
// const messages = {
//   "en": langEN,
//   "zh": langZh
// }
//
// const i18n = new VueI18n({
//
//   messages,
//   locale: lang,
//
// })

ElementLocale.i18n((key, value) => i18n.t(key, value))

export default i18n
