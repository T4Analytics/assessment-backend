from models.base_model import BaseModel
from modules.enums import QuestionType
from typing import Union


class Question(BaseModel):
	""" each question in each test """
	typ: QuestionType = str
	pretext: Union[str, None] = ""
	body: Union[str, None] = ""
	posttext: Union[str, None] = ""
	dimension: str
	modification: int = 0
	optiongroup_id: int
	test_id: int
	qorder: int


class DetailedQuestion(Question):
	# """ question and options combined """
	options: list
	choice: int
