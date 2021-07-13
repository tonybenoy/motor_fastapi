from fastapi import FastAPI
from .routes import router
from .db import get_db_conn, close_db

app = FastAPI()
app.include_router(router)

app.add_event_handler("startup", get_db_conn)
app.add_event_handler("shutdown", close_db)


@app.get("/test")
async def test():
    return {
        "result": "success",
        "message": "It works!",
    }
