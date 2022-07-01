from typing import List
from pydantic import Json
from models.base_model import BaseModel
from sqlmodel import Column, Field
from pydantic import Json
from typing import Dict


""" list of options (choices) in each question """
class OptionGroup(BaseModel):
	# texts: Json[List[str]]
	# images: Json[List[str]]
	texts: List[str]
	images: List[str]
