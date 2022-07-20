import time
from typing import Optional
from fastapi import APIRouter

from models.paper import SimplePaper, DemoPaper, MinimalPaper
from models.question import DetailedQuestion
from modules.constants import Constants
from modules.enums import TestType, SessionState
from modules.helpers import Helpers

h = Helpers()
c = Constants()
router = APIRouter(prefix="/api/v1/assessments", tags=["assessments"])


@router.post("/demo", response_model=DemoPaper)
async def create_demo_paper(paper_type: TestType = "MB", allowed_sec: int = 1200):
	""" create new demo paper """
	partner = h.db_createorselect(c.tblPartners, {"title": "Demo"})
	customer = h.db_createorselect(c.tblCustomers, {"title": "Demo"})
	test = h.db_createorselect(c.tblTests, {"test_type": paper_type})
	attendee = h.db_createorselect(c.tblAttendees, {"identifier": "demo"})
	customertest = h.db_createorselect(c.tblCustomerTests, {"customer_id": customer["id"], "test_id": test["id"], "partner_id": partner["id"], "title": f"{paper_type} Demo", "timelimit_sec": 1200})
	token = "demo" + str(h.nowts(True))[-6:] + h.randstr(2)
	partnertest = h.db_createorselect(c.tblPartnerTests, {"test_id": test["id"], "partner_id": partner["id"], })
	paperdata = {"partner_id": partner["id"], "customer_id": customer["id"], "test_id": test["id"], "customertest_id": customertest["id"], "partnertest_id": partnertest["id"], "attendee_id": attendee["id"], "allowed_sec": allowed_sec, "token": token}
	paper = h.db_createorselect(c.tblPapers, paperdata)
	paper["session_token"] = h.create_attendee_session(paper)
	return DemoPaper(token=paper["token"], allowed_sec=paper["allowed_sec"], session_token=paper["session_token"])


@router.get("/papers/{paper_token}", response_model=SimplePaper)
async def get_paper_info(paper_token: str) -> SimplePaper:
	""" get info about specific paper """
	paper_dict = h.db_selectsingle(c.tblPapers, {"token": paper_token, "is_deleted": 0})
	test = h.db_selectsingle(c.tblTests, {"id": paper_dict["test_id"]})
	paper = SimplePaper(spent_sec=paper_dict["spent_sec"], allowed_sec=paper_dict["allowed_sec"], min_start_at=paper_dict["min_start_at"], max_end_at=paper_dict["max_end_at"], pretext=test["pretext"], question_count=0, choices={}, session_token="", is_completed=paper_dict["is_completed"], active_question_token=paper_dict["active_question_token"], started_at=paper_dict["started_at"], finished_at=paper_dict["finished_at"])
	paper.choices = h.questions_choices(paper_dict["test_id"], paper_dict["id"])
	paper.question_count = len(paper.choices)
	h.close_attendee_sessions(paper_dict["id"])
	paper.session_token = h.create_attendee_session(paper_dict)
	return paper


@router.post("/papers/{paper_token}/start")
async def start_paper(paper_token: str, session_token: str):
	# TODO: this function
	""" start the testing phase of a paper """
	paper_dict = h.db_selectsingle(c.tblPapers, {"token": paper_token, "is_deleted": 0})
	if not paper_dict:
		h.http(404, "Paper not found")
	if paper_dict["is_completed"] or paper_dict["finished_at"]:
		h.http(422, "Paper already completed")
	if paper_dict["started_at"] is not None:
		h.http(409, "Paper already started")
	session_dict = h.db_selectsingle(c.tblSessions, {"token": session_token, "paper_id": paper_dict["id"], "state": SessionState.RUNNING})
	if not session_dict:
		h.http(404, "Session not found or is not the active one")
	h.db_update(c.tblPapers, {"id": paper_dict["id"]}, {"started_at": h.now()})
	return h.succ()


@router.post("/papers/{paper_token}/tick", response_model=MinimalPaper)
async def tick_paper(paper_token: str, session_token: str) -> MinimalPaper:
	""" forward paper one more second """
	paper_dict = h.db_selectsingle(c.tblPapers, {"token": paper_token, "is_deleted": 0})
	if not paper_dict:
		h.http(404, "Paper not found")
	if paper_dict["is_completed"] or paper_dict["finished_at"]:
		h.http(422, "Paper already completed")
	if paper_dict["started_at"] is None:
		h.http(409, "Paper is not even started")
	session_dict = h.db_selectsingle(c.tblSessions, {"token": session_token, "paper_id": paper_dict["id"], "state": SessionState.RUNNING})
	if not session_dict:
		h.http(404, "Session not found or is not the active one")
	newstate = SessionState.RUNNING
	if paper_dict["spent_sec"] >= paper_dict["allowed_sec"]:
		newstate = SessionState.CLOSED
	if newstate == SessionState.CLOSED:
		h.db_update(c.tblPapers, {"id": paper_dict["id"]}, {"finished_at": h.now(), "spent_sec": paper_dict["spent_sec"]+1})
		h.db_update(c.tblSessions, {"id": session_dict["id"]}, {"finished_at": h.now(), "spent_sec": session_dict["spent_sec"]+1, "state": newstate})
	else:
		h.db_update(c.tblPapers, {"id": paper_dict["id"]}, {"spent_sec": paper_dict["spent_sec"]+1})
		h.db_update(c.tblSessions, {"id": session_dict["id"]}, {"spent_sec": session_dict["spent_sec"]+1, "state": newstate})
	paper = MinimalPaper(token=paper_token, spent_sec=paper_dict["spent_sec"], allowed_sec=paper_dict["allowed_sec"], state=newstate)
	return paper


@router.post("/papers/{paper_token}/end")
async def finish_paper(paper_token: str, session_token: str):
	""" finish the testing phase of a paper """
	paper_dict = h.db_selectsingle(c.tblPapers, {"token": paper_token, "is_deleted": 0})
	if not paper_dict:
		h.http(404, "Paper not found")
	if paper_dict["is_completed"] or paper_dict["finished_at"]:
		h.http(422, "Paper already completed")
	if paper_dict["started_at"] is None:
		h.http(409, "Paper is not even started")
	session_dict = h.db_selectsingle(c.tblSessions, {"token": session_token, "paper_id": paper_dict["id"], "state": SessionState.RUNNING})
	if not session_dict:
		h.http(404, "Session not found or is not the active one")
	h.db_update(c.tblPapers, {"id": paper_dict["id"]}, {"finished_at": h.now()})
	h.db_update(c.tblSessions, {"id": session_dict["id"]}, {"finished_at": h.now(), "state": SessionState.CLOSED})
	return h.succ()


@router.get("/papers/{paper_token}/questions/{question_token}", response_model=DetailedQuestion)
async def get_question_in_paper(paper_token: str, question_token: str) -> DetailedQuestion:
	""" get the question and the options in a question of a specific paper """
	paper = h.db_selectsingle(c.tblPapers, {"token": paper_token, "is_deleted": 0})
	if not paper:
		h.http(404, "Paper not found")
	if paper["is_completed"]:
		h.http(422, "Paper already completed")
	test = h.db_selectsingle(c.tblTests, {"id": paper["test_id"]})
	if not test:
		h.http(404, "Test not found")
	return h.detailed_question(test["id"], paper["id"], question_token)


@router.post("/{paper_token}/questions/{question_token}", response_model=DetailedQuestion)
async def save_answer_to_question(paper_token: str, question_token: str, choice: int, session_token: str, next_question_token: Optional[str] = None, is_completed: Optional[int] = None):
	""" save user's answer to a question """
	paper = h.db_selectsingle(c.tblPapers, {"token": paper_token, "is_deleted": 0})
	if not paper:
		h.http(404, "Paper not found")
	if paper["is_completed"]:
		h.http(422, "Paper already completed")
	test = h.db_selectsingle(c.tblTests, {"id": paper["test_id"]})
	if not test:
		h.http(404, "Test not found")
	question_dict = h.db_selectsingle(c.tblQuestions, {"test_id": test["id"], "token": question_token, "is_deleted": 0})
	if not question_dict:
		h.http(404, "Question not found")
	session = h.db_selectsingle(c.tblSessions, {"attendee_id": paper["attendee_id"], "state": "RUNNING", "token": session_token})
	if not session:
		h.http(404, "Invalid session info")
	old_choice = h.db_selectsingle(c.tblChoices, {"attendee_id": paper["attendee_id"], "paper_id": paper["id"], "question_id": question_dict["id"]})
	new_choice = {"attendee_id": paper["attendee_id"], "paper_id": paper["id"], "session_id": session["id"], "question_id": question_dict["id"], "choice": choice, "completed_sec": int(time.time()), "is_deleted": 0}
	if old_choice:
		choice = {**old_choice, **new_choice}
	else:
		choice = new_choice
	if "created_at" in choice:
		del choice["created_at"]
	if "updated_at" in choice:
		del choice["updated_at"]
	h.db_insert(c.tblChoices, choice)
	update_dict = {}
	if next_question_token is not None:
		update_dict["active_question_token"] = next_question_token
	if is_completed is not None:
		update_dict["is_completed"] = is_completed
	if update_dict:
		h.db_update(c.tblPapers, {"token": paper_token, "is_deleted": 0}, update_dict)
	if next_question_token is None:
		return h.detailed_question(test["id"], paper["id"], question_token)
	else:
		return h.detailed_question(test["id"], paper["id"], next_question_token)
