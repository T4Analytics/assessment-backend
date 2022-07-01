from typing import List
from fastapi import APIRouter


from models.question import Question


from modules.helpers import Helpers

h = Helpers()

router = APIRouter(prefix="/api/v1/questions", tags=["questions"])

@router.get("/", response_model=List)
async def read_questions():
	return h.listing_endpoint("questions")

@router.post("/", response_model=List)
async def create_questions(records: List):
	return h.adding_endpoint("questions", records)

@router.delete("/", response_model=List[int])
async def delete_questions(ids:List[int]):
	return h.deleting_endpoint("questions", ids)
