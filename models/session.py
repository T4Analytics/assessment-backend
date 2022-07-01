from datetime import datetime
from models.base_model import BaseModel
from modules.enums import SessionState

""" active sessions """
class Session(BaseModel):
	attendee_id: str
	paper_id: int
	state: SessionState
	started_at: datetime
	finished_at: datetime
	token: str
	spent_sec: int
