from models.base_model import BaseModel


""" groups users belong to """
class UserRole(BaseModel):
	user_id: int
	role_id: int
