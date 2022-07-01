from typing import List
from fastapi import APIRouter


from models.choice import Choice


from modules.helpers import Helpers

h = Helpers()

router = APIRouter(prefix="/api/v1/choices", tags=["choices"])

@router.get("/", response_model=List[Choice])
async def read_choices():
	return h.listing_endpoint("choices")

@router.post("/", response_model=List[int])
async def create_choices(records: List[Choice]):
	retval = h.adding_endpoint("choices", records)
	return retval

@router.delete("/", response_model=List[int])
async def delete_choices(ids: List[int]):
	retval = h.deleting_endpoint("choices", ids)
	return retval
