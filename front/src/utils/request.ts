import axios from 'axios'
import router from '@/router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores'

const userStore = useUserStore()

const baseURL = 'http://127.0.0.1:5000'
const request = axios.create({
  baseURL: baseURL,
  timeout: 10000,
})

request.interceptors.request.use(
  (config) => {
    config.headers['Content-Type'] = "application/json"
    // 注入token
    if (userStore.token) {
      config.headers.Authorization = `Bearer ${userStore.token}`
    }
    return config
  },
  (error) => {
    // 失败执行promise
    return Promise.reject(error)
  }
)
// 响应拦截器
request.interceptors.response.use(
  (response) => {
    // 判断返回的数据
    const { code, status } = response.data
    if (response.status === 401) {
      ElMessage({ type: 'warning', message: 'token超时了' })
      // 说明token超时了
      //   await store.dispatch('user/logout') // 调用action 退出登录
      //  主动跳到登录页
      router.push('/login') // 跳转到登录页
    } else if (response.status === 500) {
      ElMessage({ type: 'error', message: response.data.message })
      return Promise.reject(response)
    } else {
        return response.data
    }
  },
  async (error) => {
    // error.message
    if (error.response && error.response.data) {
      ElMessage.error(error.response.data.msg)
    } else{
      ElMessage.error(error.message)
    }
    return Promise.reject(error)
  }
)

export default request
