#!/usr/bin/env python3
import json

import typer
from typing_extensions import Annotated
from websockets.sync.client import connect


def chat_cli(
    nickname: Annotated[
        str, typer.Option(help="Enter your nickname", prompt=True)
    ],
    api_url: Annotated[
        str, typer.Option(help="The URL of the chat API websocket")
    ] = "ws://localhost:8000/chat/",
):
    with connect(api_url + nickname) as ws:
        print(f"Connected to chat as {nickname}")

        def on_message(ws, message):
            data = json.loads(message)
            sender = data["nickname"]
            content = data["message"]
            print(f"{sender}: {content}")

        try:
            while True:
                message = typer.prompt("Your message", type=str)
                ws.send(json.dumps({"nickname": nickname, "message": message}))
                # Receive and print messages from other users immediately after
                # sending a message
                message = ws.recv()
                if message:
                    on_message(ws, message)
        except KeyboardInterrupt:
            ws.close()
            print("Disconnected from chat.")


if __name__ == "__main__":
    typer.run(chat_cli)
