from models.base_model import BaseModel
from typing import Optional


class Perm(BaseModel):
	""" permissions """
	slug: str
	title: Optional[str]
