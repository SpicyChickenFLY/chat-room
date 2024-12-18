import { io } from 'socket.io-client'

let socket: any = null

const baseURL = 'http://127.0.0.1:5000'

export function connSocket() {
  if (!socket) {
    console.log('Socket 创建')
    socket = io(baseURL)
  }
}

// 关闭连接
export function disconnSocket() {
  if (socket) {
    console.log('Socket 关闭')
    socket.disconnect()
    socket = null
  }
}

export function onEvtCb(event: string, callback: any) {
  socket.off(event)
  socket.on(event, callback)
}

export function emitEvt(event: string, arg: any, errCb: any) {
  socket.timeout(2000).emit(event, arg, errCb)
}
