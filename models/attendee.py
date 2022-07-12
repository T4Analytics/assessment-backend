from models.base_model import BaseModel
from typing import Optional


class Attendee(BaseModel):
	""" list of test attendees """
	partner_id: int
	customer_id: int
	email: str = ""
	identifier: Optional[str] = ""
	token: str
