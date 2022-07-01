from typing import List
from fastapi import APIRouter


from models.partner_test import PartnerTest


from modules.helpers import Helpers

h = Helpers()

router = APIRouter(prefix="/api/v1/partner_tests", tags=["partner_tests"])

@router.get("/", response_model=List[PartnerTest])
async def read_partner_tests(partner_id=0):
	return h.listing_endpoint("partner_tests", additional_conds={"partner_id":partner_id})

@router.post("/", response_model=List)
async def create_partner_tests(records: List):
	retval = h.adding_endpoint("partner_tests", records)
	return retval

@router.delete("/", response_model=List[int])
async def delete_partner_tests(ids: List[int]):
	return h.deleting_endpoint("partner_tests", ids)
