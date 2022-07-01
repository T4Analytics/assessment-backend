from models.base_model import BaseModel
from modules.enums import TestType
from sqlmodel import Field, Column, Enum


""" tests created by t4 """
class Test (BaseModel):
	typ: TestType = Field(sa_column=Column(Enum(TestType)))
	title: str
