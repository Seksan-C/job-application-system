import { createRouter, createWebHistory } from 'vue-router'
import JobApplicationForm from '../views/JobApplicationForm.vue';
import JobApplicationsList from '../views/JobApplicationsList.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: JobApplicationForm
    },
    {
      path: '/list',
      name: 'list',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/JobApplicationsList.vue')
    }
  ]
})

export default router
