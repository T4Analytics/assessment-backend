import time
from typing import Union, Optional
from fastapi import APIRouter

from models.choice import Choice
from models.paper import SimplePaper, DemoPaper
from models.question import DetailedQuestion
from modules.constants import Constants
from modules.enums import TestType
from modules.helpers import Helpers

h = Helpers()
c = Constants()
router = APIRouter(prefix="/api/v1/assessments", tags=["papers"])


@router.post("/demo", response_model=DemoPaper)
async def create_demo_paper(paper_type: TestType = "MB"):
	""" create new demo paper """
	partner = h.db_createorselect(c.tblPartners, {"title": "Demo"})
	customer = h.db_createorselect(c.tblCustomers, {"title": "Demo"})
	test = h.db_createorselect(c.tblTests, {"paper_type": paper_type})
	attendee = h.db_createorselect(c.tblAttendees, {"identifier": "demo"})
	customertest = h.db_createorselect(c.tblCustomerTests, {"customer_id": customer["id"], "test_id": test["id"], "partner_id": partner["id"], "title": f"{paper_type} Demo", "timelimit_sec": 1200})
	partnertest = h.db_createorselect(c.tblPartnerTests, {"test_id": test["id"], "partner_id": partner["id"], })
	paperdata = {"partner_id": partner["id"], "customer_id": customer["id"], "test_id": test["id"], "customertest_id": customertest["id"], "partnertest_id": partnertest["id"], "attendee_id": attendee["id"], "allowed_sec": 1200, "token": "demo"}
	paper = h.db_createorselect(c.tblPapers, paperdata)
	paper["session_token"] = h.create_attendee_session(paper)
	return DemoPaper(id=paper["id"], token=paper["token"], allowed_sec=paper["allowed_sec"], session_token=paper["session_token"])


@router.get("/papers/{paper_id}", response_model=SimplePaper)
async def get_paper_info(paper_id: int, token: str) -> SimplePaper:
	""" get info about specific paper """
	paper_dict = h.db_selectsingle(c.tblPapers, {"id": paper_id, "token": token})
	test = h.db_selectsingle(c.tblTests, {"id": paper_dict["test_id"]})
	paper = SimplePaper(spent_sec=paper_dict["spent_sec"], allowed_sec=paper_dict["allowed_sec"], min_start_at=paper_dict["min_start_at"], max_end_at=paper_dict["max_end_at"], pretext=test["pretext"], question_count=0, choices={}, session_token="")
	paper.choices = h.questions_choices(paper_dict["test_id"], paper_dict["id"])
	paper.question_count = len(paper.choices)
	h.close_attendee_sessions(paper_dict["id"])
	paper.session_token = h.create_attendee_session(paper_dict["id"])
	return paper


@router.get("/papers/{paper_id}/questions/{question_id}", response_model=DetailedQuestion)
async def get_question_in_paper(paper_id: int, paper_token: str, question_id: int) -> DetailedQuestion:
	""" get the question and the options in a question of a specific paper """
	# TODO: must also receive and check session info
	paper = h.db_selectsingle(c.tblPapers, {"id": paper_id, "token": paper_token})
	if not paper:
		h.http404("Paper not found")
	test = h.db_selectsingle(c.tblTests, {"id": paper["test_id"]})
	if not test:
		h.http404("Test not found")
	return h.detailed_question(test["id"], paper["id"], question_id)


@router.post("/{paper_id}/questions/{question_id}")
async def save_answer_to_question(paper_id: int, paper_token: str, question_id: int, choice: int, session_token: str, next_question_id: Optional[int] = None):
	""" save user's answer to a question """
	# TODO: gelen cevabi kaydetmeli
	# TODO: istenen bir sonraki sorunun statusunu de donmeli
	paper = h.db_selectsingle(c.tblPapers, {"id": paper_id, "token": paper_token})
	if not paper:
		h.http404("Paper not found")
	test = h.db_selectsingle(c.tblTests, {"id": paper["test_id"]})
	if not test:
		h.http404("Test not found")
	question_dict = h.db_selectsingle(c.tblQuestions, {"test_id": test["id"], "id": question_id})
	if not question_dict:
		h.http404("Question not found")
	session = h.db_selectsingle(c.tblSessions, {"attendee_id": paper["attendee_id"], "state": "RUNNING", "token": session_token})
	if not session:
		h.http404("Invalid session info")
	old_choice = h.db_selectsingle(c.tblChoices, {"attendee_id": paper["attendee_id"], "paper_id": paper["id"], "question_id": question_id})
	new_choice = {"attendee_id": paper["attendee_id"], "paper_id": paper["id"], "session_id": session["id"], "question_id": question_id, "choice": choice, "completed_sec": int(time.time()), "is_deleted": 0}
	if old_choice:
		choice = {**old_choice, **new_choice}
	else:
		choice = new_choice
	if next_question_id is None:
		if "created_at" in choice:
			del choice["created_at"]
		if "updated_at" in choice:
			del choice["updated_at"]
		choice2 = h.db_insert(c.tblChoices, choice)
		return h.http200
	else:
		data = h.detailed_question(test["id"], paper["id"], next_question_id)
		print(data)
		return data
