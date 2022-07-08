from fastapi import APIRouter
from models.choice import MinimalChoice
from modules.helpers import Helpers

h = Helpers()
router = APIRouter(prefix="/api/v1/choices", tags=["choices"])


