<script setup>
import { onMounted, ref } from 'vue'
import { useCategoryStore } from '@/stores/category';
import SpinnerIcon from '@/components/admin/icons/Spinner.vue'
import Swal from 'sweetalert2'

const categoryStore = useCategoryStore()
const id = ref('')
const name = ref('')
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
        const res = await categoryStore.putCategory(id.value, name.value, imageFile.value)
        console.log(res);
        isSubmitting.value = false
        categoryStore.isEditClicked = false
        Toast.fire({
            icon: "success",
            title: "Updated"
        })
    } else {
        isSubmitting.value = false
        alert('something wrong!')
    }
}

onMounted(()=>{
    id.value = categoryStore.editCategory.id
    name.value = categoryStore.editCategory.name
    imageName.value = categoryStore.editCategory.image
    imageSrc.value = 'http://localhost:5000/storage/categories/'+imageName.value
})

</script>

<template>
    <div @click="$event.currentTarget === $event.target ? categoryStore.isEditClicked = false : ''"
        class="absolute grid place-items-center w-[calc(100%+40px)] h-[calc(100%+40px)] bg-black/50 backdrop-blur top-[-20px] left-[-20px] rounded-xl backdrop:rounded-xl">
        <form v-on:submit.prevent="handleSubmit"
            class="bg-gradient-to-tr from-gray-950 to-slate-800 grid grid-cols-1 rounded-xl p-10 text-white relative gap-3">
            <div class="absolute animate-pulse h-full w-full blur bg-gradient-to-r from-red-500 to-purple-500 -z-10">
            </div>
            <div class="flex flex-wrap gap-5 justify-center">
                <img v-if="imageName" :src="imageSrc" alt="" class="w-52 object-cover rounded-xl">
                <div class="max-md-w-full grid grid-cols-1 gap-3">
                    <section class="grid grid-cols-1 gap-1">
                        <label for="name">Name</label>
                        <input v-model="name" type="text" class="bg-white rounded-xl focus:outline-none px-3 py-1 text-black" required>
                    </section>
                    <section class="grid grid-cols-1 gap-1">
                        <label for="image">Image</label>
                        <input @change="handleImage($event)" type="file" accept="image/*"
                            class="rounded-xl py-1 file:bg-slate-800 file:text-white file:border-none file:rounded-xl file:px-3 file:py-1 file:cursor-pointer file:duration-200 file:hover:bg-slate-700">
                    </section>
                    <button type="submit"  class="bg-slate-800 rounded-xl p-3 hover:bg-slate-700 duration-200 relative">
                        <SpinnerIcon v-if="isSubmitting" class="w-[35px] h-[35px] absolute left-20 top-2 animate-spin" />
                        Submit
                    </button>
                </div>
            </div>
            <button @click="categoryStore.isEditClicked = false" type="button"
                class="w-[35px] h-[35px] absolute top-1 right-1 rounded-xl bg-red-500">X</button>
        </form>
    </div>
</template>