import { defineStore } from 'pinia'
import { ref, computed } from 'vue'


export const useCartStore = defineStore('cart', () =>{
    // const item = ref([])
    const items = ref([])

    const totalItems = computed(()=>{
        return items.value.reduce((total, item)=>{
            return total += item.qty
        }, 0)
    })
    const subTotal = computed(()=>{
        return items.value.reduce((subtotal, item)=>{
            return subtotal += item.subPrice
        }, 0)
    })


    function add(p, cName){
        if(p.qty !== 0){
            const isProductExists = items.value.find((i)=>i.id === p.id)
            if(isProductExists){
                isProductExists.qty += 1
                isProductExists.subPrice += isProductExists.price            
            }else{
                const item = {...p}
                item.qty=1 
                delete item.category_id
                item.category= cName
                item.subPrice = item.price
                items.value.push(item)
            }
        }
        p.qty < 1 ? p.qty===0 : p.qty-=1
    }

    return {
        items, totalItems, add, subTotal
    }
})