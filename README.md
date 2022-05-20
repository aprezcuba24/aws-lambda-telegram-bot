# Project base to create a telegram's bot using AWS Lambda

This repository is a base project to create Telegram's bots using AWS and [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot).

This project has two lambda functions with their **Api Gateway** configuration:

- /webhook: This endpoint is to catch the webhooks that come from Telegram and respond to the message.
- /register_webhook: This endpoint configures the bot in Telegram. For example, in this endpoint, the bot configures what commands it has.

Installation
------------
The first thing that you need to do is to clone this repository and change some values in the `serverles.yml` and `package.json` files. In the future, we will have a **Cookiecutter Templete**

Development
-----------
The project has the following folders:

- handlers: In this folder will have the code to handle the different requests that come from Telegram. In the project, you can see the Start command handler.
- models: In this folder, we can implement the code to access `dynamodb`. Now the project has the code to manage the user table.
- utils: The code for supporting and not related to the current business logic.
- It also has the two lambdas, webhook, and register_webhook.

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

3. Finally, to test the bot in your local machine you can run this command.
```
python manage.py
```

Note: To work the application needs to have the **dynamodb** in the **AWS**

Docker, VScode, and Serverless Framework
----------------------------------------
The project has the file `.devcontainer/devcontainer.json` to execute the application into **VScode** and build the docker containers.

To work with **Serverless Framework** you need to install the **NPM modules** and after you can use the commands registered in the `package.json`