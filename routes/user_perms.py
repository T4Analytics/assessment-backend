from typing import List
from fastapi import APIRouter


from models.user_perm import UserPerm


from modules.helpers import Helpers

h = Helpers()

router = APIRouter(prefix="/api/v1/user_perms", tags=["user_perms"])

@router.get("/", response_model=List[UserPerm])
async def read_user_perms():
	return h.listing_endpoint("user_perms")

@router.post("/", response_model=List[int])
async def create_user_perms(records: List[UserPerm]):
	retval = h.adding_endpoint("user_perms", records)
	return retval

@router.delete("/", response_model=List[int])
async def delete_user_perms(ids: List[int]):
	retval = h.deleting_endpoint("user_perms", ids)
	return retval
