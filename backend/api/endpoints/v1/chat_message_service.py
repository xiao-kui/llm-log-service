from fastapi import APIRouter, Depends, HTTPException, Response, Request, FastAPI, Query
from loguru import logger
import json
from datetime import datetime
from backend.schemas.chat_message import ChatMessageStore, ChatMessageFilter
from backend.database.chat_message_tinydb import chat_message_tinydb, ChatMessageTinyDb
from tinydb import TinyDB, Query

app = FastAPI()

@app.post("/api/v1/log/store/chat_message")
async def handle_store_chat_message(request: ChatMessageStore):
    try:
        chat_message_tinydb.insert(request.model_dump())
    except Exception as e:
        logger.error(f"request error: {e}")

@app.post("/api/v1/log/search/chat_message")
def handle_search_chat_message(request: ChatMessageFilter):
    try:
        results = []
        db = chat_message_tinydb
        for ele in request.operator:
            if ele == "id":
                results = db.query_by_id(request.uuid)
            if ele == "time":
                results = db.query_by_time(request.start_time, request.end_time)
            if ele == "latest_n":
                results = db.query_latest_n(request.latest_n)
            if ele == "content":
                results = db.query_by_content(request.content)
            db = ChatMessageTinyDb().init_from_list(results)

        return results
    except Exception as e:
        logger.error(f"Error querying by id: {e}")
        return {}