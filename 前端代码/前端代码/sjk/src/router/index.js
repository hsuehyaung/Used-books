import Vue from 'vue'
import VueRouter from 'vue-router'
import LogRes from '@/components/MyLogReg'
import user from '@/components/MyUser'
import manage from '@/components/MyManage'
import UserShop from '@/components/UserShop';
import BookImg from '@/components/BookImg';

Vue.use(VueRouter)
export default new VueRouter({
    mode:'history',
    routes: [
        {
            path:'/',
            redirect:'/login'
        },
        {
            path: '/login',
            component: LogRes,
            meta: {
                title: "登录"
            },
        },
        {
            path: '/user',
            component: user,
            meta: {
                title: "用户界面"
            }
        },
        {
            path: '/manage',
            component: manage,
            meta: {
                title: "后台管理界面"
            }
        },
        {
            path: '/usershop',
            name: 'UserShop',
            component: UserShop
          },
          {
            path: '/bookimg/:bookName',
            name:'bookpage',
            component: BookImg
          },
    ]
})
