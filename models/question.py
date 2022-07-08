from models.base_model import BaseModel
from modules.enums import QuestionType
from models.optiongroup import OptionGroup
from typing import Optional, List


class Question(BaseModel):
	# """ each question in each test """
	typ: QuestionType = str
	pretext: Optional[str] = ""
	body: Optional[str] = ""
	posttext: Optional[str] = ""
	dimension: str
	modification: str
	optiongroup_id: OptionGroup
	# optiongroup_id: int
	test_id: int
	qorder: int


class DetailedQuestion(Question):
	options: List[OptionGroup]
