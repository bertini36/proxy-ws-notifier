# -*- coding: UTF-8 -*-

import asyncio
from functools import partial

from loguru import logger
from sanic import Blueprint
from sanic.response import text
from sanic.websocket import ConnectionClosed

from .rabbit_backend import RabbitBackend

bp = Blueprint('notifier')
connected = set()


@bp.websocket('/notifications/<user_id>/')
async def notifications(request, ws, user_id: str):

    async def send_websocket(ws, message):
        import json
        try:
            await ws.send(json.dumps(message))
        except ConnectionClosed:
            logger.info(f'User {user_id} disconnected')
            connected.remove(ws)

    logger.info(f'User {user_id} connected')
    connected.add(ws)
    loop = asyncio.get_event_loop()
    rabbit_reader = RabbitBackend(user_id, loop)
    send_ws_function = partial(send_websocket, ws)
    await rabbit_reader.read(send_ws_function)


@bp.route('/send/test/notification/<user_id>/')
async def send_test_notification(request, user_id: str):
    """
    Only for testing purposes
    """
    loop = asyncio.get_event_loop()
    rabbit_writer = RabbitBackend(user_id, loop)
    await rabbit_writer.write({'message': f'{user_id} notification'})
    return text('Test notification generated')
