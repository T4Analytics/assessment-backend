from models.base_model import BaseModel
from typing import Union


class User(BaseModel):
	""" list of users """
	partner_id: int = 0
	email: str = ""
	phone: Union[str, None] = None
	pwdhash: Union[str, None] = None
	token: Union[str, None] = None
