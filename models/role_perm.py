from models.base_model import BaseModel


""" permissions for each role """
class RolePerm(BaseModel):
	role_id: int
	perm_id: int
