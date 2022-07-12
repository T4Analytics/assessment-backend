from typing import List
from fastapi import APIRouter


from models.session import Session


from modules.helpers import Helpers

h = Helpers()
router = APIRouter(prefix="/api/v1/sessions", tags=["sessions"])


@router.get("/", response_model=List[Session])
async def read_sessions():
	return h.listing_endpoint("sessions")


@router.post("/", response_model=List[int])
async def create_sessions(records: List[Session]):
	retval = h.adding_endpoint("sessions", records)
	return retval


@router.delete("/", response_model=List[int])
async def delete_sessions(ids: List[int]):
	retval = h.deleting_endpoint("sessions", ids)
	return retval
