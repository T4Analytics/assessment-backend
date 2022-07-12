from typing import List
from fastapi import APIRouter
from modules.helpers import Helpers


h = Helpers()
router = APIRouter(prefix="/api/v1/attendees", tags=["attendees"])


@router.get("/", response_model=List)
async def read_attendees(customer_id=0):
	return h.listing_endpoint("attendees", additional_conds={"customer_id": customer_id})


@router.post("/", response_model=List)
async def create_attendees(records: List):
	exists = True
	token = ""
	while exists:
		token = h.randstr(8)
		rows = h.db_select("attendees", {"token": token})
		exists = len(rows) > 0
	for record in records:
		if "token" in record and record["token"] == "":
			del record["token"]
	retval = h.adding_endpoint("attendees", records, additional_fields={"token": token})
	return retval


@router.delete("/", response_model=List[int])
async def delete_attendees(ids: List[int]):
	retval = h.deleting_endpoint("attendees", ids)
	return retval
