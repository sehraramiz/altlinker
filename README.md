A messenger bot to provide alternative links to Twitter, YouTube, and other services.

Currently, it is a Telegram bot that replies to messages containing Twitter or YouTube links with the exact copy of that message modified with alternative links.

This bot uses [Farside, a redirecting service for FOSS alternative frontends](https://github.com/benbusby/farside). Farside already provides a reliable way of monitoring, load balancing, and redirecting [alternative frontends](https://github.com/mendel5/alternative-front-ends).

Use [@AltLinkerBot](https://t.me/AltLinkerBot) in groups to encourage the usage of these [privacy-friendly options](https://github.com/Lissy93/awesome-privacy#proxy-sites).


### Install requirements

```console
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install poetry
$ poetry install
```

### Instructions for setting up telegram bot

#### with webhook

1 - submit webhook on telegram api

```console
$ export BOT_TOKEN=bot-token-rstuvwxyz
$ export WEBHOOK_URL=https://yourdomain.com/telegram/hook
$ make webhook-set
{"ok":true,"result":true,"description":"Webhook was set"}
```
2 - run server

```console
$ export TELEGRAM_BOT_TOKEN=bot-token-rstuvwxyz
$ export PORT=8000
$ sh scripts/server.sh
```

3 - setup nginx to forward requests to port $PORT (8000)
    
telegram webhook url must be https

```nginx
server {
        listen 443 ssl;
        listen [::]:443 ssl;

        server_name altlinker.folan;

        location / {
                proxy_pass http://localhost:8000/;
        }

        ssl_certificate /etc/letsencrypt/live/altlinker.folan/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/altlinker.folan/privkey.pem;
}
```

#### with long polling

1 - delete webhook on telegram api

```console
$ export BOT_TOKEN=bot-token-rstuvwxyz
$ make webhook-delete
{"ok":true,"result":true,"description":"Webhook was deleted"}
```

2 - run server

```console
$ export TELEGRAM_BOT_TOKEN=bot-token-rstuvwxyz
$ sh scripts/polling.sh
```
