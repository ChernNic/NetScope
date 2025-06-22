import asyncio, telnetlib3
from channels.generic.websocket import AsyncWebsocketConsumer

class TelnetConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        from inventory.models import Device  

        device_id = self.scope["url_route"]["kwargs"]["device_id"]
        self.device = await asyncio.to_thread(Device.objects.select_related("access").get, id=device_id)
        self.access = self.device.access

        try:
            self.reader, self.writer = await telnetlib3.open_connection(
                host=self.access.ip,
                port=self.access.port or 23,
                shell=None,
                encoding='utf8'
            )
            await self.accept()
            asyncio.create_task(self._forward_output())

        except Exception as e:
            await self.accept()
            await self.send(f"\x1b[1;3;31m[Ошибка подключения: {str(e)}]\x1b[0m\r\n")
            await asyncio.sleep(2)  
            await self.close()

    async def _forward_output(self):
        try:
            while True:
                data = await self.reader.read(1024)
                if data:
                    await self.send(data)
                await asyncio.sleep(0.01)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            await self.send(f"\x1b[31m[Ошибка: {e}]\x1b[0m")

    async def receive(self, text_data):
        if self.writer:
            self.writer.write(text_data)
            try:
                await self.writer.drain()
            except Exception as e:
                await self.send(f"\x1b[31m[Ошибка записи: {e}]\x1b[0m")

    async def disconnect(self, _):
        if self.writer:
            self.writer.close()
