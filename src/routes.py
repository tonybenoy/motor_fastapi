from typing import Any, Dict, List
from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.responses import JSONResponse

from .db import get_database
from .pydantic_models import AllClasses, AllStudents
from .utils import (
    create_aliased_response,
    get_student_details,
    get_student_grades,
    get_student_in_a_class,
    get_total_marks,
)

router = APIRouter()


@router.get("/students")
async def read_students(db: AsyncIOMotorClient = Depends(dependency=get_database)):
    data = []
    async for student in db["students"].find():
        data.append(student)
    return create_aliased_response(model=AllStudents(students=data))


@router.get("/student/{student_id}/classes")
async def read_student_classes(
    student_id: int, db: AsyncIOMotorClient = Depends(get_database)
):
    student = None
    async for doc in db["students"].aggregate(
        [
            {"$match": {"_id": student_id}},
            {
                "$lookup": {
                    "from": "grades",
                    "localField": "_id",
                    "foreignField": "student_id",
                    "as": "classes",
                }
            },
            {
                "$replaceRoot": {
                    "newRoot": {
                        "$mergeObjects": [{"$arrayElemAt": ["$students", 0]}, "$$ROOT"]
                    }
                }
            },
            {
                "$project": {
                    "classes.scores": 0,
                    "classes._id": 0,
                    "classes.student_id": 0,
                }
            },
        ]
    ):
        student = doc
    return JSONResponse(student if student else [])


@router.get("/student/{student_id}/performance")
async def read_student_performance(
    student_id: int, db: AsyncIOMotorClient = Depends(dependency=get_database)
):
    """{
        "student_id": integer,
        "student_name": string,
        "classes": [
            {"class_id": integer, "total_marks": integer},
            {"class_id": integer, "total_marks": integer},
        ],
    }"""
    student = await get_student_details(
        db=db,
        student_ids=[
            student_id,
        ],
    )
    grades = await get_student_grades(
        db=db,
        student_ids=[
            student_id,
        ],
    )
    resp = student[0].update({"classes": get_total_marks(data=grades, by="class_id")})
    return JSONResponse(resp)


@router.get("/classes")
async def read_classes(db: AsyncIOMotorClient = Depends(dependency=get_database)):
    classes = []
    async for doc in db["grades"].find({}, {"class_id": 1, "_id": 0}):
        classes.append(doc)
    return create_aliased_response(model=AllClasses(classes=classes))


@router.get("/class/{class_id}/students")
async def read_class_students(
    class_id: int, db: AsyncIOMotorClient = Depends(dependency=get_database)
):
    resp: Dict[str, Any] = {"class_id": class_id}
    students = await get_student_in_a_class(db=db, class_id=class_id)
    los = await get_student_details(db=db, student_ids=students)
    resp.update({"students": los})
    return JSONResponse(resp)


@router.get("/class/{class_id}/performance")
async def read_class_performance(class_id: str):
    """{
            "class_id": integer,
            "students": [
                    {
                            "student_id": integer,
                            "student_name": string,
                            "total_marks": integer
                    },
                    {
                            "student_id": integer,
                            "student_name": string,
                            "total_marks": integer
                    }
            ]
    }"""
    return {}


@router.get("/class/{class_id}/student/{student_id}")
@router.get("/student/{student_id}/class/{class_id}")
async def student_course(class_id: str, student_id: str):
    """
    {
            "class_id": integer,
            "students": [
                    {
                            "student_id": integer,
                            "student_name": string,
                            "details": [
                                    {
                                            "type": "exam",
                                            "marks": integer
                                    },
                                    {
                                            "type": "quiz",
                                            "marks": integer
                                    },
                                    {
                                            "type": "homework1",
                                            "marks": integer
                                    },
                                    {
                                            "type": "homework2",
                                            "marks": integer
                                    },
                                    {
                                            "type": "total",
                                            "marks": integer
                                    }
                            ],
                            "grade": string
                    },
                    {
                            "student_id": integer,
                            "student_name": string,
                            "details": [
                                    {
                                            "type": "exam",
                                            "marks": integer
                                    },
                                    {
                                            "type": "quiz",
                                            "marks": integer
                                    },
                                    {
                                            "type": "homework1",
                                            "marks": integer
                                    },
                                    {
                                            "type": "homework2",
                                            "marks": integer
                                    },
                                    {
                                            "type": "total",
                                            "marks": integer
                                    }
                            ],
                            "grade": string
                    }
            ]
    }
    """
    return {}
