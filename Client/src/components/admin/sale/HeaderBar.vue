<script setup>
import { ref } from 'vue';
import SearchIcon from '@/components/admin/icons/Search.vue'
import NextIcon from '@/components/admin/icons/Next.vue'
import ReloadIcon from '@/components/admin/icons/Reload.vue'
import { useSaleStore } from '@/stores/sale.js'


const saleStore = useSaleStore()
const limitRows = ref(20)
const searchText = ref('')

const props = defineProps({
    title: String
})


async function handleLimit() {
    await saleStore.getSaleLists(limitRows.value)
}

async function handlePagination(num) {
    if (num === -1 && saleStore.page > 1) {
        saleStore.page -= 1
        await saleStore.getSaleLists(limitRows.value)
    }
    if (num === 1 && saleStore.page < saleStore.totalPage) {
        saleStore.page += 1
        await saleStore.getSaleLists(limitRows.value)
    }
}


async function handleReload() {
    await saleStore.getSaleLists(limitRows.value)
}
</script>

<template>
    <section
        class="bg-gradient-to-r max-md:flex-col gap-3 from-slate-950 to-slate-800 text-white flex rounded-xl px-3 py-1 items-center justify-between">
        <span class="flex items-center gap-3">
            <h1 class="text-2xl">{{ title }}</h1>
            <div class="flex gap-3">
                <select @change="handleLimit" v-model="limitRows" name="limit"
                    class="text-white bg-transparent border-2 rounded-xl p-1 focus:outline-none">
                    <option class="bg-slate-950" value="20">20</option>
                    <option class="bg-slate-950" value="40">40</option>
                    <option class="bg-slate-950" value="100">100</option>
                    <option class="bg-slate-950" value="All">All</option>
                </select>
            </div>
        </span>
        <span class="flex items-center gap-3">
            <button @click="handlePagination(-1)" class="p-1 border-2 rounded-xl hover:bg-slate-700 duration-200">
                <NextIcon class="h-5 rotate-180" />
            </button>
            {{ saleStore.page }}/{{ saleStore.totalPage }}
            <button @click="handlePagination(1)" class="p-1 border-2 rounded-xl hover:bg-slate-700 duration-200">
                <NextIcon class="h-5" />
            </button>
        </span>
        <span class="relative max-md:w-full flex">
            <button @click="handleReload" class="mr-3 hover:bg-slate-700 rounded-xl duration-200" title="reload">
                <ReloadIcon class="h-[35px] w-[35px]" />
            </button>
            <input v-model="searchText" type="search" placeholder="Search..."
                class="hidden max-md:w-full rounded-xl p-2 text-black focus:outline-none pr-10 bg-white">
            <SearchIcon
                class="hidden w-[35px] h-[35px] p-1 absolute top-[2.5px] right-[3px] bg-slate-950 rounded-xl cursor-pointer hover:bg-slate-700 duration-200" />
        </span>
    </section>
</template>