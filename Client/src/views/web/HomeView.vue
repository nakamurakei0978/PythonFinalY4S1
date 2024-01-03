<script setup>
import { onMounted, ref } from 'vue'

const loading = ref(true)

onMounted(()=>{
    loading.value=false
})
</script>

<template>
     <Transition name="fade">
        <div v-if="loading" class="grid place-items-center h-[100dvh] fixed top-0 left-0 w-screen">
            <span class="loading loading-infinity loading-lg scale-150"></span>
        </div>
    </Transition>
    <Transition name="fade">
        <div v-if="!loading" class="fixed top-0 h-screen bg-slate-950 grid place-items-center w-screen">
            <div>
                <p class="text-[300px]">Welcome</p>
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
</style>