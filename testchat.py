#!/usr/bin/env python3
import json

import click
from websockets.sync.client import connect


@click.command()
@click.option(
    "--nickname",
    prompt="Enter your nickname",
    help="Your nickname in the chat",
)
@click.option(
    "--api-url",
    default="ws://localhost:8000/chat/",
    help="The URL of the chat API websocket",
)
def chat_cli(nickname, api_url):
    with connect(api_url + nickname) as ws:
        click.echo(f"Connected to chat as {nickname}")

        def on_message(ws, message):
            data = json.loads(message)
            sender = data["nickname"]
            content = data["message"]
            click.echo(f"{sender}: {content}")

        try:
            while True:
                message = click.prompt("Your message", type=str)
                ws.send(json.dumps({"nickname": nickname, "message": message}))
                # Receive and print messages from other users immediately after
                # sending a message
                message = ws.recv()
                if message:
                    on_message(ws, message)
        except KeyboardInterrupt:
            ws.close()
            click.echo("Disconnected from chat.")


if __name__ == "__main__":
    chat_cli()
