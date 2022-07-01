from models.base_model import BaseModel
from typing import Optional


""" list of customers """
class Customer(BaseModel):
	parent_id: Optional[int] = 0
	title: str = ""
	contact: str = ""
