# -*- coding: UTF-8 -*-

import asyncio
import json

from aio_pika import connect_robust, ExchangeType, Message
from loguru import logger

from .settings import TASK_HOST


class RabbitBackend:

    def __init__(self, routing_key: str, loop):
        self.routing_key = routing_key
        self.loop = loop

        self.connection = None
        self.channel = None
        self.exchange = None
        self.queue = None

    async def set_up(self):
        self.connection = await connect_robust(
            host=TASK_HOST,
            loop=self.loop
        )
        self.channel = await self.connection.channel()
        self.exchange = await self.channel.declare_exchange(
            self.routing_key,
            type=ExchangeType.DIRECT,
            auto_delete=False,
            durable=True
        )
        self.queue = await self.channel.declare_queue(
            self.routing_key,
            auto_delete=False,
            durable=True
        )
        await self.queue.bind(
            exchange=self.routing_key,
            routing_key=self.routing_key
        )

    async def disconnect(self):
        await self.queue.unbind(self.exchange, self.routing_key)
        await self.queue.delete()
        await self.connection.close()


class RabbitReader(RabbitBackend):

    async def read_queue(self, async_callback):
        async with self.queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    await self.process_message(message, async_callback)

    @staticmethod
    async def process_message(message: Message, async_callback):
        data = json.loads(message.body)
        await async_callback(data)

    async def read(self, async_callback):
        try:
            tasks = [
                self.read_queue(async_callback)
            ]
            await asyncio.gather(*tasks)
        except Exception as e:
            logger.error(f'ERROR {e}')
            await self.disconnect()


class RabbitWriter(RabbitBackend):

    async def write(self, message: dict):
        try:
            await self.exchange.publish(
                Message(
                    body=json.dumps(message).encode()
                ),
                routing_key=self.routing_key
            )
        except Exception as e:
            logger.error(f'ERROR {e}')
            await self.disconnect()


