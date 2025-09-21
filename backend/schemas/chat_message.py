"""
# @Date    : 2025/09/02
# @Author  : kui.xiao
# @Description :
"""

from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict, model_validator
from enum import Enum
from typing import Union, Dict, Literal
from datetime import datetime

class ChatMessageStore(BaseModel):
    user: str = None
    id: str = None
    group_id: str = None
    finish_reason: str = None
    time_to_first_token:str = None
    time_to_last_token:str = None
    time_per_output_token: str = None
    tokens_per_second:str = None
    token_size: int = 0
    device_name: str = None
    model_name: str = None
    messages: list = Field(default_factory=list)
    additional_kwargs: dict = Field(default_factory=dict)

    model_config = ConfigDict(extra="allow")

    @model_validator(mode="before")
    def reset_additional_kwargs(cls, values):
        if isinstance(values, dict):
            known_fields = set(cls.model_fields.keys())
            extra = {k: v for k, v in values.items() if k not in known_fields}
            values["additional_kwargs"] = extra
        return values

class TimeUnitType(str, Enum):
    Minutes = "Minutes"
    Hours = "Hours"
    Days = "Days"
    Weeks = "Weeks"
    Months = "Months"
    Years = "Years"

class FilterType(str, Enum):
    Id = "Id"
    Time = "Time"
    LatestN = "LatestN"
    Content = "Content"
    DeviceName = "DeviceName"
    ModelName = "ModelName"
    Criteria = "Criteria"

class ChatMessageFilter(BaseModel):
    operator: list[FilterType] = Field(default_factory=list)
    id: Optional[str] = None
    start_time: Optional[datetime]= None
    end_time: Optional[datetime]= None
    latest_n: Optional[int]= None
    content: Optional[str]= None
    device_name: Optional[str]= None
    model_name: Optional[str]= None

