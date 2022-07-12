from models.base_model import BaseModel


class UserRole(BaseModel):
	""" groups users belong to """
	user_id: int
	role_id: int
