<script setup>
import { RouterLink, RouterView, useRoute } from 'vue-router'
import Sidenav from './components/admin/Sidenav.vue'
import Navbar from '@/components/web/Navbar.vue'
import { ref, computed, onMounted, onBeforeMount } from 'vue';
import { useAuthStore } from './stores/auth';
import router from './router'


const authStore = useAuthStore()
const loading = ref(true)
onMounted(async () => {
  loading.value = true
  try {
    await authStore.checkLogin()
    await authStore.checkAdmin()
  } catch (err) {
    console.log(err);
  }
  loading.value = false
})

router.beforeEach((to, from, next) => {
  if (authStore.isLoggedIn) {
    if (to.name !== 'login' && to.name !== 'register') {
      if (authStore.isAdmin) {
        next()
      } else {
        if (!to.name.startsWith('admin')) {
          next()
        }
      }
    }
  } else {
    if (to.name.startsWith('admin')) {
      next({ name: 'login' })
    } else {
      next()
    }
  }
})


const isAdminRoute = computed(() => {
  return useRoute().path.startsWith('/admin')
})
</script>

<template>
  <!-- storefront -->
  <div v-if="!isAdminRoute" class="bg-slate-950 h-screen">
    <Navbar />
    <RouterView />
  </div>



  <!-- for admin -->
  <div v-if="isAdminRoute"
    class="h-[100dvh] grid grid-cols-[250px_1fr] max-sm:grid-cols-[66px_1fr] duration-200 overflow-hidden">
    <Sidenav />
    <div class="rounded-xl m-2 bg-white p-5 ">
      <RouterView />
    </div>
  </div>
</template>

<style scoped></style>
