from typing import List
from models.base_model import BaseModel


class OptionGroup(BaseModel):
	""" list of options (choices) in each question """
	# texts: Json[List[str]]
	# images: Json[List[str]]
	texts: List[str]
	images: List[str]
