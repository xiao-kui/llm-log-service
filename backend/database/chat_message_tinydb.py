from streamlit.testing.v1.element_tree import ChatMessage
from tinydb import TinyDB, Query
import re
from typing import Optional
from backend.schemas.chat_message import LatestN
from pathlib import Path
from tinydb.queries import QueryLike
from tinydb.storages import MemoryStorage
from tinydb import where
from datetime import datetime, timezone

class ChatMessageTinyDb:
    def __init__(self):
        self.db: Optional[TinyDB] = None

    def init_from_path(self, path:str):
        self.db = TinyDB(path)
        return self

    def init_from_list(self, messages: list[ChatMessage]):
        """用给定的 ChatMessage 列表初始化内存数据库"""
        self.db = TinyDB(storage=MemoryStorage)
        for msg in messages:
            if hasattr(msg, "to_dict"):
                record = msg.to_dict()
            elif hasattr(msg, "__dict__"):
                record = dict(msg.__dict__)
            else:
                raise TypeError(f"Unsupported ChatMessage type: {type(msg)}")

            self.db.insert(record)

        return self

    def insert(self, msg: dict) -> None:
        msg["time"] = datetime.now().timestamp()
        msg["time"] = datetime.now(timezone.utc).timestamp()
        self.db.insert(msg)

    def search_by_time(self, start_time: datetime, end_time: datetime) -> list[dict]:
        """按时间区间查询消息"""
        start_ts = start_time.timestamp()
        end_ts = end_time.timestamp()
        return self.db.search((where("time") >= start_ts) & (where("time") <= end_ts))

    def search_by_uuid(self, uuid: str) -> list[dict]:
        """根据 uuid 查询消息"""
        return self.db.search(where("uuid") == uuid) # type: ignore

    def search_latest_n(self, latest_n: LatestN) -> list[dict]:
        all_msgs = self.db.all()
        all_msgs.sort(key=lambda x: x.get("time", 0), reverse=True)
        return all_msgs[:latest_n.count]

    def search_by_content(self, content: str) -> list[dict]:
        results = []
        for item in self.db.all():
            messages = item.get("messages", [])
            if not messages: continue

            for idx, msg in enumerate(reversed(messages)):
                if msg.get("role") == "user" or msg.get("role") == "assistant":
                    if content in msg.get("content", ''):
                        results.append(item)
                        break
                if idx > 1:
                    break

        return results

file_path = Path(__file__).parent.parent / "resources/chat_messages.json"
chat_message_tinydb = ChatMessageTinyDb().init_from_path(str(file_path))