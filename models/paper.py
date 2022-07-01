from datetime import datetime
from typing import Union, Dict
from models.base_model import BaseModel
from sqlmodel import Column, Field
from pydantic import Json

""" each paper filled by attendees """
class Paper(BaseModel):
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
