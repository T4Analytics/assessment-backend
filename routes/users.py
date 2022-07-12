from typing import List
from fastapi import APIRouter

from models.user import User

from modules.helpers import Helpers

h = Helpers()

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.get("/", response_model=List[User])
async def read_users(partner_id=0):
	return h.listing_endpoint("users", additional_conds={"partner_id": partner_id})


@router.post("/", response_model=List)
async def create_users(records: List[User]):
	retval = h.adding_endpoint("users", records)
	return retval


@router.delete("/", response_model=List[int])
async def delete_users(ids: List[int]):
	retval = h.deleting_endpoint("users", ids)
	return retval
