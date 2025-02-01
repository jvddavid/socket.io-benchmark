import closeWithGrace from 'close-with-grace'
import { Server } from 'socket.io'
import { config } from './constants/config'

async function main() {
  const io = new Server({
    cors: {
      origin: '*',
    },
    transports: ['websocket', 'polling'],
  })

  let count = 0
  io.on('connection', async (socket) => {
    const room = `room-${Math.floor(count % config.messages.roomsLength)}`
    count++
    config.messages.roomsCount[room]++
    await socket.join(room)

    socket.on('disconnect', async () => {
      config.messages.roomsCount[room]--
      count--
    })
  })

  const interval = setInterval(
    () => {
      const message = config.messages.message()
      for (const room of config.messages.rooms) {
        io.to(room).emit('message', message)
      }
    },
    1000 / config.messages.messagesPerSecond,
  )

  const logInterval = setInterval(
    () => {
      console.log(`Connected clients: ${count}`)
    },
    1000,
  )

  io.listen(config.port)
  console.log(`Listening on port ${config.port}`)

  closeWithGrace(async () => {
    clearInterval(interval)
    clearInterval(logInterval)
    await io.close()
  })
}

main().catch(console.error)
