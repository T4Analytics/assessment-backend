from typing import List
from fastapi import APIRouter


from models.customer_test import CustomerTest


from modules.helpers import Helpers

h = Helpers()

router = APIRouter(prefix="/api/v1/customer_tests", tags=["customer_tests"])

@router.get("/", response_model=List[CustomerTest])
async def read_customer_tests(customer_id=0):
	return h.listing_endpoint("customer_tests", additional_conds={"customer_id":customer_id})

@router.post("/", response_model=List)
async def create_customer_tests(records: List):
	retval = h.adding_endpoint("customer_tests", records)
	return retval

@router.delete("/", response_model=List[int])
async def delete_customer_tests(ids: List[int]):
	return h.deleting_endpoint("customer_tests", ids)
