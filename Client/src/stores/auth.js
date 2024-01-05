import { ref } from 'vue'
import { defineStore } from "pinia"

export const useAuthStore = defineStore('auth', () => {
  const isLoggedIn = ref(false)
  const isAdmin = ref(false)

  async function checkLogin(){
    try{
      const token = localStorage.getItem('token')
      const res = await fetch('http://localhost:5000/verify-login',{
        headers: {
          'x-access-token': token
        }
      })
      const data = await res.json()
      isLoggedIn.value = data.message !== 'true' ? false : true
    }catch(err){
      console.log(err);
    }
  }

  async function checkAdmin(){
    try{
      const token = localStorage.getItem('token')
      const res = await fetch('http://localhost:5000/verify-admin',{
        headers: {
          'x-access-token': token
        }
      })
      const data = await res.json()
      isAdmin.value = data.message !== 'true' ? false : true
      !isLoggedIn.value ? isAdmin.value = false : '' 
    }catch(err){
      console.log(err);
    }
  }

  return {
    isLoggedIn, isAdmin, checkLogin, checkAdmin
  }
})