from fastapi import APIRouter
from modules.helpers import Helpers

h = Helpers()
router = APIRouter(prefix="/api/v1/questions", tags=["questions"])
