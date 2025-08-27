from typing import List, Optional
from pydantic import BaseModel, field_serializer, field_validator, Field
from enum import Enum
from typing import Union, Dict, Literal
from datetime import datetime

class ChatMessageStore(BaseModel):
    user: str = None
    uuid: str = None
    group_id: str = None
    finish_reason: str = None
    time_to_first_token:int = None
    time_to_last_token:int = None
    time_per_output_token:int = None
    token_count: int = 0
    messages: list = Field(default_factory=list)


DateTimeUnit = Literal["minutes", "hours", "days", "weeks", "months", "years"]

class LatestN(BaseModel):
    count: int
    unit: DateTimeUnit

class ChatMessageFilter(BaseModel):
    operator: list[Literal["uuid", "time", "latest_n", "content"]] = Field(default_factory=list)
    uuid: Optional[str] = None
    start_time: Optional[datetime]= None
    end_time: Optional[datetime]= None
    latest_n: Optional[LatestN]= None
    content: Optional[str]= None
