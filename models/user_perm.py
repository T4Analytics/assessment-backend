from models.base_model import BaseModel


class UserPerm(BaseModel):
	""" permissions specific to users (not needed normally) """
	user_id: int
	perm_id: int
