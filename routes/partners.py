from typing import List
from fastapi import APIRouter


from models.partner import Partner


from modules.helpers import Helpers

h = Helpers()
router = APIRouter(prefix="/api/v1/partners", tags=["partners"])


@router.get("/", response_model=List[Partner])
async def read_partners():
	return h.listing_endpoint("partners")


@router.post("/", response_model=List)
async def create_partners(records: List[dict]):
	retval = h.adding_endpoint("partners", records)
	return retval


@router.delete("/", response_model=List[int])
async def delete_partners(ids: List[int]):
	retval = h.deleting_endpoint("partners", ids)
	return retval
