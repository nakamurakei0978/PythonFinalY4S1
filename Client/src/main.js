import './assets/css/style.css'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { useAuthStore } from './stores/auth'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
const authStore = useAuthStore()
await authStore.checkLogin()
await authStore.checkAdmin()


app.use(router)

app.mount('#app')
