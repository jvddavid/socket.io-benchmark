import asyncio
import socketio
from datetime import datetime
import argparse
import sys

class Client:
    def __init__(self):
        self.sio = socketio.AsyncClient()
        self.sio.on('connect', self.on_connect)
        self.sio.on('disconnect', self.on_disconnect)
        self.sio.on('time', self.on_message)
        self.sio.on('candle', self.on_message)

    async def connect(self, url, transport='websocket'):
        await self.sio.connect(url, headers={
            'Origin': 'http://localhost:3000'
        }, transports=[transport], retry=True)

    async def on_connect(self):
        print('Connected to server')
        print('my sid is', self.sio.sid)
        print('my transport is', self.sio.transport)
        await self.sio.emit('subscribe', {
            'id': 1857,
            'size': 60,
        })
        await self.sio.emit('subscribe', {
            'id': 1857,
            'size': 60,
        })

    async def on_disconnect(self, reason):
        print('Disconnected from server', reason)

    count = 0
    async def on_message(self, data, *args):
        self.count += 1

    async def on_subscribe(self, data):
        print('Subscribed:', data)

    async def on_my_message(self, data):
        print('Received my message:', data)

    def print(self):
        print(f"Client {self.sio.sid} at {datetime.now()} received {self.count} messages with status {self.sio.eio.state}")
        self.count = 0

    async def close(self):
        await self.sio.disconnect()

clients: list[Client] = []
async def main():
    parser = argparse.ArgumentParser(description="Load tester for socket.io applications")
    parser.add_argument('-u', '--url', action='store')
    parser.add_argument('-t', '--transport', action='store', default='websocket')
    parser.add_argument('-c', '--concurrency', type=int, default=1)
    
    args = parser.parse_args(sys.argv[1:])
    url = args.url
    if not url:
        print("Please provide a URL")
        sys.exit(1)
    transport = args.transport

    for i in range(args.concurrency):
        client = Client()
        clients.append(client)
        asyncio.create_task(client.connect(url, transport))

    while True:
        for client in clients:
            client.print()
        print("Connected clients:", len(clients))
        print("Press Ctrl+C to stop")
        await asyncio.sleep(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        for client in clients:
            asyncio.run(client.close())
        print('Interrupted')
        sys.exit(0)

