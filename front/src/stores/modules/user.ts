import { defineStore } from 'pinia'
import { reactive, ref } from 'vue'

export const useUserStore = defineStore(
  'user',
  () => {
    // 用户token
    const token = ref('')

    // 设置用户信息
    const setToken = (data: any) => {
      token.value = data.accessToken
    }

    // 退出登录
    const logout = () => {
      token.value = ''
      window.location.replace('/')
    }

    return {
      token,
      setToken,
      logout
    }
  },
  {
    persist: true
  }
)
