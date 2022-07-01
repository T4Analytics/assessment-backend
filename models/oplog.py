from typing import Dict
from models.base_model import BaseModel
from modules.enums import ActionType, ObjectType
# from pydantic import Json
from sqlmodel import Field, Column, Enum


""" action log for each user, test, session, question """
class OpLog(BaseModel):
	user_id: int = 0
	action_typ: ActionType = Field(sa_column=Column(Enum(ActionType))) # what action was performed
	object_typ: ObjectType = Field(sa_column=Column(Enum(ObjectType))) 
	object_id: int = 0 # together with object_typ, which object was modified
	completed_ms: int # how long did it take
	# changes: Json[Dict, Dict] # may be included later on
