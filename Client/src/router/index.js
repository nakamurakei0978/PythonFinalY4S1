import { createRouter, createWebHistory } from 'vue-router'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/auth-register',
      name: 'register',
      component: () => import('@/views/RegisterView.vue')
    },
    {
      path: '/auth-login',
      name: 'login',
      component: () => import('@/views/LoginView.vue')
    },
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/web/HomeView.vue')
    }, {
      path: '/product',
      name: 'product',
      component: () => import('@/views/web/ProductView.vue')
    }
    , {
      path: '/admin',
      name: 'admin-dashboard',
      component: () => import('@/views/admin/DashboardView.vue'),
      meta: {
        requiresAdmin: true,
      },
    },
    {
      path: '/admin/category',
      name: 'admin-category',
      component: () => import('@/views/admin/CategoryView.vue')
    },
    {
      path: '/admin/product',
      name: 'admin-product',
      component: () => import('@/views/admin/ProductView.vue')
    },
    {
      path: '/admin/sale',
      name: 'admin-sale',
      component: () => import('@/views/admin/SaleView.vue')
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: () => import('@/views/FourOFour.vue')
    }
  ]
})


export default router
