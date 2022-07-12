from typing import List
from fastapi import APIRouter


from models.role_perm import RolePerm


from modules.helpers import Helpers

h = Helpers()
router = APIRouter(prefix="/api/v1/role_perms", tags=["role_perms"])


@router.get("/", response_model=List[RolePerm])
async def read_role_perms():
	return h.listing_endpoint("role_perms")


@router.post("/", response_model=List[int])
async def create_role_perms(records: List[RolePerm]):
	retval = h.adding_endpoint("role_perms", records)
	return retval


@router.delete("/", response_model=List[int])
async def delete_role_perms(ids: List[int]):
	retval = h.deleting_endpoint("role_perms", ids)
	return retval
