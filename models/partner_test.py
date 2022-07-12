from models.base_model import BaseModel


class PartnerTest(BaseModel):
	""" tests allowed to partners """
	partner_id: int
	test_id: int
