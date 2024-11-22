<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import request from '@/utils/request'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores'
import { getSocket } from '@/utils/socket'

const userStore = useUserStore()
const router = useRouter()

const registerPanelVisable = ref(false)
const form = ref({
  username: '',
  password: ''
})

const validateForm = () => {
  if (form.value.username === '') {
    ElMessage({ message: '请输入用户名', type: 'error', grouping: true })
    return false
  }
  if (form.value.password === '') {
    ElMessage({ message: '请输入密码', type: 'error', grouping: true })
    return false
  }
  return true
}

const login = () => {
  if (!validateForm()) { return }
  request
    .post('/api/auth/login', {
      username: form.value.username,
      password: form.value.password
    })
    .then((res: any) => {
      if (res.code === 1) {
        ElMessage.success({ message: res.msg })
        userStore.setToken(res.data)

        let socket = getSocket()
        socket.emit('login', { token: userStore.token })

        router.replace('/chat')
      } else {
        ElMessage.error({ message: res.msg, grouping: true })
      }
    })
}

// 注册
const register = () => {
  if (!validateForm()) { return }
  request
    .post('/api/user', {
      username: form.value.username,
      password: form.value.password,
    })
    .then((res: any) => {
      if (res.code === 1) {
        ElMessage.success({ message: res.message })
        form.value.username = ''
        form.value.password = ''
        registerPanelVisable.value = false
      } else {
        ElMessage.error({
          message: res.message,
          grouping: true
        })
      }
    })
}

// 判断用户是否已登录过
if (userStore.token) {
  router.replace('/chat')
}
</script>
<template>
  <div id="login">
    <div class="form-box">
      <div class="background">
        <div class="login-text">
          <h1 class="title">登陆</h1>
          <p class="sub-title">子标题</p>
          <!-- <img src="/images/register.jpg" alt="register.jpg" /> -->
          <p class="text">已有账号？</p>
          <button class="change-login" @click="registerPanelVisable = false">登录</button>
        </div>
        <div class="register-text">
          <h1 class="title">注册</h1>
          <p class="sub-title">子标题</p>
          <!-- <img src="/images/login.jpg" alt="register.jpg" /> -->
          <p class="text">没有账号？</p>
          <el-button class="change-register" @click="registerPanelVisable = true">注册</el-button>
        </div>
      </div>

      <div class="form-block" :class="{ 'change-register-form': registerPanelVisable }">
        <div class="login-box">
          <h1 class="login-title">LOGIN</h1>
          <el-form class="login-form">
            <input
              type="text"
              name="login-username"
              class="login-username"
              id="login-username"
              v-model="form.username"
              placeholder="用户名"
              autocomplete="off"
            />
            <input
              type="password"
              name="login-password"
              class="login-password"
              id="login-password"
              v-model="form.password"
              placeholder="密码"
              autocomplete="off"
            />
            <el-button class="login-button" id="login-button" @click="login()"> 登录 </el-button>
            <router-link to="/forget" class="forget">忘记密码？</router-link>
          </el-form>
        </div>

        <div class="register-box">
          <h1 class="register-title">REGISTER</h1>
          <form class="register-form">
            <input
              type="text"
              name="register-username"
              class="register-username"
              id="register-username"
              v-model="form.username"
              placeholder="请输入用户名"
              autocomplete="off"
            />
            <input
              type="password"
              name="register-password"
              class="register-password"
              id="register-password"
              v-model="form.password"
              placeholder="请输入密码"
              autocomplete="off"
            />
            <el-button class="register-button" id="register-button" @click="register"> 注册 </el-button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped lang="scss">
@use '@/assets/scss/login/' as *;
</style>
