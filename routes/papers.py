from typing import Dict
from fastapi import APIRouter
from models.paper import SimplePaper, DemoPaper
from models.question import DetailedQuestion
from modules.constants import Constants
from modules.enums import TestType
from modules.helpers import Helpers

h = Helpers()
c = Constants()
router = APIRouter(prefix="/api/v1/papers", tags=["papers"])


@router.post("/demo", response_model=DemoPaper)
async def create_demo_paper(typ: TestType = "MB"):
	""" create new demo paper """
	partner = h.db_createorselect(c.tblPartners, {"title": "Demo"})
	customer = h.db_createorselect(c.tblCustomers, {"title": "Demo"})
	test = h.db_createorselect(c.tblTests, {"typ": typ})
	attendee = h.db_createorselect(c.tblAttendees, {"identifier": "demo"})
	customertest = h.db_createorselect(c.tblCustomerTests, {"customer_id": customer["id"], "test_id": test["id"], "partner_id": partner["id"], "title": f"{typ} Demo", "timelimit_sec": 1200})
	partnertest = h.db_createorselect(c.tblPartnerTests, {"test_id": test["id"], "partner_id": partner["id"], })
	paperdata = {"partner_id": partner["id"], "customer_id": customer["id"], "test_id": test["id"], "customertest_id": customertest["id"], "partnertest_id": partnertest["id"], "attendee_id": attendee["id"], "allowed_sec": 1200, "token": "demo"}
	paper = h.db_createorselect(c.tblPapers, paperdata)
	return DemoPaper(id=paper["id"], token=paper["token"], allowed_sec=paper["allowed_sec"])


@router.get("/{paperid}", response_model=SimplePaper)
async def get_paper_info(paperid: int, papertoken: str):
	""" get info about specific paper """
	record = h.db_selectsingle(c.tblPapers, {"id": paperid, "token": papertoken})
	test = h.db_selectsingle(c.tblTests, {"id": record["test_id"]})
	paper = SimplePaper(spent_sec=record["spent_sec"], allowed_sec=record["allowed_sec"], min_start_at=record["min_start_at"], max_end_at=record["max_end_at"], pretext=test["pretext"], question_count=0, questions=[])
	paper.questions = h.field2tuple(h.db_select(c.tblQuestions, {"test_id": record["test_id"]}))
	paper.question_count = len(paper.questions)
	print(paper)
	return paper


@router.get("/{paperid}/questions/{questionid}", response_model=DetailedQuestion)
async def get_question_in_paper(paperid: int, questionid: int, choice: int) -> Dict:
	""" save user's answer to a question """
	pass


@router.post("/{paperid}/questions/{questionid}", response_model=Dict)
async def save_answer_to_question(paperid: int, questionid: int, choice: int) -> Dict:
	""" save user's answer to a question """
	pass
