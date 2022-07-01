from models.base_model import BaseModel
from typing import Optional

""" permissions """
class Perm(BaseModel):
	slug: str
	title: Optional[str]
