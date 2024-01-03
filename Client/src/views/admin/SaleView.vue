<script setup>
import { onMounted, onUnmounted, ref } from 'vue';
import HeaderBar from '@/components/admin/sale/HeaderBar.vue'
import ViewIcon from '@/components/admin/icons/View.vue'
import Swal from 'sweetalert2'
import { useSaleStore } from '@/stores/sale.js'
import ViewDetails from '@/components/admin/sale/ViewDetails.vue'


const saleStore = useSaleStore()
const loading = ref(true)

onMounted(async () => {
  await saleStore.getSaleLists(20)
  loading.value = false
})

function formatToDollar(price) {
  let USDollar = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  })
  return USDollar.format(price)
}

const sale = ref('')
function handleView(s) {
  sale.value = s
  saleStore.isViewClicked = true
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
      await saleStore.deleteList(id)
      Swal.fire({
        title: "Deleted!",
        text: "Your file has been deleted.",
        icon: "success"
      });
    }
  })
}

</script>

<template>
  <Transition name="slide-fade">
    <div v-if="!loading" class="text-black rounded-xl relative h-full">
      <HeaderBar title="Sale" />

      <div class="bg-slate-950 grid grid-rows-[40px_1fr] divide-y-2 p-1 rounded-xl mt-3">
        <div class="grid grid-cols-5 bg-white text-xl font-bold rounded-se-xl rounded-ss-xl items-center px-1">
          <div>#</div>
          <div>User</div>
          <div>Date</div>
          <div>Total amount</div>
          <div>Action</div>
        </div>
        <div
          class="divide-y-2 bg-white overflow-auto h-[calc(100dvh-160px)] max-sm:h-[calc(100dvh-207px)] p-1 rounded-es-xl rounded-ee-xl">
          <div v-for="s in saleStore.sale_lists" class="grid grid-cols-5 h-12 items-center">
            <div class="overflow-ellipsis overflow-clip">{{ s.id }}</div>
            <div class="overflow-ellipsis overflow-clip">{{ s.user }}</div>
            <div>{{ s.date }}</div>
            <div>{{ formatToDollar(s.total) }}</div>
            <div class="flex gap-3">
              <button @click="handleView(s)"
                class="bg-slate-950 hover:bg-slate-700 duration-200 p-2 rounded-xl text-white">
                <ViewIcon class="h-5" />
              </button>
            </div>
          </div>
        </div>
      </div>
      <Transition name="show">
        <ViewDetails v-if="saleStore.isViewClicked" :sale="sale" />
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