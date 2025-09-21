"""
# @Date    : 2025/09/02
# @Author  : kui.xiao
# @Description :
"""

from fastapi import APIRouter, Depends, HTTPException, Response, Request, FastAPI, Query
from loguru import logger
import json
from datetime import datetime
from backend.schemas.chat_message import ChatMessageStore, ChatMessageFilter, FilterType
from backend.database.chat_message_tinydb import chat_message_tinydb, ChatMessageTinyDb
from tinydb import TinyDB, Query

app = FastAPI()

@app.post("/api/v1/log/store/chat_message")
async def handle_store_chat_message(request: Request):
    try:
        body = await request.json()
        chat_message_store = ChatMessageStore(**body)
        chat_message_tinydb.insert(chat_message_store.model_dump(exclude_unset=True))
    except Exception as e:
        logger.error(f"request error: {e}")

@app.post("/api/v1/log/search/chat_message")
def handle_search_chat_message(request: ChatMessageFilter):
    try:
        results = []
        db = chat_message_tinydb
        for ele in request.operator:
            if ele == FilterType.Id:
                results = db.search_by_id(request.uuid)
            if ele == FilterType.Time:
                results = db.search_by_time(request.start_time, request.end_time)
            if ele == FilterType.LatestN:
                results = db.search_latest_n(request.latest_n)
            if ele == FilterType.Content:
                results = db.search_by_content(request.content)
            if ele == FilterType.Criteria:
                results = db.search_by_criteria(request.latest_n, request.device_name, request.model_name)
            db = ChatMessageTinyDb().init_from_list("temp", results)

        return results
    except Exception as e:
        logger.error(f"Error querying by id: {e}")
        return []