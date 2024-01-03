<script setup>
import { ref } from 'vue';
import SearchIcon from '@/components/admin/icons/Search.vue'
import AddIcon from '@/components/admin/icons/Add.vue'
import NextIcon from '@/components/admin/icons/Next.vue'
import ReloadIcon from '@/components/admin/icons/Reload.vue'
import { useCategoryStore } from '@/stores/category';

const categoryStore = useCategoryStore()
const limitRows = ref(20)
const  searchText = ref('')


const props = defineProps({
    title: String,
    search: Boolean,
    add: Boolean
})

const isAdd = ref(false)
function handleAdd(title){
    if(title === 'Category'){
        categoryStore.addButton()
        isAdd.value = categoryStore.isAddClicked 
    }
}

function handleLimitRows(title){
    if(title === 'Category'){
        if(categoryStore.haveSearchClicked){
            categoryStore.page = 1
            categoryStore.totalPage = 1
            categoryStore.limitRows = limitRows.value
            categoryStore.searchCategories(categoryStore.holdSearchText)
        }else{
            categoryStore.page = 1
            categoryStore.totalPage = 1
            categoryStore.getCategories(limitRows.value)
        }
    }
}

function handlePagination(num, title){
    if(title === 'Category'){
        if(categoryStore.haveSearchClicked){
            if(num === -1){
                categoryStore.page === 1 ? '' : categoryStore.page -= 1
                categoryStore.searchCategories(categoryStore.holdSearchText)
            }
            if(num === 1){
                categoryStore.page === categoryStore.totalPage ? '' : categoryStore.page += 1 
                categoryStore.searchCategories(categoryStore.holdSearchText)
            }
        }else{
            if(num === -1){
                categoryStore.page === 1 ? '' : categoryStore.page -= 1
                categoryStore.getCategories(categoryStore.limitRows)
            }
            if(num === 1){
                categoryStore.page === categoryStore.totalPage ? '' : categoryStore.page += 1 
                categoryStore.getCategories(categoryStore.limitRows)
            }
        }
    }
}

function handleSearch(title){
    if(searchText.value && title === 'Category'){
        categoryStore.page = 1
        categoryStore.totalPage = 1
        categoryStore.searchCategories(searchText.value)
        categoryStore.holdSearchText = searchText.value
        categoryStore.haveSearchClicked = true
    }
}

function handleResetSearch(){
    categoryStore.holdSearchText=''
    searchText.value =''
    categoryStore.haveSearchClicked = false
    categoryStore.page = 1
    categoryStore.getCategories(limitRows.value)
}

</script>

<template>
    <section class="bg-gradient-to-r max-md:flex-col gap-3 from-slate-950 to-slate-800 text-white flex rounded-xl px-3 py-1 items-center justify-between"> 
        <span class="flex items-center gap-3">
            <h1 class="text-2xl">{{title}}</h1>
            <div class="flex gap-3">
                <AddIcon @click="handleAdd(title)" :class="isAdd?'bg-slate-800':''" class="w-[35px] h-[35px] cursor-pointer hover:bg-slate-800 p-1 rounded-xl duration-200" title="Add category"/>
                <select @change="handleLimitRows(title)" v-model="limitRows" name="limit" class="text-white bg-transparent border-2 rounded-xl p-1 focus:outline-none">
                    <option class="bg-slate-950" value="20">20</option>
                    <option class="bg-slate-950" value="40">40</option>
                    <option class="bg-slate-950" value="100">100</option>
                    <option class="bg-slate-950" value="All">All</option>
                </select>
            </div>
        </span>
        <span class="flex items-center gap-3">
            <button @click="handlePagination(-1,title)" class="p-1 border-2 rounded-xl hover:bg-slate-700 duration-200">
                <NextIcon class="h-5 rotate-180" />
            </button>
            {{ categoryStore.page }}/{{categoryStore.totalPage}}
            <button @click="handlePagination(1,title)" class="p-1 border-2 rounded-xl hover:bg-slate-700 duration-200">
                <NextIcon class="h-5" />
            </button>
        </span>
        <span class="relative max-md:w-full flex">
            <button @click="handleResetSearch" class="mr-3 hover:bg-slate-700 rounded-xl duration-200" title="Reset search">
                <ReloadIcon class="h-[35px] w-[35px] "/>
            </button>
            <input v-model="searchText" v-if="search" type="search" placeholder="Search..." class="max-md:w-full rounded-xl p-2 text-black focus:outline-none pr-10 bg-white">
                <SearchIcon @click="handleSearch(title)" class="w-[35px] h-[35px] p-1 absolute top-[2.5px] right-[3px] bg-slate-950 rounded-xl cursor-pointer hover:bg-slate-700 duration-200" />
        </span>
    </section>  
</template>