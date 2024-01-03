<script setup>
import Cart from '@/components/web/Cart.vue'
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';
import Swal from 'sweetalert2'

const authStore = useAuthStore()
const router = useRouter()

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

function handleLogout() {
    Swal.fire({
        title: "Are you sure?",
        text: "You about to logout.",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Yes, Logout"
    }).then(async (result) => {
        if (result.isConfirmed) {
            localStorage.removeItem('token')
            authStore.isLoggedIn = false
            authStore.isAdmin = false
            router.push({ name: 'login' })
            Toast.fire({
                icon: "success",
                title: "Logout successfully",
                showCloseButton: 'true'
            })
            // Swal.fire({
            //     title: "Logged Out!",
            //     text: "Log out successfully.",
            //     icon: "success"
            // })
        }
    })
}
</script>

<template>
    <div class="navbar bg-base-100 sticky top-0 z-40 px-5">
        <div class="flex-none w-[96px]">
            <a class="btn btn-ghost text-xl">Y4S3</a>
        </div>
        <ul class="menu menu-horizontal rounded-box flex-1 gap-2 justify-center">
            <li>
                <RouterLink active-class="btn-active" class="btn btn-ghost text-xl" :to="{ name: 'home' }">Home</RouterLink>
            </li>
            <li>
                <RouterLink active-class="btn-active" class="btn btn-ghost text-xl" :to="{ name: 'product' }">Product
                </RouterLink>
            </li>
        </ul>
        <div class="flex-none">
            <Cart />
            <div class="dropdown dropdown-end">
                <div tabindex="0" role="button" class="btn btn-ghost btn-square avatar">
                    <div class="w-10 rounded-full">
                        <img alt="Tailwind CSS Navbar component" src="../../assets//images/Untitled.png" />
                    </div>
                </div>
                <ul tabindex="0" class="menu menu-sm dropdown-content mt-3 z-[1] p-2 shadow bg-base-100 rounded-box w-52">
                    <li v-if="authStore.isLoggedIn">
                        <a class="justify-between">
                            Profile
                            <span class="badge">New</span>
                        </a>
                    </li>
                    <li v-if="authStore.isAdmin">
                        <RouterLink :to="{ name: 'admin-dashboard' }" active-class="bg-slate-800">Admin</RouterLink>
                    </li>
                    <li v-if="authStore.isLoggedIn"><a>Settings</a></li>
                    <li v-if="!authStore.isLoggedIn">
                        <RouterLink :to="{ name: 'login' }" active-class="bg-slate-800">Login</RouterLink>
                    </li>
                    <li v-if="!authStore.isLoggedIn">
                        <RouterLink :to="{ name: 'register' }" active-class="bg-slate-800">Register</RouterLink>
                    </li>
                    <li @click="handleLogout" v-if="authStore.isLoggedIn"><a>Logout</a></li>
                </ul>
            </div>
        </div>

    </div>
</template>