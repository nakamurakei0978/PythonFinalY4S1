<script setup>
import { ref } from 'vue'
import { useSaleStore } from '@/stores/sale';
import SpinnerIcon from '@/components/admin/icons/Spinner.vue'
import Swal from 'sweetalert2'

const saleStore = useSaleStore()

const props = defineProps({
    sale: Object
})

function formatToDollar(price) {
  let USDollar = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  })
  return USDollar.format(price)
}



</script>

<template>
    <div @click="$event.currentTarget === $event.target ? saleStore.isViewClicked = false : ''"
        class="absolute grid place-items-center w-[calc(100%+40px)] h-[calc(100%+40px)] bg-black/50 backdrop-blur top-[-20px] left-[-20px] rounded-xl backdrop:rounded-xl">
        <div class="bg-slate-950 text-white p-5 rounded-xl">
            <section class="flex justify-end mb-3">
                <button @click="saleStore.isViewClicked = false" class="bg-red-500 w-[35px] h-[35px] rounded-xl">X</button>
            </section>
            <section class="flex gap-32 justify-between">
                <span>Sale id: {{ sale.id }}</span>
                <span>Purchase date: {{ sale.date }}</span>
            </section>
            <section class="flex gap-32 justify-between">
                <span>User: {{ sale.user }}</span>
                Total purchased: {{ formatToDollar(sale.total) }}
            </section>
            <section class="overflow-auto max-h-[calc(100vh-300px)] bg-white p-3 mt-3 divide-y-2 rounded-xl text-black"> 
                <div class="grid grid-cols-4 text-xl">
                    <div>Product</div>
                    <div>Qty</div>
                    <div>Price</div>
                    <div>Sub total</div>
                </div>
                <div class="grid grid-cols-4" v-for="p in sale.details">
                    <div>{{ p.product_name }}</div>
                    <div>{{ p.qty }}</div>
                    <div>{{ formatToDollar(p.price) }}</div>
                    <div>{{ formatToDollar(p.price * p.qty) }}</div>
                </div>
            </section>
        </div>
    </div>
</template>