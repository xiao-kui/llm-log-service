"""
# @Date    : 2025/09/05
# @Author  : kui.xiao
# @Description : 每天存储一个 tinydb，文件名格式为 YYYY-MM-DD.json，所有 search 方法会查遍所有 db
"""
import os

from streamlit.testing.v1.element_tree import ChatMessage
from tinydb import TinyDB, where
from tinydb.storages import MemoryStorage
from typing import Optional
from backend.schemas.chat_message import LatestN
from pathlib import Path
from datetime import datetime, timezone


class ChatMessageTinyDb:
    def __init__(self, base_dir: str = ''):
        self.dbs: dict[str, TinyDB] = {}
        self.current_day_str = ""
        if base_dir:
            self.base_dir = Path(base_dir)
            self.base_dir.mkdir(parents=True, exist_ok=True)
            for file in self.base_dir.rglob("*.json"):
                self.dbs[file.stem] = TinyDB(str(file))

    def _switch_db(self, now: datetime):
        """切换到对应日期的 tinydb 文件"""
        day_str = now.strftime("%Y-%m-%d")
        if day_str not in self.dbs:
            file_path = self.base_dir / f"{day_str}.json"
            self.dbs[day_str] = TinyDB(file_path)
        self.current_day_str = day_str
        self.db = self.dbs[day_str]

    def init_from_list(self, db_key, messages: list[ChatMessage]):
        """用给定的 ChatMessage 列表初始化内存数据库"""
        self.dbs[db_key] = TinyDB(storage=MemoryStorage)
        for msg in messages:
            if hasattr(msg, "to_dict"):
                record = msg.to_dict()
            elif hasattr(msg, "__dict__"):
                record = dict(msg.__dict__)
            else:
                raise TypeError(f"Unsupported ChatMessage type: {type(msg)}")

            self.dbs[db_key].insert(record)

        return self

    def insert(self, msg: dict) -> None:
        now = datetime.now(timezone.utc)
        self._switch_db(now)
        msg["datetime"] = now.timestamp()
        msg["datetime-formatted"] = now.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        self.db.insert(msg)

    # ----------------------
    # search 部分：遍历 self.dbs
    # ----------------------
    def _all_records(self):
        """返回所有 db 的全部记录"""
        for db in self.dbs.values():
            yield from db.all()

    def search_by_time(self, start_time: datetime, end_time: datetime) -> list[dict]:
        start_ts = start_time.timestamp()
        end_ts = end_time.timestamp()
        results = []
        for db in self.dbs.values():
            results.extend(
                db.search((where("datetime") >= start_ts) & (where("datetime") <= end_ts))
            )
        return results

    def search_by_uuid(self, uuid: str) -> list[dict]:
        results = []
        for db in self.dbs.values():
            results.extend(db.search(where("uuid") == uuid))  # type: ignore
        return results

    def search_latest_n(self, latest_n: LatestN) -> list[dict]:
        all_msgs = list(self._all_records())
        all_msgs.sort(key=lambda x: x.get("datetime", 0), reverse=True)
        return all_msgs[:latest_n.count]

    def search_by_content(self, content: str) -> list[dict]:
        results = []
        for item in self._all_records():
            messages = item.get("messages", [])
            if not messages:
                continue

            for idx, msg in enumerate(reversed(messages)):
                if msg.get("role") in ("user", "assistant"):
                    if content in msg.get("content", ""):
                        results.append(item)
                        break
                if idx > 1:
                    break
        return results


base_path = Path(__file__).parent.parent / "resources/tinydb"
chat_message_tinydb = ChatMessageTinyDb(str(base_path))
