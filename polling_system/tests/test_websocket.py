import pytest
import json
from channels.testing import WebsocketCommunicator
from polling_system.asgi import application
from polling_system.consumers import PollConsumer

@pytest.mark.asyncio
async def test_websocket_poll():
    communicator = WebsocketCommunicator(application, 'ws/chat/')
    connect,_ = await communicator.connect()
    assert connect

    message = {'type':'chat.message', 'message':'hello.world!'}
    await communicator.send_json_to(message)

    response = await communicator.receive_json_from()
    assert response['message'] == 'hello world'

    await  communicator.disconnect()