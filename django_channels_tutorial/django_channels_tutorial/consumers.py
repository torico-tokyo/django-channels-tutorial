import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer


class TutorialConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        """
        クライアントが WebSocket に接続した時
        """
        print(f'[{self.channel_name}] connect')
        # クライアントを broadcast グループに追加
        await self.channel_layer.group_add(
            'broadcast',
            self.channel_name,
        )
        # connect の最後に accept() する。
        await self.accept()

    async def disconnect(self, _close_code):
        """
        切断時の処理
        """
        print(f'[{self.channel_name}] disconnect')
        await self.channel_layer.group_discard(
            'broadcast',
            self.channel_name,
        )
        await self.close()

    async def receive_json(self, data):
        """
        WebSocket からイベントを受信した時
        """
        print(f'[{self.channel_name}] receive_json: {data}')
        # 第二引数の type の . を _ に置換した、self のメソッドを、
        # 指定したグループの全てのクライアントに対して実行する。
        await self.channel_layer.group_send(
            'broadcast',
            {'type': 'broadcast.message', 'data': data}
        )

    async def broadcast_message(self, event):
        print(f'[{self.channel_name}] broadcast_message: {event}')
        data = event['data']
        await self.send(text_data=json.dumps(data))
