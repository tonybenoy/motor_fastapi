from itertools import groupby
from typing import Any, Dict, List, Optional

from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from starlette.responses import JSONResponse


def create_aliased_response(model: BaseModel, by_alias: bool = False) -> JSONResponse:
    return JSONResponse(content=jsonable_encoder(obj=model, by_alias=by_alias))


async def get_student_details(
    db: AsyncIOMotorClient, student_ids: List[int]
) -> List[Dict[str, Any]]:
    return [
        {"student_id": stu["_id"], "student_name": stu["name"]}
        async for stu in db["students"].find({"_id": {"$in": student_ids}})
    ]


async def get_student_in_a_class(db: AsyncIOMotorClient, class_id: int) -> List[int]:
    return [
        doc["student_id"]
        async for doc in db["grades"].find(
            {"class_id": class_id}, {"student_id": 1, "_id": 0}
        )
    ]


async def get_student_grades(
    db: AsyncIOMotorClient, student_ids: List[int], class_id: Optional[int] = None
) -> List[Dict[str, Any]]:
    filters: Dict[str, Any] = (
        {"student_id": {"$in": student_ids}}
        if not class_id
        else {"student_id": {"$in": student_ids}, "class_id": class_id}
    )
    return [stu async for stu in db["grades"].find(filters)]


def get_total_marks(data: List[Dict[str, Any]], by: str) -> List[Dict[str, int]]:
    resp = []
    for key, value in groupby(data, lambda x: x[by]):
        total = 0
        for k in value:
            for item in k["scores"]:
                total = total + int(item["score"])
        resp.append({by: key, "total_marks": total})
    return resp
