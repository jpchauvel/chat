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

In this case you have to first make sure you have Python and Poetry installed in
your system.

I will not give you details on how to install Python in your system, for that
you can go to [https://www.python.org](https://www.python.org).

To install poetry, just run the following command:

```sh
pip install -U poetry
```

Then, install all the test script dependencies, just so:

```sh
poetry install
```

After that you're good to run the test script!

```sh
poetry run ./testchat.py
```
