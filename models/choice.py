from models.base_model import BaseModel


class Choice(BaseModel):
	""" each answer from the user """
	attendee_id: int
	test_id: int
	session_id: int
	question_id: int
	choice: str
	completed_ms: int # how long did it take


class MinimalChoice(BaseModel):
	""" question_id and choice_id only (for accepting answers) """
	question_id: int
	choice_id: int
	