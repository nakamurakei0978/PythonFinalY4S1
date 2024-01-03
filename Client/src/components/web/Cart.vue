<script setup>
import { onMounted, ref } from 'vue';
import { useCartStore } from '@/stores/cart.js'
import { useProductStore } from '@/stores/product.js'
import router from '@/router';
import { useAuthStore } from '@/stores/auth'
import Swal from 'sweetalert2'
import { stringify } from 'postcss';

const productStore = useProductStore()
const cartStore = useCartStore()
const authStore = useAuthStore()


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

function formatToDollar(price) {
    let USDollar = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
    })
    return USDollar.format(price)
}

function handleRemove(item) {
    const product = productStore.products.find(p => p.id === item.id)
    product.qty += item.qty
    cartStore.items = cartStore.items.filter(i => i.id !== item.id)
    Toast.fire({
        icon: "error",
        title: "Removed",
        showCloseButton: 'true'
    })
}

const isCheckout = ref(false)
async function handleCheckout() {
    if (cartStore.totalItems > 0) {
        if (authStore.isLoggedIn) {
            isCheckout.value = true
            // const res = await fetch('http://192.168.100.11:5000/stripe_payment', {
            //     method: 'POST',
            //     body: JSON.stringify({
            //         "items": cartStore.items
            //     }),
            //     headers: {
            //         'Content-Type': 'application/json'
            //     }
            // })
            // const url = await res.json()
            // window.location.href = url.url
            
            Swal.fire({
                title: "Confirm Payment?",
                text: "You won't be able to revert back!",
                icon: "warning",
                showCancelButton: true,
                confirmButtonColor: "#3085d6",
                cancelButtonColor: "#d33",
                confirmButtonText: "Yes, confirm payment",
                background: "black"
            }).then(async(result) => {
                if (result.isConfirmed) {
                    try{
                        const token = localStorage.getItem('token')
                        const items = cartStore.items
                        const data = ref([])
                        for(const i of items){
                            const product_id = i.id
                            const qty = i.qty
                            data.value.push({product_id, qty})
                        }

                        const res = await fetch('http://localhost:5000/checkout',{
                            method: 'POST',
                            headers: {
                                'content-type':'application/json',
                                'x-access-token': token
                            },
                            body: JSON.stringify(data.value),
                        })
                        console.log(res);
                    }catch(err){
                        console.log(err)
                    }
                    Swal.fire({
                        title: "Paid",
                        text: "Item has been paid.",
                        icon: "success"
                    });
                    cartStore.items = []
                }
            })
            isCheckout.value = false
        } else {
            Swal.fire({
                icon: "error",
                title: "Oops...",
                text: "Please first login first!",
                background: "black"
            })
        }
    } else {
        Swal.fire({
            icon: "error",
            title: "Oops...",
            text: "No item in cart!",
            background: "black"
        });
    }
}
</script>

<template>
    <div class="drawer">
        <input id="my-drawer" type="checkbox" class="drawer-toggle" />
        <div class="drawer-content">
            <label for="my-drawer" class="btn btn-ghost btn-square drawer-button">
                <div class="indicator">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
                        stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                    </svg>
                    <span class="badge badge-sm indicator-item">{{ cartStore.totalItems }}</span>
                </div>
            </label>
        </div>
        <div class="drawer-side z-[100]">
            <label for="my-drawer" aria-label="close sidebar" class="drawer-overlay"></label>
            <ul class="p-4 w-[450px] min-h-full bg-base-200 text-base-content relative">
                <div class="text-xl flex justify-between items-center">
                    <span>Cart</span>
                    <label for="my-drawer" class="btn btn-ghost btn-square">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24"
                            stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </label>
                </div>
                <div>
                    <li class="flex py-6" v-for="i in cartStore.items">
                        <div class="h-24 w-24 flex-shrink-0 overflow-hidden rounded-md border border-gray-200">
                            <img :src="'http://192.168.100.11:5000/storage/products/' + i.image"
                                alt="Front of satchel with blue canvas body, black straps and handle, drawstring top, and front zipper pouch."
                                class="h-full w-full object-cover object-center">
                        </div>

                        <div class="ml-4 flex flex-1 flex-col">
                            <div>
                                <div class="flex justify-between text-base font-medium text-white">
                                    <h3>
                                        <a href="#">{{ i.name }}</a>
                                    </h3>
                                    <p class="ml-4">{{ formatToDollar(i.subPrice) }}</p>
                                </div>
                                <p class="mt-1 text-sm text-gray-500">{{ i.category }}</p>
                            </div>
                            <div class="flex flex-1 items-center justify-between text-sm">
                                <p class="text-gray-500">Qty {{ i.qty }}</p>
                                <div class="flex">
                                    <button type="button" @click="handleRemove(i)"
                                        class="font-medium text-red-400 hover:text-red-500">Remove</button>
                                </div>
                            </div>
                        </div>
                    </li>
                </div>
                <div class="h-[200px] grid place-items-center"></div>
                <li class="absolute bottom-0 w-full left-0 bg-base-200">
                    <div class="border-t border-gray-200 px-4 py-6 sm:px-6">
                        <div class="flex justify-between text-base font-medium text-white">
                            <p>Subtotal</p>
                            <p>{{ formatToDollar(cartStore.subTotal) }}</p>
                        </div>
                        <p class="mt-0.5 text-sm text-gray-500">Shipping and taxes calculated at checkout.</p>
                        <div class="mt-6">
                            <a @click="handleCheckout"
                                class="flex items-center justify-center rounded-md border border-transparent bg-indigo-600 px-6 py-3 text-base font-medium text-white shadow-sm hover:bg-indigo-700 cursor-pointer">
                                <span v-if="isCheckout" class="loading loading-spinner loading-md mr-3"></span>
                                Checkout
                            </a>
                        </div>
                        <div class="mt-6 flex justify-center text-center text-sm text-gray-500">
                            <p>
                                or
                                <label for="my-drawer"
                                    class="font-medium cursor-pointer text-indigo-600 hover:text-indigo-500">
                                    Continue Shopping
                                    <span aria-hidden="true"> &rarr;</span>
                                </label>
                            </p>
                        </div>
                    </div>
                </li>
            </ul>
        </div>
    </div>
</template>