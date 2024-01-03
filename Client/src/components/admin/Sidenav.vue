<script setup>
import DashboardIcon from '@/components/admin/icons/Dashboard.vue';
import CategoryIcon from '@/components/admin/icons/Category.vue'
import ProductIcon from '@/components/admin/icons/Product.vue'
import SaleIcon from '@/components/admin/icons/Sale.vue'
import HomeIcon from '@/components/admin/icons/Home.vue'
import LogoutIcon from '@/components/admin/icons/Logout.vue'
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import Swal from 'sweetalert2'

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

const authStore = useAuthStore()
const router = useRouter()
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
    <aside class="flex flex-col p-2 pr-0">
        <nav class="flex flex-col text-[25px] gap-2 box-border">
            <RouterLink :to="{ name: 'admin-dashboard' }" active-class="bg-gradient-to-r from-slate-800 to-slate-950"
                class="duration-200 ease-linear flex items-center gap-2 rounded-xl p-1 hover:bg-slate-800 "
                title="Dashboard">
                <DashboardIcon class="fill-white min-w-[50px] min-h-[50px] max-w-[50px] max-h-[50px]" />
                <span class="max-sm:hidden">
                    Dashboard
                </span>
            </RouterLink>
            <RouterLink :to="{ name: 'admin-category' }" active-class=" bg-gradient-to-r from-slate-800 to-slate-950"
                class="duration-200 ease-linear flex items-center gap-2 rounded-xl p-1 hover:bg-slate-800" title="Category">
                <CategoryIcon class="fill-white min-w-[50px] min-h-[50px] max-w-[50px] max-h-[50px]" />
                <span class="max-sm:hidden">
                    Category
                </span>
            </RouterLink>
            <RouterLink :to="{ name: 'admin-product' }" active-class=" bg-gradient-to-r from-slate-800 to-slate-950"
                class="duration-200 ease-linear flex items-center gap-2 rounded-xl p-1 hover:bg-slate-800" title="Product">
                <ProductIcon class="fill-white min-w-[50px] min-h-[50px] max-w-[50px] max-h-[50px]" />
                <span class="max-sm:hidden">
                    Product
                </span>
            </RouterLink>
            <RouterLink :to="{ name: 'admin-sale' }" active-class=" bg-gradient-to-r from-slate-800 to-slate-950"
                class="duration-200 ease-linear flex items-center gap-2 rounded-xl p-1 hover:bg-slate-800" title="Product">
                <SaleIcon class="fill-white min-w-[50px] min-h-[50px] max-w-[50px] max-h-[50px]" />
                <span class="max-sm:hidden">
                    Sale
                </span>
            </RouterLink>
            <RouterLink :to="{ name: 'home' }"
                class="duration-200 ease-linear flex items-center gap-2 rounded-xl p-1 hover:bg-slate-800" title="Product">
                <HomeIcon class="min-w-[50px] min-h-[50px] max-w-[50px] max-h-[50px]" />
                <span class="max-sm:hidden">
                    Goto Homepage
                </span>
            </RouterLink>
            <button @click="handleLogout"
                class="duration-200 ease-linear flex items-center gap-2 rounded-xl p-1 hover:bg-slate-800" title="Product">
                <LogoutIcon class="min-w-[50px] min-h-[50px] max-w-[50px] max-h-[50px]" />
                <span class="max-sm:hidden">
                    Log out
                </span>
            </button>
        </nav>
    </aside>
</template>