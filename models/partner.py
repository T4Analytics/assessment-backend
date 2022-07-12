from models.base_model import BaseModel


class Partner(BaseModel):
	""" list of our partners """
	title: str = ""
	email: str = ""
