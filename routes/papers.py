from typing import List
from fastapi import APIRouter


from models.paper import Paper


from modules.helpers import Helpers

h = Helpers()

router = APIRouter(prefix="/api/v1/papers", tags=["papers"])

@router.get("/", response_model=List[Paper])
async def read_papers():
	return h.listing_endpoint("papers")

@router.post("/", response_model=List[int])
async def create_papers(records: List[Paper]):
	retval = h.adding_endpoint("papers", records)
	return retval

@router.delete("/", response_model=List[int])
async def delete_papers(ids:List[int]):
	retval = h.deleting_endpoint("papers", ids)
	return retval
