from models.base_model import BaseModel
from modules.enums import ActionType, ObjectType
# from pydantic import Json
from sqlmodel import Field, Column, Enum


class AttendeeLog(BaseModel):
	""" action log for each attendee, test, session, question """
	attendee_id: int = 0
	partner_id: int = 0
	customer_id: int = 0
	paper_id: int = 0
	session_id: int = 0
	action_typ: ActionType = Field(sa_column=Column(Enum(ActionType)))  # what action was performed
	object_typ: ObjectType = Field(sa_column=Column(Enum(ObjectType)))
	object_id: int = 0  # together with object_typ, which object was modified
	completed_ms: int  # how long did it take
	# changes: Json[Dict, Dict] # may be included later on
