from models.base_model import BaseModel


""" each answer from the user """
class Choice(BaseModel):
	attendee_id: int
	test_id: int
	session_id: int
	question_id: int
	choice: str
	completed_ms: int # how long did it take
