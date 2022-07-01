from models.base_model import BaseModel


""" Application and company settings """
class Setting(BaseModel):
	company_id: int = 0
	slug: str
	typ: str
	value: str
