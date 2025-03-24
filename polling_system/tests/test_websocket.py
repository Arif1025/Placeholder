import pytest
import json
from channels.testing import WebsocketCommunicator
from polling_system.asgi import application
from polling_system.consumers import PollConsumer

@pytest.mark.asyncio
async def test_websocket_poll():
    communicator = WebsocketCommunicator(application, 'ws/chat/')  # Create a WebSocket communicator
    connect,_ = await communicator.connect()  # Establish WebSocket connection
    assert connect

    message = {'type':'chat.message', 'message':'hello.world!'}  # Prepare a message to send
    await communicator.send_json_to(message)  # Send the message to WebSocket

    response = await communicator.receive_json_from()  # Receive the response from WebSocket
    assert response['message'] == 'hello world'  # Verify the message received is correct

    await communicator.disconnect()  # Close the WebSocket connection
