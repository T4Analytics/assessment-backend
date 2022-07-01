from models.base_model import BaseModel
from typing import Union


""" list of users """
class User(BaseModel):
	partner_id: int = 0
	email: str = ""
	phone: Union[str, None] = None
	pwdhash: Union[str, None] = None
	token: Union[str, None] = None
