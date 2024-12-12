<script setup lang="ts">
import { ref, nextTick, computed } from 'vue'
import { ElMessage, ElScrollbar, ElMessageBox } from 'element-plus'

import { useUserStore } from '@/stores'
import request from '@/utils/request'
import router from '@/router'
import { formatDate, formatMessageDate } from '@/utils'
import { connSocket, disconnSocket, onEvtCb, emitEvt } from '@/utils/socket'

import UserInfo from './components/UserInfo.vue'
import RoomCreate from './components/RoomCreate.vue'

// socket
const userStore = useUserStore()
const token = userStore.token
const userId = JSON.parse(atob(token.split('.')[1])).sub

const scrollbarRef: any = ref<InstanceType<typeof ElScrollbar> | null>(null)
const userStatusColor = computed(() => {
  return function (status: string) {
    const map = {
      online: 'success',
      busy: 'danger',
      hide: 'primary'
    }
    return status in map ? map[status] : 'info'
  }
})

const userInfo: any = ref({})
const roomListInfo = ref([])
const userInfoMap = ref({})
const selectedRoom = ref(-1)

const loading = ref(true)
const memberVisible = ref(false)
const accountVisible = ref(false)
const userList: any = ref([])
const messageList: any = ref([
  { name: 'chow', time: '', message: 'hello' },
  { name: 'other', time: '', message: 'hello' }
])
const textareaInput = ref('')

const onEnter = (event: KeyboardEvent) => {
  event.preventDefault() // 阻止默认的回车行为（换行）
  sendMessage()
}

// SocketIO API

// 发送信息
const sendMessage = () => {
  if (textareaInput.value !== '') {
    emitEvt('msg', {
      userId: userId,
      roomId: selectedRoom.value,
      content: textareaInput.value,
    })

    textareaInput.value = ''
  } else {
    // 发送消息不能为空
  }
}

// 接收消息
const onMsgEvt = (data) => {
  if (data.type === 'msg') {
    messageList.value.push(data.data)
    autoScroll()
  } else if (data.type === 'userList') {
    userList.value = data.data
  } else if (data.type === 'kick') {
    ElMessage.error(data.message)
    userStore.token = ''
    router.push('/')
  }
}

const onCloseEvt = (data) => {
  ElMessage.error('与服务器断开连接！')
  router.replace('/')
}

// RESTful API

const getUserInfo = (userId: number) => {
  request
    .get(`/api/user/${userId}`)
    .then((res: any) => (userInfo.value = res.data))
    .catch((err: any) => console.log('ERROR', err))
}

const getUserRoomInfo = (userId: number) => {
  request
    .get(`/api/user/${userId}/room`)
    .then((res: any) => (roomListInfo.value = res.data))
    .catch((err: any) => console.log('ERROR', err))
}

const getRoomUserInfo = async (roomId: number) => {
  await request
    .get(`/api/room/${roomId}/user`)
    .then((res: any) => (userInfoMap.value = res.data))
    .catch((err: any) => console.log('ERROR', err))
}

const getHistoryChat = (roomId: number, nextId: number) => {
  request
    .get(`/api/room/${roomId}/chat`, {
      headers: {
        'Content-Type': 'application/json'
      },
      params: { nextId }
    })
    .then((res: any) => (messageList.value = res.data))
    .catch((err: any) => console.log('ERROR', err))
}

const selectRoom = async (roomId: number) => {
  getRoomUserInfo(roomId)
  let nextId = roomListInfo.value.filter((item: any) => item.roomId === roomId)[0].latestChatId
  if (nextId) getHistoryChat(roomId, nextId + 1)
  selectedRoom.value = roomId
}

// 初始化

if (!token) {
  ElMessage.error('请先登录！')
  router.replace('/')
}

const initChat = async () => {
  getUserInfo(userId)
  getUserRoomInfo(userId)

  loading.value = false

  connSocket()
  onEvtCb('msg', onMsgEvt)
  onEvtCb('disconnect', onCloseEvt)
  emitEvt('joinRoom', { token: userStore.token })
}

initChat()

// 自动滚动
const autoScroll = () => {
  nextTick(() => {
    if (scrollbarRef.value) {
      scrollbarRef.value.setScrollTop(scrollbarRef.value.wrapRef.scrollHeight)
    }
  })
}

const findRoom = () => {}

// 获取历史数据
const isLoading = ref(false)
const page = ref(1)
const fetchMessages = async () => {
  if (isLoading.value) return

  isLoading.value = true

  // 假设 `loadMoreMessages` 是一个方法从后端获取更多消息
  request
    .get('/api/user/message?page=' + page.value)
    .then(async (res: any) => {
      const newMessages = res.data

      const changeMessage = setTimeout(() => {
        messageList.value.unshift(...newMessages)

        isLoading.value = false
        page.value += 1

        // 插入新消息后的滚动高度
        nextTick(() => {
          // 调整滚动位置
          scrollbarRef.value.scrollTo({
            // top: (103 * newMessages.length + 8)
            top: remToPx(6.4375) * newMessages.length + remToPx(0.5)
          })
        })

        clearTimeout(changeMessage)
      }, 1000)
    })
    .catch((err) => {
      console.log(err)
    })
}
// 滚动条事件
const handleScroll = () => {
  if (scrollbarRef.value.wrapRef.scrollTop == 0) {
    fetchMessages()
  }
}
const remToPx = (rem: number) => {
  const rootFontSize = parseFloat(getComputedStyle(document.documentElement).fontSize)
  return rem * rootFontSize
}

// 退出登录
const logout = () => {
  ElMessageBox.confirm('是否退出登录？', '提示框', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'warning'
  })
    .then(() => {
      ElMessage({
        type: 'success',
        message: '你已退出登录'
      })
      userStore.logout()
      disconnSocket()
    })
    .catch(() => {
      // do nothing
    })
}

// 打开用户资料
const userInfoRef: any = ref(null)
const openUserInfo = () => {
  userInfoRef.value.open()
}

// open create room dialog
const roomCreateRef: any = ref(null)
const openCreateRoom = () => {
  roomCreateRef.value.open()
}
</script>
<template>
  <div id="chat" v-loading="loading" element-loading-background="rgba(122, 122, 122, 0.8)">
    <div class="chat-room">
      <!-- 用户信息列表 -->
      <div class="user-option-box">
        <div class="user-box">
          <el-badge class="user-status" is-dot :type="userStatusColor(userInfo?.status)">
            <el-avatar
              class="user-img"
              :src="`/images/userimg/${userInfo?.avatar}`"
              @click="openUserInfo"
            />
          </el-badge>
        </div>
        <el-icon class="option-icon active"><ChatLineSquare /></el-icon>
        <el-icon class="option-icon"><User /></el-icon>
        <el-icon class="option-icon setting"><Operation /></el-icon>
      </div>

      <div class="room-box">
        <div class="room-search-box">
          <el-input resize="none" type="textarea" class="search-input" />
          <el-popover trigger="click">
            <div>
              <el-button @click="openCreateRoom"
                ><el-icon><Message /></el-icon>create room</el-button
              >
            </div>
            <div>
              <el-button
                ><el-icon><User /></el-icon>add friend/room</el-button
              >
            </div>
            <template #reference>
              <el-button size="default" class="room-add-btn" @click="findRoom">
                <el-icon><Plus /></el-icon>
              </el-button>
            </template>
          </el-popover>
        </div>
        <div class="room-list-box">
          <el-scrollbar>
            <a
              :class="{ 'room-info-box': true, active: item.roomId === selectedRoom }"
              v-for="item in roomListInfo"
              :key="item"
              @click="selectRoom(item.roomId)"
            >
              <el-avatar class="user-img" src="/images/ACGN.png" />
              <div class="content">
                <div class="title">
                  <p class="name">{{ item.roomName }}</p>
                  <p class="time">{{ item.latestChatCreateTime }}</p>
                </div>
                <div class="message">
                  <p class="text">
                    <span>{{ item.latestChatUserName }}:{{ item.latestChatContent }}</span>
                    <el-badge
                      v-if="item.unreadMessages > 0"
                      :value="item.unreadMessages"
                      :max="99"
                    />
                  </p>
                </div>
              </div>
            </a>
          </el-scrollbar>
        </div>
      </div>

      <!-- 消息列表 -->
      <div class="room-preview">
        <div class="room-name">
          <p class="title">
            <span v-if="selectedRoom >= 0 && roomListInfo.length > 0">
              {{ roomListInfo.filter((item) => item.roomId === selectedRoom)[0].roomName }}
            </span>
          </p>
          <div class="chat-options">
            <span class="hidden"></span>
            <span class="max"></span>
            <span class="close" @click="logout"></span>
          </div>
        </div>
        <div class="chat-ui-empty" v-if="selectedRoom === -1">
          <el-empty description="机会常常只留给那些敢于开口的人" />
        </div>
        <div class="chat-ui" v-else>
          <div class="message-list">
            <div class="loading-text" v-if="isLoading">
              <el-icon class="is-loading"><Loading /></el-icon>加载中...
            </div>
            <el-scrollbar height="100%" ref="scrollbarRef" @scroll="handleScroll">
              <div
                v-for="item in messageList"
                :key="item.id"
                class="message-item"
                :class="{
                  other: item.userId === userId
                }"
              >
                <el-avatar
                  v-if="item.userId !== userId"
                  class="user-img"
                  src="https://empty"
                >
                  {{ userInfoMap[item.userId].nickname }}
                </el-avatar>
                <div class="message-content">
                  <div class="title">
                    <span class="name" v-if="item.userId !== userId">
                      {{ userInfoMap[item.userId] ? userInfoMap[item.userId].nickname : item.userId }}
                    </span>
                    <span class="time">{{ formatDate(item.time) }}</span>
                    <span class="name" v-if="item.userId === userId">
                      {{ userInfoMap[item.userId] ? userInfoMap[item.userId].nickname : item.userId }}
                    </span>
                  </div>
                  <div class="text">
                    <p>{{ item.content }}</p>
                  </div>
                </div>
                <el-avatar
                  v-if="item.userId === userId"
                  class="user-img-right"
                  src="https://empty"
                >
                  {{ userInfoMap[item.userId].nickname }}
                </el-avatar>
              </div>
            </el-scrollbar>
          </div>
          <div class="message-input-box">
            <div class="message-option">
              <el-tooltip class="box-item" effect="dark" content="表情" placement="top-start">
                <el-icon class="option-icon"><PictureRounded /></el-icon>
              </el-tooltip>
              <el-tooltip class="box-item" effect="dark" content="发送图片" placement="top-start">
                <el-icon class="option-icon"><Picture /></el-icon>
              </el-tooltip>
              <el-tooltip class="box-item" effect="dark" content="发送文件" placement="top-start">
                <el-icon class="option-icon"><Folder /></el-icon>
              </el-tooltip>
              <el-tooltip class="box-item" effect="dark" content="语音通话" placement="top-start">
                <el-icon class="option-icon"><Phone /></el-icon>
              </el-tooltip>
              <el-tooltip class="box-item" effect="dark" content="视频通话" placement="top-start">
                <el-icon class="option-icon"><Camera /></el-icon>
              </el-tooltip>
            </div>
            <el-input
              type="textarea"
              class="textarea"
              resize="none"
              v-model="textareaInput"
              @keydown.enter="onEnter"
            />
            <el-button type="primary" class="send-button" @click="sendMessage">发送</el-button>
          </div>

          <el-button class="member-visible-btn" @click="memberVisible = !memberVisible">
            {{ memberVisible ? '&gt;' : '&lt;' }}
          </el-button>
        </div>
        <!-- 账号列表 -->
        <div class="account-list-box" v-if="accountVisible">
          <!-- 窗口选项栏 -->
          <div class="member-title">
            <p class="title">在线人数：{{ userList.length }}</p>
          </div>
          <div class="member-list">
            <el-scrollbar height="100%">
              <div class="member-item" v-for="item in userList" :key="item">
                <el-avatar class="user-img" :src="`/images/userimg/${item.img}`" />
                <div class="name">{{ item.name }}</div>
              </div>
            </el-scrollbar>
          </div>
        </div>
      </div>
    </div>

    <!-- 用户信息表 -->
    <UserInfo ref="userInfoRef"></UserInfo>
    <RoomCreate ref="roomCreateRef"></RoomCreate>
  </div>
</template>
<style scoped lang="scss">
@use '@/assets/scss/chat/' as *;
</style>
