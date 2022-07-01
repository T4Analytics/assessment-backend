from typing import List
from fastapi import APIRouter

from models.role import Role

from modules.helpers import Helpers

h = Helpers()

router = APIRouter(prefix="/api/v1/roles", tags=["roles"])


@router.get("/", response_model=List[Role])
async def read_roles():
	return h.listing_endpoint("roles")


@router.post("/", response_model=List[int])
async def create_roles(records: List[Role]):
	retval = h.adding_endpoint("roles", records)
	return retval


@router.delete("/", response_model=List[int])
async def delete_roles(ids: List[int]):
	retval = h.deleting_endpoint("roles", ids)
	return retval
