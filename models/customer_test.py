from typing import Optional
from models.base_model import BaseModel


class CustomerTest(BaseModel):
	""" tests created by our partners (eg peoplise) for their customers (eg turkcell) """
	partner_id: int
	customer_id: int
	test_id: int
	pretext: Optional[str] = ""
	title: Optional[str] = ""
	posttext: Optional[str] = ""
	timelimit_sec: int
