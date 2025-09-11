"""
# @Date    : 2025/09/02
# @Author  : kui.xiao
# @Description :
"""

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
    time_to_first_token:str = None
    tokens_per_second:str = None
    time_per_output_token:str = None
    token_count: int = 0
    messages: list = Field(default_factory=list)


class TimeUnitType(str, Enum):
    Minutes = "Minutes"
    Hours = "Hours"
    Days = "Days"
    Weeks = "Weeks"
    Months = "Months"
    Years = "Years"

class FilterType(str, Enum):
    Uuid = "Uuid"
    Time = "Time"
    LatestN = "LatestN"
    Content = "Content"

class LatestN(BaseModel):
    count: int

class ChatMessageFilter(BaseModel):
    operator: list[FilterType] = Field(default_factory=list)
    uuid: Optional[str] = None
    start_time: Optional[datetime]= None
    end_time: Optional[datetime]= None
    latest_n: Optional[LatestN]= None
    content: Optional[str]= None
