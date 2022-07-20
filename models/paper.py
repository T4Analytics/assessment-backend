from datetime import datetime
from typing import Union
from sqlmodel import SQLModel
from models.base_model import BaseModel


class Paper(BaseModel):
	""" each paper filled by attendees """
	partner_id: int
	customer_id: int
	test_id: int
	attendee_id: int
	token: str
	started_at: Union[datetime, None] = None
	finished_at: Union[datetime, None] = None
	min_start_at: Union[datetime, None] = None
	max_end_at: Union[datetime, None] = None
	evaluated_at: Union[datetime, None] = None
	pdf_at: Union[datetime, None] = None
	# result_json: Dict = Field(default={}, sa_column=Column(Json))
	result_json: dict
	spent_sec: int
	allowed_sec: int
	
	class Config:
		arbitrary_types_allowed = True


class DemoPaper(SQLModel):
	""" used in creating demo papers """
	token: str
	allowed_sec: int


class SimplePaper(SQLModel):
	""" used when responding with paper info """
	spent_sec: int
	allowed_sec: int
	min_start_at: Union[datetime, None]
	max_end_at: Union[datetime, None]
	pretext: str
	test_type: str
	session_token: str
	question_count: int
	choices: dict
	is_completed: int
	started_at: Union[datetime, None]
	finished_at: Union[datetime, None]
	active_question_token: Union[str, None]


class MinimalPaper(SQLModel):
	""" used when responding to paper ticks """
	token: str
	spent_sec: int
	allowed_sec: int
