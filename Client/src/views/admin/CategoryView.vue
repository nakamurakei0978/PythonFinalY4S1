<script setup>
import { onMounted, onUnmounted, ref } from 'vue';
import HeaderBar from '@/components/admin/category/HeaderBar.vue'
import AddCategoryForm from '@/components/admin/category/AddCategoryForm.vue'
import EditIcon from '@/components/admin/icons/Edit.vue'
import { useCategoryStore } from '@/stores/category'
import EditCategoryForm from '@/components/admin/category/EditCategoryForm.vue';
import Swal from 'sweetalert2'


const categoryStore = useCategoryStore()
const loading = ref(true)

onMounted(async () => {
  loading.value = true
  const res = await categoryStore.getCategories(20)
  console.log(res);
  loading.value = false
})



const isImageClicked = ref(false)
const imageSrc = ref('')
function handleZoomImage(src) {
  imageSrc.value = src
  isImageClicked.value = true
}

function handleEdit(category) {
  categoryStore.editCategory = category
  categoryStore.isEditClicked = true
}

function handleDelete(id) {
  Swal.fire({
    title: "Are you sure?",
    text: "You won't be able to revert this!",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    confirmButtonText: "Yes, delete it!"
  }).then(async (result) => {
    if (result.isConfirmed) {
      await categoryStore.deleteCategory(id)
      Swal.fire({
        title: "Deleted!",
        text: "Your file has been deleted.",
        icon: "success"
      });
    }
  })
}

onUnmounted(() => {
  categoryStore.isAddClicked = false
})
</script>

<template>
  <Transition name="slide-fade">
    <div v-if="!loading" class="text-black rounded-xl relative h-full">
      <HeaderBar title="Category" :search='true' :add='true' />

      <div class="bg-slate-950 grid grid-rows-[40px_1fr] divide-y-2 p-1 rounded-xl mt-3">
        <div class="grid grid-cols-4 bg-white text-xl font-bold rounded-se-xl rounded-ss-xl items-center px-1">
          <div>#</div>
          <div>Name</div>
          <div>Image</div>
          <div>Action</div>
        </div>
        <div
          class="divide-y-2 bg-white overflow-auto h-[calc(100dvh-160px)] max-sm:h-[calc(100dvh-207px)] p-1 rounded-es-xl rounded-ee-xl">
          <div class="grid grid-cols-4 h-12 items-center" v-for="c in categoryStore.categories">
            <div class="overflow-ellipsis overflow-clip">{{ c.id }}</div>
            <div class="overflow-ellipsis overflow-clip">{{ c.name }}</div>
            <div>
              <img @click="handleZoomImage('http://192.168.100.11:5000/storage/categories/' + c.image)" v-if="c.image"
                :src="'http://192.168.100.11:5000/storage/categories/' + c.image" alt=""
                class="w-10 object-cover h-10 rounded-xl cursor-zoom-in">
              <span v-else>N/A</span>
            </div>
            <div class="flex gap-3">
              <button @click="handleEdit(c)"
                class="bg-slate-950 hover:bg-slate-700 duration-200 p-2 rounded-xl text-white">
                <EditIcon class="h-5" />
              </button>
              <button @click="handleDelete(c.id)"
                class="bg-red-500 w-10 h-10 hover:bg-red-600 duration-200 rounded-xl text-white">X</button>
            </div>
          </div>
        </div>
      </div>

      <Transition name="show">
        <AddCategoryForm v-if="categoryStore.isAddClicked" />
      </Transition>
      <Transition name="show">
        <EditCategoryForm v-if="categoryStore.isEditClicked" />
      </Transition>
      <Transition name="show">
        <div v-if="isImageClicked" @click="$event.currentTarget === $event.target ? isImageClicked = false : ''"
          class="absolute grid place-items-center w-[calc(100%+40px)] h-[calc(100%+40px)] bg-black/50 backdrop-blur top-[-20px] left-[-20px] rounded-xl backdrop:rounded-xl">
          <img :src="imageSrc" alt="" class="object-contain w-fit max-h-full min-h-1">
          <button @click="isImageClicked = false"
            class="absolute w-[100px] h-[50px] text-white bg-red-500 hover:bg-red-700 duration-200 rounded-xl text-xl bottom-1">X</button>
        </div>
      </Transition>
    </div>
  </Transition>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  /* use the transition utility classes from Tailwind CSS */
  @apply transition-opacity duration-500 ease-in-out;
}

.fade-enter-from,
.fade-leave-to {
  /* use the opacity utility class from Tailwind CSS */
  @apply opacity-0;
}

.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.8s cubic-bezier(1, 0.5, 0.8, 1);
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateX(20px);
  opacity: 0;
}

.show-enter-active {
  animation: show-out 0.2s;
}

.show-leave-active {
  animation: show-out 0.2s reverse;
}

@keyframes show-out {
  0% {
    transform: scale(0);
  }

  100% {
    transform: scale(1);
  }
}

::-webkit-scrollbar {
  width: 10px;
}

::-webkit-scrollbar-track {
  margin-bottom: 10px;
}

::-webkit-scrollbar-thumb {
  background-color: black;
  border-radius: 5px;
}
</style>