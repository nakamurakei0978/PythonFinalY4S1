<script setup>
import { onMounted, ref } from 'vue';
import { useAuthStore } from '@/stores/auth';
import {useRouter} from 'vue-router';
import Swal from 'sweetalert2'
import { useCartStore } from '@/stores/cart';

const cartStore = useCartStore()
const router = useRouter()
const loading = ref(true)
const authStore = useAuthStore()
const username = ref('')
const password = ref('')

const Toast = Swal.mixin({
    toast: true,
    position: "top-end",
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
    didOpen: (toast) => {
        toast.onmouseenter = Swal.stopTimer;
        toast.onmouseleave = Swal.resumeTimer;
    }
})

onMounted(()=>{
    loading.value=false
})


async function handleSubmit(){
    try{
        const credentials = btoa(`${username.value}:${password.value}`)
        const res = await fetch('http://127.0.0.1:5000/login',{
            headers: {
                'Authorization': 'Basic '+credentials
            }
        })
        const data = await res.json()
        localStorage.setItem('token', data.token)
        authStore.isLoggedIn = true
        await authStore.checkAdmin()
        authStore.isAdmin ? router.push({name:'admin-dashboard'}): router.push({name:'home'})
        Toast.fire({
            icon: "success",
            title: "Login successfully",
            showCloseButton: 'true'
        })
        cartStore.items = []
    }catch(err){
        console.log(err);
        Toast.fire({
            icon: "error",
            title: "Something is wrong!",
            showCloseButton: 'true'
        })
    }
}

</script>

<template>
    <Transition name="fade">
        <div v-if="loading" class="grid place-items-center h-[100dvh] fixed top-0 left-0 w-screen">
            <span class="loading loading-infinity loading-lg scale-150"></span>
        </div>
    </Transition>
    <Transition name="fade">
        <div class="h-[calc(100dvh-80px)] grid place-items-center">
            <form v-on:submit.prevent="handleSubmit" class="grid grid-cols-1 gap-2">
                <label for="username">Username</label>
                <input v-model="username" type="text" required placeholder="Type here"
                    class="input input-bordered w-full max-w-xs" />
                <label for="password">Password</label>
                <input v-model="password" type="text" required placeholder="Type here"
                    class="input input-bordered w-full max-w-xs" />
                <button type="submit" class="btn">Submit</button>
                <div class="text-center">
                    <p>
                        Haven't had an account yet? 
                    </p>
                    <RouterLink class="text-blue-500 hover:text-blue-300" :to="{name: 'register'}">Let's register an account.</RouterLink>
                </div>
            </form>
        </div>
    </Transition>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
    /* use the transition utility classes from Tailwind CSS */
    @apply transition-opacity duration-500 ease-in-out;
}

.fade-enter-from,
.fade-leave-to {
    /* use the opacity utility class from Tailwind CSS */
    @apply opacity-0;
}
</style>