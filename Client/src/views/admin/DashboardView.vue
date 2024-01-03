<script setup>
import { onMounted, ref } from 'vue';


const loading = ref(true)

onMounted(()=>{
    loading.value = false
})
</script>

<template>
    <Transition name="slide-fade">
        <div v-if="!loading" class="text-black rounded-xl relative h-full grid place-items-center">
            <div>
                <p class="text-[200px]">Welcome</p>
                <p>Project Final Y4S3</p>
                <p>PYTHON FLASK With VUE3</p>
                <p></p>
                <p>Name: NAKAMURAKEI</p>
                <p>GROUP: SS3.4</p>
            </div>
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