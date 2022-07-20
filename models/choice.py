from sqlmodel import SQLModel
from models.base_model import BaseModel


class Choice(BaseModel):
	""" each answer from the user """
	attendee_id: int
	paper_id: int
	session_id: int
	question_id: int
	choice: int
	completed_ms: int  # how long did it take


class ChoiceNoDates(SQLModel):
	""" each answer from the user """
	id: int
	attendee_id: int
	paper_id: int
	session_id: int
	question_id: int
	choice: int
	completed_ms: int  # how long did it take


class MinimalChoice(BaseModel):
	""" question_id and choice_id only (for accepting answers) """
	question_id: int
	choice_id: int
