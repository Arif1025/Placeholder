import json
from channels.generic.websocket import AsyncWebsocketConsumer

class PollConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({'message':'Connect to Websocket'}))

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data=json.load(text_data)
        message=data['message']
        await self.send(text_data=json.dumps({'message':message}))