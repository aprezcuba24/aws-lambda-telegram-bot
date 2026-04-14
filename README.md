# Project base to create a telegram's bot using AWS Lambda

This repository is a base project to create Telegram's bots using AWS and [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot).

The deployed stack uses **AWS Lambda** with a **Function URL** (HTTP), not API Gateway:

- `/webhook`: Receives Telegram updates and runs handlers.
- `/register-bot`: Sets the Telegram webhook and bot commands.

Installation
------------
The first thing that you need to do is to clone this repository and change some values in the `serverless.yml` and `package.json` files. In the future, we will have a **Cookiecutter Template**.

Local development (Docker)
--------------------------
For development you can run **DynamoDB Local**, **dynamodb-admin** (web UI), and the dev container from [local.yml](local.yml) without touching AWS DynamoDB.

1. Copy the env template and set your bot token:
   ```bash
   cp .envs/.local/.app.example .envs/.local/.app
   # Edit .envs/.local/.app and set TELEGRAM_TOKEN
   ```

2. Start Compose (DynamoDB Local on port **8000**, admin UI on **8001**, app container stays idle). Si tu instalación solo tiene el binario `docker-compose` (con guion), usa ese mismo comando con `-f local.yml`.
   ```bash
   docker compose -f local.yml up -d
   ```

3. Open **dynamodb-admin** in the browser: [http://localhost:8001](http://localhost:8001) (inspect tables and items).

4. Enter the app container and create tables once (el servicio se llama `app`; no uses nombres fijos de contenedor para evitar conflictos):
   ```bash
   docker compose -f local.yml exec app bash
   python scripts/create_tables.py
   ```

5. Run the bot in **polling** mode (good for local dev):
   ```bash
   python manager.py
   ```

Environment variables for local dev are documented in [.envs/.local/.app.example](.envs/.local/.app.example). `DYNAMODB_ENDPOINT` points at the `dynamodb-local` service from inside the Compose network.

If you run Python **on the host** (not inside Docker), set `DYNAMODB_ENDPOINT=http://localhost:8000` in your env instead.

The VS Code **Dev Container** (`.devcontainer/devcontainer.json`) starts `app`, `dynamodb-local`, and `dynamodb-admin` together.

Development
-----------
The project has the following folders:

- `app/handlers`: Handlers for Telegram updates (e.g. Start command).
- `app/models`: DynamoDB access (e.g. user table).
- `app/utils`: Supporting code (dispatcher, persistence, metrics).
- `app/main.py`: Lambda handler for webhook + register routes.

Example
-------
The project already has a command to start the bot.

1. Create the file `app/handlers/start.py`
```
from string import Template
from telegram import Update

from app.utils.callback_context import CallbackContext


START_TEXT = """
Hello "$name"
"""


def start_query(update: Update, context: CallbackContext):
    user_model = context.user_db # this is the logic to get or create the user from database.
    update.effective_message.edit_text(text=Template(START_TEXT).substitute(name=user_model["complete_name"]))
```

2. Next step is to register the command in the **configure** method in the file `app/config.py`
```
def configure_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler(command="start", callback=start_command))
```

3. To test the bot locally with Docker and DynamoDB Local, follow **Local development (Docker)** above. The entrypoint is:
```
python manager.py
```

Docker, VS Code, and Serverless Framework
-----------------------------------------
The project has the file `.devcontainer/devcontainer.json` to execute the application in **VS Code** and build the docker containers.

To work with **Serverless Framework** you need to install the **NPM modules** and then you can use the commands registered in the `package.json`.

Run tests
```
python -m pytest
```
