#!/usr/bin/env python3
import json

import typer
from typing_extensions import Annotated
from websockets.sync.client import connect
from websockets.typing import Data


def chat_cli(
    nickname: Annotated[
        str, typer.Option(help="Enter your nickname", prompt=True)
    ],
    api_url: Annotated[
        str, typer.Option(help="The URL of the chat API websocket")
    ] = "ws://localhost:8000/chat/",
) -> None:
    with connect(uri=api_url + nickname) as ws:
        print(f"Connected to chat as {nickname}")

        def on_message(message: Data) -> None:
            data = json.loads(s=message)
            sender = data["nickname"]
            content = data["message"]
            print(f"{sender}: {content}")

        try:
            while True:
                message: Data = typer.prompt(text="Your message", type=str)
                ws.send(
                    message=json.dumps(
                        {"nickname": nickname, "message": message}
                    )
                )
                # Receive and print messages from other users immediately after
                # sending a message
                message = ws.recv()
                if message:
                    on_message(message=message)
        except KeyboardInterrupt:
            ws.close()
            print("Disconnected from chat.")


if __name__ == "__main__":
    typer.run(function=chat_cli)
