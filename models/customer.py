from models.base_model import BaseModel
from typing import Optional


class Customer(BaseModel):
	""" list of customers """
	parent_id: Optional[int] = 0
	title: str = ""
	contact: str = ""
