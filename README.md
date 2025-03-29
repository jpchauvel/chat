# Generic chat application built with Redis PubSub and FastAPI

This application has a single global room where all connected "users" can send
and receive messages.

You can build a web-based frontend using the Websockets API. The message is
basically a JSON object with the following form:

```json
{
    "nickname": "Joe Doe",
    "message": "A message"
}
```

**NOTE:** It does not echo the sender's message.

I've included a test CLI program called `testchat.py`. Its usage is pretty
straightforward: you just have to provide a nickname and then a message. After
that it waits for other users' messages to arrive. Once the messages are
received, the prompt to send a new message is presented once again. Looping
endlessly.

## Running the server

To run the server you just need docker (docker compose) installed in your
machine and the run the following command:

```sh
docker-compose -f docker-compose.yml up
```

## Running the test script

To build, install `uv`, follow the instructions in their documentation
<https://docs.astral.sh/uv/getting-started/installation/>, `uv` will handle all
the dependencies and the python installation as well. So we don't need to
install `python` separately.

Then, install all the test script dependencies, just so:

```sh
uv sync
```

After that you're good to run the test script!

```sh
uv run ./testchat.py
```
