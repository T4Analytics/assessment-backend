from models.base_model import BaseModel
from typing import Optional


""" list of test attendees """
class Attendee(BaseModel):
	partner_id: int
	customer_id: int
	email: str = ""
	identifier: Optional[str] = ""
	token: str
