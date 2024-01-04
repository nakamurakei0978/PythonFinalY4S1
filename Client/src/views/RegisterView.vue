<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import Swal from 'sweetalert2'

const router = useRouter()
const loading = ref(true)
const isSubmiting = ref(false)
const username = ref('')
const password = ref('')
const confirm_password = ref('')

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

onMounted(() => {
    loading.value = false
})


async function handleSubmit() {
    if (password.value === confirm_password.value) {
        try {
            isSubmiting.value = true
            await fetch('http://127.0.0.1:5000/register', {
                body: JSON.stringify({
                    'username': username.value,
                    'password': password.value
                }),
                method: 'POST',
                headers: {
                    'content-type': 'application/json'
                }
            })
            isSubmiting.value = false
            router.push({ name: 'login' })
            Toast.fire({
                icon: "success",
                title: "An account has been created",
                showCloseButton: 'true'
            })
        } catch (err) {
            console.log(err)
        }
    }
}
</script>

<template>
    <Transition name="fade">
        <div v-if="loading" class="grid place-items-center h-[100dvh] fixed top-0 left-0 w-screen">
            <span class="loading loading-infinity loading-lg scale-150"></span>
        </div>
    </Transition>
    <Transition name="fade">
        <div v-if="!loading" class="h-[calc(100dvh-80px)] grid place-items-center">
            <form v-on:submit.prevent="handleSubmit" class="grid grid-cols-1 gap-2">
                <label for="username">Username</label>
                <input v-model="username" type="text" required placeholder="Type here"
                    class="input input-bordered w-full max-w-xs" />
                <label for="password">Password</label>
                <input v-model="password" type="text" required placeholder="Type here"
                    class="input input-bordered w-full max-w-xs" />
                <label for="confirm_password">Confirm Password</label>
                <input v-model="confirm_password" type="text" required placeholder="Type here"
                    class="input input-bordered w-full max-w-xs" />
                <button type="submit" class="btn">
                    <span v-if="isSubmiting" class="loading loading-spinner loading-md mr-3"></span>
                    Submit
                </button>
            </form>
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