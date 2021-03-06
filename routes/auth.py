from typing import Dict
from fastapi import APIRouter
from modules.helpers import Helpers

h = Helpers()
router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/login", response_model=Dict)
async def auth_login(email: str, password: str):
	print(email, password)
	pass


@router.post("/remind", response_model=Dict)
async def auth_login(email: str):
	print(email)
	pass
