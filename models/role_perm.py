from models.base_model import BaseModel


class RolePerm(BaseModel):
	""" permissions for each role """
	role_id: int
	perm_id: int
