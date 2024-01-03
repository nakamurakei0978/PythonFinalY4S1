<script setup>
import { onMounted, ref } from 'vue'
import { useCategoryStore } from '@/stores/category';
import SpinnerIcon from '@/components/admin/icons/Spinner.vue'
import { useProductStore } from '@/stores/product';
import Swal from 'sweetalert2'

const productStore = useProductStore()
const categoryStore = useCategoryStore()
const id = ref('')
const name = ref('')
const price = ref('')
const qty = ref('')
const category_id = ref('')
const imageName = ref('')
const imageSrc = ref('')
const imageFile = ref(null)

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

function handleImage(e) {
    imageFile.value = e.target.files[0]
    imageSrc.value = URL.createObjectURL(e.target.files[0]);
}

const isSubmitting = ref(false)
async function handleSubmit() {
    isSubmitting.value = true
    if (name.value) {
        const res = await productStore.putProduct(id.value, name.value, qty.value, price.value, category_id.value, imageFile.value)
        productStore.isEditClicked = false
        isSubmitting.value = false
        Toast.fire({
            icon: "success",
            title: "Updated"
        })
    } else {
        isSubmitting.value = false
        alert('something wrong!')
    }
}

onMounted(() => {
    id.value = productStore.editProduct.id
    name.value = productStore.editProduct.name
    qty.value = productStore.editProduct.qty
    price.value = productStore.editProduct.price
    category_id.value = productStore.editProduct.category_id
    imageName.value = productStore.editProduct.image
    imageSrc.value = 'http://192.168.100.11:5000/storage/products/' + imageName.value
})

</script>

<template>
    <div @click="$event.currentTarget === $event.target ? productStore.isEditClicked = false : ''"
        class="absolute grid place-items-center w-[calc(100%+40px)] h-[calc(100%+40px)] bg-black/50 backdrop-blur top-[-20px] left-[-20px] rounded-xl backdrop:rounded-xl">
        <form v-on:submit.prevent="handleSubmit"
            class="bg-gradient-to-tr from-gray-950 to-slate-800 grid grid-cols-1 rounded-xl p-10 text-white relative gap-3">
            <div class="absolute animate-pulse h-full w-full blur bg-gradient-to-r from-red-500 to-purple-500 -z-10">
            </div>
            <div class="flex flex-wrap gap-5 justify-center">
                <img v-if="imageName" :src="imageSrc" alt="" class="w-72 object-contain rounded-xl">
                <div>
                    <section class="grid grid-cols-1 gap-1">
                        <label for="name">Name</label>
                        <input v-model="name" placeholder="Enter product name" type="text"
                            class="rounded-xl bg-white focus:outline-none px-3 py-1 text-black" required>
                    </section>
                    <section class="grid grid-cols-1 gap-1">
                        <label for="name">Category</label>
                        <select v-model="category_id" class="rounded-xl px-3 py-1 bg-white text-black focus:outline-none"
                            required>
                            <option value="" disabled>Select category</option>
                            <option v-for="c in categoryStore.categories" :value="c.id">{{ c.name }}</option>
                        </select>
                    </section>
                    <section class="grid grid-cols-1 gap-1">
                        <label for="name">Qty</label>
                        <input v-model="qty" placeholder="Enter product qty" type="number"
                            class="rounded-xl focus:outline-none px-3 py-1 bg-white text-black" required>
                    </section>
                    <section class="grid grid-cols-1 gap-1">
                        <label for="name">Price</label>
                        <input v-model="price" placeholder="Enter product price" type="number" step="any"
                            class="rounded-xl focus:outline-none px-3 py-1 bg-white text-black" required>
                    </section>
                    <section class="grid grid-cols-1 gap-1">
                        <label for="image">Image</label>
                        <input @change="handleImage($event)" type="file" accept="image/*"
                            class="rounded-xl py-1 file:bg-slate-800 file:text-white file:border-none file:rounded-xl file:px-3 file:py-1 file:cursor-pointer file:duration-200 file:hover:bg-slate-700">
                    </section>
                    <button type="submit"
                        class="w-full bg-slate-800 rounded-xl p-3 hover:bg-slate-700 duration-200 relative">
                        <SpinnerIcon v-if="isSubmitting" class="w-[35px] h-[35px] absolute left-20 top-2 animate-spin" />
                        Submit
                    </button>
                </div>
            </div>
            <button @click="productStore.isEditClicked = false" type="button"
                class="w-[35px] h-[35px] absolute top-1 right-1 rounded-xl bg-red-500">X</button>
        </form>
    </div>
</template>