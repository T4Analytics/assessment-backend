from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class BaseModel(SQLModel, table=True):
    # """ base record type """
    id: Optional[int] = Field(default=None, primary_key=True)
    is_deleted: Optional[int] = 0
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config(SQLModel.Config):
        arbitrary_types_allowed = True
