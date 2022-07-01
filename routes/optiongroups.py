from typing import List
from fastapi import APIRouter


from models.optiongroup import OptionGroup


from modules.helpers import Helpers

h = Helpers()

router = APIRouter(prefix="/api/v1/optiongroups", tags=["optiongroups"])


@router.get("/", response_model=List[OptionGroup])
async def read_optiongroups():
	return h.listing_endpoint("optiongroups")


@router.post("/", response_model=List[int])
async def create_optiongroups(records: List[OptionGroup]):
	retval = h.adding_endpoint("optiongroups", records)
	return retval


@router.delete("/", response_model=List[int])
async def delete_optiongroups(ids:List[int]):
	retval = h.deleting_endpoint("optiongroups", ids)
	return retval
