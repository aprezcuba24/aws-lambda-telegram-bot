import json
import os
from collections import defaultdict
from copy import deepcopy
from typing import Any, DefaultDict, Dict, Optional

from telegram.ext import BasePersistence, PersistenceInput
from telegram.ext._utils.types import CDCData, ConversationDict, ConversationKey

from app.utils.dynamodb import get_dynamodb_resource

dynamodb = get_dynamodb_resource()
PERSISTENCE_TABLE = os.environ.get("PERSISTENCE_TABLE")
RECORD_ID = "THE_ONLY_ID_RECORD"


class DynamodbPersistence(BasePersistence[Dict[Any, Any], Dict[Any, Any], Dict[Any, Any]]):
    """Using dynamodb to make the bot persistent"""

    def __init__(self, on_flush: bool = False):
        super().__init__(
            store_data=PersistenceInput(callback_data=False),
            update_interval=60,
        )
        self.on_flush = on_flush
        self.user_data: Optional[DefaultDict[int, Dict]] = None
        self.chat_data: Optional[DefaultDict[int, Dict]] = None
        self.bot_data: Optional[Dict] = None
        self.conversations: Optional[Dict[str, Dict[str, Any]]] = None

    def get_persistence_data(self):
        table = dynamodb.Table(PERSISTENCE_TABLE)
        key = {"persistence_id": RECORD_ID}
        item = table.get_item(Key=key)
        return item.get("Item", None)

    def load_data(self) -> None:
        data = self.get_persistence_data()
        if data:
            self.user_data = defaultdict(dict, json.loads(data["user_data"]))
            self.chat_data = defaultdict(dict, json.loads(data["chat_data"]))
            self.bot_data = json.loads(data["bot_data"])
            self.conversations = json.loads(data["conversations"])
        else:
            self.conversations = {}
            self.user_data = defaultdict(dict)
            self.chat_data = defaultdict(dict)
            self.bot_data = {}

    def dump_data(self) -> None:
        data = {
            "persistence_id": RECORD_ID,
            "conversations": json.dumps(self.conversations),
            "user_data": json.dumps(self.user_data),
            "chat_data": json.dumps(self.chat_data),
            "bot_data": json.dumps(self.bot_data),
        }
        table = dynamodb.Table(PERSISTENCE_TABLE)
        table.put_item(Item=data)

    async def get_user_data(self) -> Dict[int, Dict[Any, Any]]:
        if self.user_data is None:
            self.load_data()
        return deepcopy(self.user_data)  # type: ignore[arg-type]

    async def get_chat_data(self) -> Dict[int, Dict[Any, Any]]:
        if self.chat_data is None:
            self.load_data()
        return deepcopy(self.chat_data)  # type: ignore[arg-type]

    async def get_bot_data(self) -> Dict[Any, Any]:
        if self.bot_data is None:
            self.load_data()
        return deepcopy(self.bot_data)  # type: ignore[arg-type]

    async def get_callback_data(self) -> Optional[CDCData]:
        return None

    async def get_conversations(self, name: str) -> ConversationDict:
        if self.conversations is None:
            self.load_data()
        data = self.conversations.get(name, {}).copy()  # type: ignore[union-attr]
        result: ConversationDict = {}
        for key, value in data.items():
            parts = key.split("|")
            new_key: ConversationKey = (int(parts[0]), int(parts[1]))
            result[new_key] = value
        return result

    async def update_conversation(
        self, name: str, key: ConversationKey, new_state: Optional[object]
    ) -> None:
        str_key = f"{key[0]}|{key[1]}"
        if not self.conversations:
            self.conversations = {}
        if self.conversations.setdefault(name, {}).get(str_key) == new_state:
            return
        self.conversations[name][str_key] = new_state
        if not self.on_flush:
            self.dump_data()

    async def update_user_data(self, user_id: int, data: Dict[Any, Any]) -> None:
        if self.user_data is None:
            self.user_data = defaultdict(dict)
        if self.user_data.get(user_id) == data:
            return
        self.user_data[user_id] = data
        if not self.on_flush:
            self.dump_data()

    async def update_chat_data(self, chat_id: int, data: Dict[Any, Any]) -> None:
        if self.chat_data is None:
            self.chat_data = defaultdict(dict)
        if self.chat_data.get(chat_id) == data:
            return
        self.chat_data[chat_id] = data
        if not self.on_flush:
            self.dump_data()

    async def update_bot_data(self, data: Dict[Any, Any]) -> None:
        if self.bot_data == data:
            return
        self.bot_data = data.copy()
        if not self.on_flush:
            self.dump_data()

    async def update_callback_data(self, data: CDCData) -> None:
        pass

    async def drop_chat_data(self, chat_id: int) -> None:
        if self.chat_data is None:
            self.load_data()
        if chat_id in self.chat_data:
            del self.chat_data[chat_id]
            if not self.on_flush:
                self.dump_data()

    async def drop_user_data(self, user_id: int) -> None:
        if self.user_data is None:
            self.load_data()
        if user_id in self.user_data:
            del self.user_data[user_id]
            if not self.on_flush:
                self.dump_data()

    async def refresh_user_data(self, user_id: int, user_data: Dict[Any, Any]) -> None:
        pass

    async def refresh_chat_data(self, chat_id: int, chat_data: Dict[Any, Any]) -> None:
        pass

    async def refresh_bot_data(self, bot_data: Dict[Any, Any]) -> None:
        pass

    async def flush(self) -> None:
        self.dump_data()
