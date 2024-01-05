<script setup>
import { ref, onMounted } from 'vue'
import { useProductStore } from '@/stores/product.js'
import { useCategoryStore } from '@/stores/category.js'
import { useCartStore } from '@/stores/cart'
import Swal from 'sweetalert2'

const loading = ref(true)
const productStore = useProductStore()
const categoryStore = useCategoryStore()
const cartStore = useCartStore()

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

onMounted(async () => {
    loading.value = true
    const res_category = await categoryStore.getCategories('All')
    const res = await productStore.getProducts()
    console.log(`category: ${res_category}, Product: ${res}`)
    loading.value = false
})

function formatToDollar(price) {
    let USDollar = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
    })
    return USDollar.format(price)
}

function getCategoryName(id) {
    try {
        const category = categoryStore.categories.find((c) => c.id === id)
        return category ? category.name : 'N/A'
    } catch (err) {
        console.log(err);
    }
}

function handleAddToCart(p, category_name) {
    cartStore.add(p, category_name)
    Toast.fire({
        icon: "success",
        title: "+1 item added",
        showCloseButton: 'true'
    })
}

</script>

<template>
    <Transition name="fade">
        <div v-if="loading" class="grid place-items-center h-[100dvh] fixed top-0 left-0 w-screen">
            <span class="loading loading-infinity loading-lg scale-150"></span>
        </div>
    </Transition>
    <Transition name="fade">
        <div v-if="!loading" class="grid place-items-center p-5 ">
            <div class="grid sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                <div class="card card-compact w-80 bg-base-100 shadow-xl" v-for="p in productStore.products">
                    <figure><img :src="'http://localhost:5000/storage/products/' + p.image" alt="Shoes" />
                    </figure>
                    <div class="card-body">
                        <div class="flex justify-between items-center">
                            <h2 class="card-title">{{ p.name }}</h2>
                            <span>{{ formatToDollar(p.price) }}</span>
                        </div>
                        <p>Qty {{ p.qty }}</p>
                        <div class="card-actions justify-between items-center">
                            <div class="badge badge-outline">{{ getCategoryName(p.category_id) }}</div>
                            <button @click="handleAddToCart(p, getCategoryName(p.category_id))" class="btn btn-primary">Add
                                to
                                cart</button>
                        </div>
                    </div>
                </div>
            </div>
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