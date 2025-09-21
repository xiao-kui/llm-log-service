"""
# @Date    : 2025/09/05
# @Author  : kui.xiao
# @Description :
"""

import streamlit as st
from datetime import datetime, time, timedelta, timezone
import httpx
from backend.schemas.chat_message import ChatMessageFilter

from typing import List, Dict
from backend.schemas.chat_message import FilterType

API_BASE_URL = "http://127.0.0.1:9015/api/v1/log/search/chat_message"

def fetch_messages_by_time(start: datetime, end: datetime) -> List[Dict]:
    payload = ChatMessageFilter(operator=[FilterType.Time],start_time=start, end_time=end).model_dump_json()
    resp = httpx.post(API_BASE_URL, content=payload, headers={"Content-Type": "application/json"})
    resp.raise_for_status()
    return resp.json()

def fetch_message_by_id(id: str) -> Dict:
    payload = ChatMessageFilter(operator=[FilterType.Id], id=id).model_dump()
    resp = httpx.post(API_BASE_URL, json=payload)
    resp.raise_for_status()
    return resp.json()


def fetch_message_by_latest_n(latest_n: int) -> Dict:
    payload = ChatMessageFilter(operator=[FilterType.LatestN], latest_n=latest_n).model_dump()
    resp = httpx.post(API_BASE_URL, json=payload)
    resp.raise_for_status()
    return resp.json()

def fetch_messages_by_content(content: str) -> Dict:
    payload = ChatMessageFilter(operator=[FilterType.Content], content=content).model_dump()
    resp = httpx.post(API_BASE_URL, json=payload)
    resp.raise_for_status()
    return resp.json()

# Search by criteria
def fetch_messages_by_criteria(latest_n:int, device_name: str, model_name: str) -> Dict:
    payload = ChatMessageFilter(operator=[FilterType.Criteria],
                                latest_n=latest_n,
                                device_name=device_name,
                                model_name=model_name).model_dump()

    resp = httpx.post(API_BASE_URL, json=payload)
    resp.raise_for_status()
    return resp.json()

# ----- Sidebar Render Functions -----
def render_sidebar_time_query():
    with st.sidebar.expander("🕒 Search by Time", expanded=False):
        start_date = st.date_input("Start Date", datetime.now(), key="start_date")
        start_time_val = st.time_input("Start Time", time(0, 0), key="start_time")
        end_date = st.date_input("End Date", datetime.now(), key="end_date")
        end_time_val = st.time_input("End Time", time(23, 59), key="end_time")

        # 🌍 时区选择
        tz_offset = st.number_input("Timezone Offset", min_value=-12, max_value=14, value=0, step=1, key="tz_offset")

        start_dt_local = datetime.combine(start_date, start_time_val)
        end_dt_local = datetime.combine(end_date, end_time_val)

        # 转换为 UTC
        tzinfo = timezone(timedelta(hours=tz_offset))
        start_dt_utc = start_dt_local.replace(tzinfo=tzinfo).astimezone(timezone.utc)
        end_dt_utc = end_dt_local.replace(tzinfo=tzinfo).astimezone(timezone.utc)

        if st.button("Search", key="query_time"):
            st.session_state["query_result"] = fetch_messages_by_time(start_dt_utc, end_dt_utc)


def render_sidebar_id_query():
    with st.sidebar.expander("🆔 Search by ID", expanded=False):
        message_id = st.text_input("Enter Message ID", key="id_input")
        if st.button("Search", key="search_by_id"):
            if message_id:
                st.session_state["query_result"] = fetch_message_by_id(message_id)
            else:
                st.session_state["query_result"] = {"error": "Message ID is required"}


def render_sidebar_latest_query():
    with st.sidebar.expander("🆕 Search By Latest N", expanded=False):
        count = st.number_input("Number of messages", min_value=1, max_value=1000, value=5, step=1, key="latest_n")
        if st.button("Search", key="query_latest_n"):
            latest_n = count
            msgs = fetch_message_by_latest_n(latest_n)
            st.session_state["query_result"] = msgs if msgs else [{"info": "No messages found"}]

def render_sidebar_content_query():
    with st.sidebar.expander("🔍 Search By Content", expanded=False):
        count = st.text_input("content", key="content")
        if st.button("Search", key="query_by_content"):
            msgs = fetch_messages_by_content(count)
            st.session_state["query_result"] = msgs if msgs else [{"info": "No messages found"}]

def render_sidebar_criteria_query():
    with st.sidebar.expander("⚙️ Search By Condition", expanded=False):
        latest_n = st.number_input("latest_n", value=50)
        device_name = st.text_input("device_name", value="8295")
        model_name = st.text_input("model_name")
        if st.button("Search", key="query_by_conditions"):
            msgs = fetch_messages_by_criteria(latest_n, device_name, model_name)
            st.session_state["query_result"] = msgs if msgs else [{"info": "No messages found"}]

def render_query_results():
    if "query_result" in st.session_state:
        st.json(st.session_state["query_result"])

def main():
    st.title("📑 Chat Message Viewer")

    render_sidebar_time_query()
    render_sidebar_id_query()
    render_sidebar_latest_query()
    render_sidebar_content_query()
    render_sidebar_criteria_query()
    render_query_results()


if __name__ == "__main__":
    main()
