#!/usr/bin/env python3
import asyncio
import json
import logging

import redis.asyncio as redis
import typer
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from redis.asyncio.client import PubSub
from typing_extensions import Annotated

app: FastAPI = FastAPI()

global_room = "global_room"

logging.basicConfig(level=logging.INFO)


async def get_redis_client(host: str = "localhost") -> redis.Redis:
    return await redis.from_url(url=f"redis://{host}")


async def chat_reader(
    channel: PubSub, websocket: WebSocket, nickname: str
) -> None:
    while True:
        message: dict = await channel.get_message(
            ignore_subscribe_messages=True
        )
        if message is not None:
            decoded_message: str = message["data"].decode()
            data = json.loads(s=decoded_message)
            # Exclude messages sent by the same user
            if data["nickname"] != nickname:
                await websocket.send_text(data=decoded_message)


async def chat_publisher(client: redis.Redis, websocket: WebSocket) -> None:
    while True:
        data: str = await websocket.receive_text()
        await client.publish(channel=global_room, message=data)


@app.websocket(path="/chat/{nickname}")
async def main_chat_handler(websocket: WebSocket, nickname: str) -> None:
    logging.info(msg=f"User {nickname} joined the chat")
    client: redis.Redis = await get_redis_client(host=app.redis)

    try:
        await websocket.accept()

        async with client.pubsub() as pubsub:
            await pubsub.subscribe(global_room)

            reader_future: asyncio.Task[None] = asyncio.create_task(
                coro=chat_reader(pubsub, websocket, nickname)
            )
            publisher_future: asyncio.Task[None] = asyncio.create_task(
                coro=chat_publisher(client, websocket)
            )
            await publisher_future
            await reader_future
    except WebSocketDisconnect:
        logging.info(msg=f"User {nickname} is disconnecting...")


def run_server(
    host: Annotated[str, typer.Option()] = "0.0.0.0",
    port: Annotated[int, typer.Option()] = 8000,
    redis: Annotated[str, typer.Option()] = "localhost",
) -> None:
    app.redis = redis
    uvicorn.run(app=app, host=host, port=port)


if __name__ == "__main__":
    typer.run(function=run_server)
