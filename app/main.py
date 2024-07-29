from fastapi import FastAPI

from .router import prediction_router

app = FastAPI()

app.include_router(prediction_router.router)

@app.get("/")
def root():
    return {"message": "this is Rainfall Model Server"}
