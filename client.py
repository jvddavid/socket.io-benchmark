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
        self.sio.on('message', self.on_message)
        self.sio.on('my message', self.on_my_message)

    async def connect(self, url):
        await self.sio.connect(url, transports=['websocket'])

    async def on_connect(self):
        print('Connected to server')
        print('my sid is', self.sio.sid)
        print('my transport is', self.sio.transport)

    async def on_disconnect(self):
        print('Disconnected from server')

    count = 0
    async def on_message(self, data):
        self.count += 1

    async def on_my_message(self, data):
        print('Received my message:', data)

    def print(self):
        print(f"Client {self.sio.sid} at {datetime.now()} received {self.count} messages")
        self.count = 0

    async def close(self):
        await self.sio.disconnect()

clients: list[Client] = []
async def main():
    parser = argparse.ArgumentParser(description="Load tester for socket.io applications")
    parser.add_argument('-s', '--host', action='store', default='localhost')
    parser.add_argument('-p', '--port', action='store', default=3000)
    parser.add_argument('-c', '--concurrency', type=int, default=1)
    
    args = parser.parse_args(sys.argv[1:])

    url = f'http://{args.host}:{args.port}'

    for i in range(args.concurrency):
        client = Client()
        clients.append(client)
        asyncio.create_task(client.connect(url))

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

