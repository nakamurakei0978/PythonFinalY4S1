import { defineStore } from "pinia"
import { ref } from "vue"


export const useSaleStore = defineStore('sale',()=>{
    const sale_lists = ref([])
    const page = ref(1)
    const totalPage = ref(1)
    const isViewClicked = ref(false)

    async function getSaleLists(limit){
        try{
            const res = await fetch(`http://localhost:5000/sale?limit=${limit}&page=${page.value}`)
            const data = await res.json()
            sale_lists.value = data.sales
            totalPage.value = data.totalPage
        }catch(err){
            console.log(err);
        }
    }



    return{
        sale_lists, getSaleLists, page, totalPage, isViewClicked
    }
})