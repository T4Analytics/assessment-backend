from typing import Optional
from sqlmodel import Field
from models.base_model import BaseModel

""" tests created by our partners (eg peoplise) for their customers (eg turkcell) """
class CustomerTest(BaseModel):
	partner_id: int
	customer_id: int
	test_id: int
	pretext: Optional[str] = ""
	title: Optional[str] = ""
	posttext: Optional[str] = ""
	timelimit_sec: int
