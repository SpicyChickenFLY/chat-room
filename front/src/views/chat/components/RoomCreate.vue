<script setup lang="ts">
import request from '@/utils/request'
import { useUserStore } from '@/stores'
import router from '@/router'
import { ElMessage } from 'element-plus'
import { ref } from 'vue'

const userStore = useUserStore()

// 模态框
const dialogFormVisible = ref(false)

// 用户信息表单
const userInfoForm = ref({
  username: ''
})

// 标签长度
const labelWidth = ref(100)

// 打开模态框
const open = () => {
  dialogFormVisible.value = true

  const token = userStore.token
  const userId = JSON.parse(atob(token.split('.')[1])).sub
  if (!token) {
    ElMessage.error('请先登录！')
    router.replace('/')
    return
  }
}

// 更改信息
const changeInfo = () => {
  request.post('/api/user/updateInfo', { userInfoForm: userInfoForm.value }).then((res: any) => {
    if (res.code === 1) {
      ElMessage({
        message: '修改成功',
        type: 'success'
      })
      window.location.replace('/chat')
    }
  })
}

// 导出方法
defineExpose({
  open
})
</script>
<template>
  <el-dialog v-model="dialogFormVisible" :show-close="false" width="600" align-center>
    <div class="container">
      <div class="user-choice">
        <el-input
          v-model="filterText"
          style="width: 240px"
          placeholder="Search user"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <div>choose friend to create</div>
        <el-tree
          ref="treeRef"
          style="max-width: 600px"
          class="filter-tree"
          :data="data"
          :props="defaultProps"
          default-expand-all
          :filter-node-method="filterNode"
        />
      </div>
      <div class="user-chosen">
        <div>create room</div>
        <el-scrollbar>
        </el-scrollbar>
      </div>
    </div>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取消</el-button>
        <el-button type="primary" @click="changeInfo">确认</el-button>
      </div>
    </template>
  </el-dialog>
</template>
<style lang="scss">
.container {
  display: flex;
  height: 500px;

  .user-choice {

  }

  .user-chosen {

  }
}
</style>
