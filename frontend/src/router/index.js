import Vue from 'vue';
import Router from 'vue-router';
import TodoList from '../components/TodoList.vue';
import Check from '../components/Check.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'TodoList',
      component: TodoList,
    },
    {
      path: '/check',
      name: 'Check',
      component: Check,
    },
  ],
});

