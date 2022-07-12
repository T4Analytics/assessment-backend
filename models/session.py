from datetime import datetime
from typing import Union

from models.base_model import BaseModel
from modules.enums import SessionState


class NewSession(BaseModel):
	""" newly-created session """
	attendee_id: str
	paper_id: int
	state: SessionState
	started_at: datetime
	token: str


class Session(NewSession):
	""" active sessions """
	finished_at: Union[datetime, None]
	spent_sec: Union[int, None]


