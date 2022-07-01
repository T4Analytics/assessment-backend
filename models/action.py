from datetime import datetime
from modules.enums import ActionType, ObjectType
from models.base_model import BaseModel
from sqlmodel import Field, Column, Enum
from typing import Union

class Action(BaseModel):
	action_typ: ActionType = Field(sa_column=Column(Enum(ActionType)))
	object_typ: ObjectType = Field(sa_column=Column(Enum(ObjectType)))
	object_id: int
	started_at: datetime = Field(default=datetime.now())
	completed_ms: Union[int,None] = None
