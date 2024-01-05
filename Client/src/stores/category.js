import { ref, computed } from "vue"
import { defineStore } from "pinia"
import axios from 'axios'

export const useCategoryStore = defineStore('category', () => {
    const categories = ref([])
    const isAddClicked = ref(false)
    const limitRows = ref('')
    const page = ref(1)
    const totalPage = ref(1)
    const editCategory = ref('')
    const haveSearchClicked = ref(false)

    function addButton() {
        isAddClicked.value = !isAddClicked.value
    }

    async function postCategory(name, imageFile) {
        name = name.toLowerCase()

        let formData = new FormData()
        formData.append('name', name)
        formData.append('image', imageFile)
        const res = await axios({
            method: 'POST',
            url: 'http://localhost:5000/post_category',
            data: formData,
            headers: { 'Content-Type': 'multipart/form-data' },
        }).then(async (res) => {
            // categories.value.push(res.data.category)
            await getCategories(limitRows.value)
            return res.data.message
        }).catch((err) => {
            return err.response.data.message
        })
        return res
    }

    async function getCategories(limit) {
        limitRows.value = limit
        if (limit === 'All') {
            try {
                const res = await axios.get('http://localhost:5000/get_categories')
                totalPage.value = 1
                page.value = 1
                categories.value = res.data.categories
                return res.data.message
            } catch (err) {
                console.log(err);
            }
        } else {
            try {
                const res = await axios.get(`http://localhost:5000/get_categories?limit=${limit}&page=${page.value}`)
                totalPage.value = res.data.totalPage === 0 ? 1 : res.data.totalPage
                categories.value = res.data.categories
                return res.data.message
            } catch (err) {
                console.log(err);
            }
        }
    }

    async function putCategory(id, name, imageFile) {
        name = name.toLowerCase()
        let formData = new FormData()
        formData.append('name', name)
        formData.append('image', imageFile)
        const res = await axios({
            method: 'PUT',
            url: `http://localhost:5000/put_category/${id}`,
            data: formData,
            headers: { 'Content-Type': 'multipart/form-data' },
        }).then((res) => {
            const category = categories.value.find((c)=>c.id === id)
            category.name = res.data.category.name
            category.image = res.data.category.image
            return res.data.message
        }).catch((err) => {
            return err
        })
        return res
    }

    async function deleteCategory(id) {
        const res = await axios({
            method: 'DELETE',
            url: `http://localhost:5000/delete_category/${id}`
        }).then(async (res) => {
            await getCategories(limitRows.value)
            return res.data.message
        }).catch((err) => {
            return err.response.data.message
        })
        return res
    }

    let holdSearchText=''
    async function searchCategories(search){
        try {
            const res = await axios.get('http://localhost:5000/search_categories', {
                params: { search, limit: limitRows.value, page: page.value },
                headers: { 'Content-Type': 'application/json' },
            })
            totalPage.value = res.data.totalPage === 0 ? 1 : res.data.totalPage
            categories.value = res.data.categories
        } catch (err) {
            console.log(err);
        }
    }


    return { categories, getCategories, postCategory, addButton, isAddClicked, page, totalPage, limitRows, editCategory, putCategory, deleteCategory, searchCategories, holdSearchText, haveSearchClicked }
})