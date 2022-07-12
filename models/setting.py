from models.base_model import BaseModel


class Setting(BaseModel):
	""" Application and company settings """
	company_id: int = 0
	slug: str
	typ: str
	value: str
