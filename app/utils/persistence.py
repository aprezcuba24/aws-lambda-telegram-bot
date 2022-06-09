import json
import os
import boto3
from collections import defaultdict
from copy import deepcopy
from typing import Any, DefaultDict, Dict, Optional, Tuple

from telegram.ext import BasePersistence


region = os.environ.get("REGION")
dynamodb = boto3.resource("dynamodb", region_name=region)
PERSISTENCE_TABLE = os.environ.get("PERSISTENCE_TABLE")
RECORD_ID="THE_ONLY_ID_RECORD"


class DynamodbPersistence(BasePersistence):
    '''Using dynamodb to make the bot persistent'''

    def __init__(self, on_flush: bool = False):
        super().__init__(store_user_data=True,store_chat_data=True,store_bot_data=True)
        self.on_flush = on_flush
        self.user_data: Optional[DefaultDict[int, Dict]] = None
        self.chat_data: Optional[DefaultDict[int, Dict]] = None
        self.bot_data: Optional[Dict] = None
        self.conversations: Optional[Dict[str, Dict[Tuple, Any]]] = None

    def get_persistence_data(self):
        table = dynamodb.Table(PERSISTENCE_TABLE)
        Key = {"persistence_id": RECORD_ID}
        item = table.get_item(Key=Key)
        return item.get("Item", None)

    def load_data(self) -> None:
        data = self.get_persistence_data()
        if data:
            self.user_data = defaultdict(dict, json.loads(data['user_data']))
            self.chat_data = defaultdict(dict, json.loads(data['chat_data']))
            # For backwards compatibility with files not containing bot data
            self.bot_data = json.loads(data['bot_data'])
            self.conversations = json.loads(data['conversations'])
        else:
            self.conversations = dict()
            self.user_data = defaultdict(dict)
            self.chat_data = defaultdict(dict)
            self.bot_data = {}

    def dump_data(self) -> None:
        data = {
            "persistence_id": RECORD_ID,
            'conversations': json.dumps(self.conversations),
            'user_data': json.dumps(self.user_data),
            'chat_data': json.dumps(self.chat_data),
            'bot_data': json.dumps(self.bot_data),
        }
        table = dynamodb.Table(PERSISTENCE_TABLE)
        table.put_item(Item=data)

    def get_user_data(self) -> DefaultDict[int, Dict[Any, Any]]:
        if self.user_data:
            pass
        else:
            self.load_data()
        return deepcopy(self.user_data)  # type: ignore[arg-type]

    def get_chat_data(self) -> DefaultDict[int, Dict[Any, Any]]:
        if self.chat_data:
            pass
        else:
            self.load_data()
        return deepcopy(self.chat_data)  # type: ignore[arg-type]

    def get_bot_data(self) -> Dict[Any, Any]:
        if self.bot_data:
            pass
        else:
            self.load_data()
        return deepcopy(self.bot_data)  # type: ignore[arg-type]

    def get_conversations(self, name: str) -> Dict:
        if self.conversations:
            pass
        else:
            self.load_data()
        data = self.conversations.get(name, {}).copy()  # type: ignore[union-attr]
        result = {}
        for key, value in data.items():
            new_key = key.split("|")
            new_key = (int(new_key[0]), int(new_key[1]))
            result[new_key] = value
        return result

    def update_conversation(self, name: str, key: Tuple[int, ...], new_state: Optional[object]) -> None:
        new_key = f"{key[0]}|{key[1]}"
        if not self.conversations:
            self.conversations = dict()
        if self.conversations.setdefault(name, {}).get(new_key) == new_state:
            return
        self.conversations[name][new_key] = new_state
        if not self.on_flush:
            self.dump_data()

    def update_user_data(self, user_id: int, data: Dict) -> None:
        if self.user_data is None:
            self.user_data = defaultdict(dict)
        if self.user_data.get(user_id) == data:
            return
        self.user_data[user_id] = data
        if not self.on_flush:
            self.dump_data()

    def update_chat_data(self, chat_id: int, data: Dict) -> None:
        if self.chat_data is None:
            self.chat_data = defaultdict(dict)
        if self.chat_data.get(chat_id) == data:
            return
        self.chat_data[chat_id] = data
        if not self.on_flush:
            self.dump_data()

    def update_bot_data(self, data: Dict) -> None:
        if self.bot_data == data:
            return
        self.bot_data = data.copy()
        if not self.on_flush:
            self.dump_data()

    def flush(self) -> None:
        self.dump_data()
