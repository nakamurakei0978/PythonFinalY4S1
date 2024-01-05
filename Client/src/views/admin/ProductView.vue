<script setup>
import { onMounted, onUnmounted, ref } from 'vue';
import HeaderBar from '@/components/admin/product/HeaderBar.vue'
import AddProductForm from '@/components/admin/product/AddProductForm.vue'
import EditProductForm from '@/components/admin/product/EditProductForm.vue'
import EditIcon from '@/components/admin/icons/Edit.vue'
import { useProductStore } from '@/stores/product'
import { useCategoryStore } from '@/stores/category'
import Swal from 'sweetalert2'

const productStore = useProductStore()
const categoryStore = useCategoryStore()
const loading = ref(true)


onMounted(async () => {
  const category_res = await categoryStore.getCategories('All')
  const product_res = await productStore.getProducts()
  console.log(product_res);
  loading.value = false
})

function formatToDollar(price) {
  let USDollar = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  })
  return USDollar.format(price)
}

function getCategoryName(id) {
  if (!id) return 'N/A'
  const categories = categoryStore.categories
  const category = categories.find((c) => c.id === id)
  return category.name
}

function handleEdit(product) {
  productStore.editProduct = product
  productStore.isEditClicked = true
}

const isImageClicked = ref(false)
const imageSrc = ref('')
function handleImageClick(src) {
  isImageClicked.value = true
  imageSrc.value = src
}


async function handleDelete(id) {
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
      await productStore.deleteProduct(id)
      Swal.fire({
        title: "Deleted!",
        text: "Your file has been deleted.",
        icon: "success"
      });
    }
  })
}

onUnmounted(() => {
  productStore.isAddClicked = false
})
</script>

<template>
  <Transition name="slide-fade">
    <div v-if="!loading" class="text-black rounded-xl relative h-full">
      <HeaderBar title="Product" />

      <div class="bg-slate-950 grid grid-rows-[40px_1fr] divide-y-2 p-1 rounded-xl mt-3">
        <div class="grid grid-cols-7 bg-white text-xl font-bold rounded-se-xl rounded-ss-xl items-center px-1">
          <div>#</div>
          <div>Name</div>
          <div>Qty</div>
          <div>Price</div>
          <div>Category</div>
          <div>Image</div>
          <div>Action</div>
        </div>
        <div
          class="divide-y-2 bg-white overflow-auto h-[calc(100dvh-160px)] max-sm:h-[calc(100dvh-207px)] p-1 rounded-es-xl rounded-ee-xl">
          <div v-for="p in productStore.products" class="grid grid-cols-7 h-12 items-center">
            <div class="overflow-ellipsis overflow-clip">{{ p.id }}</div>
            <div class="overflow-ellipsis overflow-clip">{{ p.name }}</div>
            <div>{{ p.qty > 0 ? p.qty : 'No stock!' }}</div>
            <div>{{ formatToDollar(p.price) }}</div>
            <div>{{ getCategoryName(p.category_id) }}</div>
            <div>
              <img @click="handleImageClick('http://localhost:5000/storage/products/' + p.image)" v-if="p.image"
                :src="'http://localhost:5000/storage/products/' + p.image" alt=""
                class="w-10 object-cover h-10 rounded-xl cursor-zoom-in">
              <span v-else>N/A</span>
            </div>
            <div class="flex gap-3">
              <button @click="handleEdit(p)"
                class="bg-slate-950 hover:bg-slate-700 duration-200 p-2 rounded-xl text-white">
                <EditIcon class="h-5" />
              </button>
              <button @click="handleDelete(p.id)"
                class="bg-red-500 w-10 h-10 hover:bg-red-600 duration-200 rounded-xl text-white">X</button>
            </div>
          </div>
        </div>
      </div>

      <Transition name="show">
        <AddProductForm v-if="productStore.isAddClicked" />
      </Transition>
      <Transition name="show">
        <EditProductForm v-if="productStore.isEditClicked" />
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