import { ref } from "vue"
import { defineStore } from "pinia"
import axios from 'axios'

export const useProductStore = defineStore('product', () => {
    const products = ref([])
    const isAddClicked = ref(false)
    const isEditClicked = ref(false)
    const limitRows = ref(20)
    const page = ref(1)
    const totalPage = ref(1)
    const isSearchClicked = ref(false)
    const editProduct = ref([])


    async function postProduct(name, price, qty, category_id, imageFile){
        name = name.toLowerCase()
        let formData = new FormData()
        formData.append('name', name)
        formData.append('qty', qty)
        formData.append('price', price)
        formData.append('category_id', category_id)
        formData.append('image', imageFile)
        try{
            const res = await axios.post('http://127.0.0.1:5000/post_product',formData,{
                headers: { 'Content-Type': 'multipart/form-data' }
            })
            await getProducts()
            return res.data.message
        }catch(err){
            return err.response.data.message
        }
    }

    async function getProducts(){
        try{
            const res = await axios.get('http://127.0.0.1:5000/get_products',{
                params: {
                    limit: limitRows.value,
                    page: page.value,
                }
            })
            if(res.data.totalPage > 0){
                if(res.data.totalPage < page.value){
                    page.value = res.data.totalPage
                }
                totalPage.value = res.data.totalPage
            }else{
                page.value =1
                totalPage.value=1
            }
            products.value = res.data.products
            return res.data.message
        }catch(err){
            console.log(err);
        }
    }

    let holdSearchText = ''
    async function searchProducts(text){
        text = text.toLowerCase()
        try{
            const res = await axios.get('http://127.0.0.1:5000/search_products',{
                params:{
                    limit: limitRows.value,
                    page: page.value,
                    searchName: text 
                }
            })
            console.log(res.data.totalPage);
            if(res.data.totalPage < page.value){
                if(res.data.totalPage > 0){
                    page.value = res.data.totalPage
                }else{
                    isSearchClicked.value = false
                    getProducts()
                }
            }else{
                totalPage.value = res.data.totalPage
            }
            products.value = res.data.products
            return res.data.message
        }catch(err){
            console.log(err);
        }
    }

    async function putProduct(id,name,qty,price,category_id,imageFile){
        name = name.toLowerCase()
        let formData = new FormData()
        formData.append('id', id)
        formData.append('name', name)
        formData.append('qty',qty)
        formData.append('price',price)
        formData.append('category_id',category_id)
        formData.append('image', imageFile)
        try{
            const res = await axios.put('127.0.0.1:5000/put_product',formData,{
                headers: { 'Content-Type': 'multipart/form-data' }
            })
            const product = products.value.find((p)=>p.id === id)
            product.name = res.data.product.name
            product.qty = res.data.product.qty
            product.price = res.data.product.price
            product.category_id = res.data.product.category_id
            product.image = res.data.product.image
            return res.data.message
        }catch(err){
            console.log(err);
        }
    }

    async function deleteProduct(id){
        try{
            const res = await axios.delete(`http://127.0.0.1:5000/delete_product/${id}`)
            products.value = products.value.filter((p)=> p.id !== id)
            console.log(page.value);
            return res.data.message
        }catch(err){ 
            console.log(err);
        }
    }
    

    return {  
        isAddClicked, postProduct, getProducts, page, limitRows, products, totalPage, searchProducts, holdSearchText, isSearchClicked, editProduct, putProduct, deleteProduct
    }
})