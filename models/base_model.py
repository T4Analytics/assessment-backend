from datetime import datetime
from typing import Optional
from typing import Union
from sqlmodel import SQLModel, Field


class BaseModel(SQLModel, table=True):
    """ base record type """
    id: Optional[int] = Field(default=None, primary_key=True)
    is_deleted: Optional[int] = 0
    created_at: Union[datetime, None]
    updated_at: Union[datetime, None]

    class Config(SQLModel.Config):
        arbitrary_types_allowed = True
