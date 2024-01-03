<script setup>
import { ref } from 'vue'
import SearchIcon from '@/components/admin/icons/Search.vue'
import AddIcon from '@/components/admin/icons/Add.vue'
import NextIcon from '@/components/admin/icons/Next.vue'
import ReloadIcon from '@/components/admin/icons/Reload.vue'
import { useProductStore } from '@/stores/product'

const productStore = useProductStore()
const props = defineProps({
    title: String
})

async function handleLimit(){
    if(productStore.isSearchClicked){
        productStore.page = 1
        await productStore.searchProducts(productStore.holdSearchText)
    }else{
        productStore.page = 1
        await productStore.getProducts()
    }
}

function handlePagination(num){
    if(productStore.isSearchClicked){
        if(num === -1){
            productStore.page === 1 ? '': productStore.page -= 1
            productStore.searchProducts(productStore.holdSearchText)
        }
        if(num === 1){
            productStore.page === productStore.totalPage ? '': productStore.page += 1
            productStore.searchProducts(productStore.holdSearchText)
        }
    }else{
        if(num === -1){
            productStore.page === 1 ? '': productStore.page -= 1
            productStore.getProducts()
        }
        if(num === 1){
            productStore.page === productStore.totalPage ? '': productStore.page += 1
            productStore.getProducts()
        }
    }
}


const search = ref('')
function handleSearch(){
    if(search.value){
        productStore.isSearchClicked=true
        productStore.page = 1
        productStore.searchProducts(search.value)
        productStore.holdSearchText = search.value
    }

}

function handleResetSearch(){
    productStore.isSearchClicked = false
    search.value =''
    productStore.holdSearchText = ''
    productStore.page = 1
    productStore.getProducts()
}
</script>

<template>
    <section class="bg-gradient-to-r max-md:flex-col gap-3 from-slate-950 to-slate-800 text-white flex rounded-xl px-3 py-1 items-center justify-between"> 
        <span class="flex items-center gap-3">
            <h1 class="text-2xl">{{title}}</h1>
            <div class="flex gap-3">
                <AddIcon @click="productStore.isAddClicked = true" class="w-[35px] h-[35px] cursor-pointer hover:bg-slate-800 p-1 rounded-xl duration-200" title="Add category"/>
                <select @change="handleLimit" v-model="productStore.limitRows" name="limit" class="text-white bg-transparent border-2 rounded-xl p-1 focus:outline-none">
                    <option class="bg-slate-950" value="20">20</option>
                    <option class="bg-slate-950" value="40">40</option>
                    <option class="bg-slate-950" value="100">100</option>
                    <option class="bg-slate-950" value="All">All</option>
                </select>
            </div>
        </span>
        <span class="flex items-center gap-3">
            <button @click="handlePagination(-1)" class="p-1 border-2 rounded-xl hover:bg-slate-800 duration-200">
                <NextIcon class="h-5 rotate-180" />
            </button>
            {{ productStore.page }}/{{productStore.totalPage}}
            <button @click="handlePagination(1)" class="p-1 border-2 rounded-xl hover:bg-slate-800 duration-200">
                <NextIcon class="h-5" />
            </button>
        </span>
        <span class="relative max-md:w-full flex">
            <button @click="handleResetSearch" class="mr-3 hover:bg-slate-700 rounded-xl duration-200" title="Reset search">
                <ReloadIcon class="h-[35px] w-[35px] "/>
            </button>
            <input v-model="search" type="search" placeholder="Search..." class="max-md:w-full bg-white rounded-xl p-2 text-black focus:outline-none pr-10">
                <SearchIcon @click="handleSearch" class="w-[35px] h-[35px] p-1 absolute top-[2.5px] right-[3px] bg-slate-950 rounded-xl cursor-pointer hover:bg-slate-800 duration-200 " />
        </span>
    </section>  
</template>