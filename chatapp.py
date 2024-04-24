#!/usr/bin/env python3
import asyncio
import json
import logging

import redis.asyncio as redis
import typer
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing_extensions import Annotated

app = FastAPI()

global_room = "global_room"

logging.basicConfig(level=logging.INFO)


async def get_redis_client(host: str = "localhost"):
    return await redis.from_url(f"redis://{host}")


async def chat_reader(
    channel: redis.client.PubSub, websocket: WebSocket, nickname: str
):
    while True:
        message = await channel.get_message(ignore_subscribe_messages=True)
        if message is not None:
            message = message["data"].decode()
            data = json.loads(message)
            # Exclude messages sent by the same user
            if data["nickname"] != nickname:
                await websocket.send_text(message)


async def chat_publisher(
    client: redis.client.Redis, websocket: WebSocket, nickname: str
):
    while True:
        data = await websocket.receive_text()
        await client.publish(global_room, data)


@app.websocket("/chat/{nickname}")
async def main_chat_handler(websocket: WebSocket, nickname: str):
    logging.info(f"User {nickname} joined the chat")
    client = await get_redis_client(app.redis)

    try:
        await websocket.accept()

        async with client.pubsub() as pubsub:
            await pubsub.subscribe(global_room)

            reader_future = asyncio.create_task(
                chat_reader(pubsub, websocket, nickname)
            )
            publisher_future = asyncio.create_task(
                chat_publisher(client, websocket, nickname)
            )
            await publisher_future
            await reader_future
    except WebSocketDisconnect:
        logging.info(f"User {nickname} is disconnecting...")


def run_server(
    host: Annotated[str, typer.Option()] = "0.0.0.0",
    port: Annotated[int, typer.Option()] = 8000,
    redis: Annotated[str, typer.Option()] = "localhost",
):
    app.redis = redis
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    typer.run(run_server)
