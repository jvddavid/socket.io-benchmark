const port = Number.parseInt(process.env.PORT ?? '3000')

if (Number.isNaN(port) || !Number.isSafeInteger(port) || port < 1 || port > 65535) {
  throw new Error('Invalid PORT')
}

const rooms = Array.from({ length: 1000 }, (_, i) => `room-${i}`)

export const config = {
  port,
  host: process.env.HOST ?? 'localhost',
  messages: {
    roomsLength: rooms.length,
    rooms,
    roomsCount: rooms.reduce<Record<string, number>>((acc, room) => {
      acc[room] = 0
      return acc
    }, {}),
    roomsPerClient: 1,
    messageLength: 256,
    messagesPerSecond: 8,
    message(): string {
      return `[${Date.now()}, ${Array.from({ length: this.messageLength }, () => Math.floor(Math.random() * 10).toString()).join(',')}]`
    },
  },
}
