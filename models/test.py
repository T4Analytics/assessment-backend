from models.base_model import BaseModel
from modules.enums import TestType
from sqlmodel import Field, Column, Enum


class Test (BaseModel):
	""" tests created by t4 """
	typ: TestType = Field(sa_column=Column(Enum(TestType)))
	title: str
