from models.base_model import BaseModel


""" permissions specific to users (not needed normally) """
class UserPerm(BaseModel):
	user_id: int
	perm_id: int
