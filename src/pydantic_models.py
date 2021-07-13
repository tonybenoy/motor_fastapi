from typing import List
from bson import ObjectId
from pydantic import BaseModel, Field
from decimal import Decimal


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class StudentModel(BaseModel):
    student_id: int = Field(..., alias="_id")
    student_name: str = Field(..., alias="name")


class AllStudents(BaseModel):
    students: List[StudentModel]


class GradeModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    student_id: int = Field(...)
    scores: List = Field(...)
    class_id: int = Field(...)


class TypeModel(BaseModel):
    type: str = Field(...)
    score: Decimal = Field(...)


class ClassModel(BaseModel):
    class_id: int = Field(...)


class AllClasses(BaseModel):
    classes: List[ClassModel] = Field(...)


class StudentClasses(StudentModel):
    classes: List[ClassModel] = Field(...)
