from typing import List
from fastapi import APIRouter

from models.user_role import UserRole

from modules.helpers import Helpers
h = Helpers()

router = APIRouter(prefix="/api/v1/user_roles", tags=["user_roles"])


@router.get("/", response_model=List[UserRole])
async def read_user_roles():
	return h.listing_endpoint("user_roles")


@router.post("/", response_model=List[int])
async def create_user_roles(records: List[UserRole]):
	retval = h.adding_endpoint("user_roles", records)
	return retval


@router.delete("/", response_model=List[int])
async def delete_user_roles(ids: List[int]):
	retval = h.deleting_endpoint("user_roles", ids)
	return retval
