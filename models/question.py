from models.base_model import BaseModel
from modules.enums import QuestionType
from models.optiongroup import OptionGroup
from sqlmodel import Enum, Column, Field
from typing import Optional
#from sqlalchemy.sql.sqltypes import Dict

""" each question in each test """
class Question(BaseModel):
	typ: QuestionType = Field(sa_column=Column(Enum(QuestionType)))
	pretext: Optional[str] = ""
	body: Optional[str] = ""
	posttext: Optional[str] = ""
	dimension: str
	modification: str
	# optiongroup_id: OptionGroup = Field(sa_column=Column(Enum(OptionGroup)))
	optiongroup_id: int
	test_id: int
	qorder: int
