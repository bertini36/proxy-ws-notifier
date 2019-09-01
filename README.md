# proxy-ws-notifier

This service redirects RabbitMQ messages of a concrete routing key to its
user browser using a websocket connection.

First user has to be connected to its endpoint `/notifications/<user_id>/`.
```javascript
const ws = new WebSocket("ws://127.0.0.1:8000/notifications/<user_id>/");
console.log("Waiting for notifications...");

ws.onmessage = function(event) {
    let data;
    try {
        data = JSON.parse(event.data);
        console.log(data);
    } catch(e) {
        return console.log(e);
    }
};
```
Then all RabbitMQ messages received with the routing key `<user_id>` will
be sended using the websocket connection established. You can check 
[RabbitMQ documentation](https://www.rabbitmq.com/tutorials/tutorial-four-python.html).

## Prerequisites

If you don’t have Docker installed, follow the instructions for your OS:

- On Mac OS X, you’ll need [Docker for Mac](https://docs.docker.com/docker-for-mac/)
- On Windows, you’ll need [Docker for Windows](https://docs.docker.com/docker-for-windows/)
- On Linux, you’ll need [docker-engine](https://docs.docker.com/engine/installation/)

And aditionally install [Docker compose](https://docs.docker.com/compose/install/)

## Usage

**Build environment**
```bash
make build
```

**Run environment**
```bash
make up
```

**Stop environment**
```bash
make down
```

You can specify your own configurations in a `.env` file.
```
cp notifier/.env-sample notifier/.env
```

## Testing notifications
Follow these steps to check notifications.
- Open `notifier/templates/receiver.html` in your web browser.
- Specify an user (you only will receive its notifications) and click "Connect".
- Now, in another browser tab you can request `<HOST>:<PORT>/send/test/notification/<user>/` where
  user has to be the name which you have specified previously.
- Then in the first tab javascript console you will see the generated test notification.

<p align="center">&mdash; Built with :heart: from Mallorca &mdash;</p>