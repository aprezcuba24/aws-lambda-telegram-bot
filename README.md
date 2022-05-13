# Project base to create a telegram's bot using AWS Lambda

This repository is a base project to create Telegram's bots using AWS and [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot).

The projedct will have a lambda function to catch the webhooks from telegram.

It also have another lambda function to configure the bot in Telegram.

Installation
------------
The first thing that you need to do is to clone this repository and change some values in the `serverles.yml` and `package.json` files. In the future we will have a **Cookiecutter Templete**

Development
-----------
The project already has a handler for the `start` command in `app/handlers/start.py` and you can create another ones in the **handlers** folder.

To connect the new handlers you need to add it in the **configure** method in the `app/webhook.py` file.

In the `app/register_webhook.py` you also can configure in Telegram, the commands that you bot will have.

To test the bot in your local machine yo can run
```
python manage.py
```
