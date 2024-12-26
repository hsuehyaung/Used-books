import Vue from 'vue';
import VueRouter from 'vue-router';
import Checkout from '/src/components/Checkout.vue';

Vue.use(VueRouter);

const routes = [
  // 其他路由
  {
    path: '/checkout',
    name: 'Checkout',
    component: Checkout
  }
];

const router = new VueRouter({
  routes
});

export default router;