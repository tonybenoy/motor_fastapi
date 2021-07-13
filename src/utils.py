from typing import List
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from starlette.responses import JSONResponse


def create_aliased_response(model: BaseModel, by_alias: bool = False) -> JSONResponse:
    return JSONResponse(content=jsonable_encoder(obj=model, by_alias=by_alias))


async def get_students_in(db: AsyncIOMotorClient, student_ids: List[int]):
    return [
        {"student_id": stu["_id"], "student_name": stu["name"]}
        async for stu in db["sample_training"]["students"].find(
            {"_id": {"$in": student_ids}}
        )
    ]


async def get_student_ids(db: AsyncIOMotorClient, class_id: int):
    return [
        doc["student_id"]
        async for doc in db["sample_training"]["grades"].find(
            {"class_id": class_id}, {"student_id": 1, "_id": 0}
        )
    ]
