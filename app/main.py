from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .router import prediction_router

app = FastAPI()

# Router
app.include_router(prediction_router.router)

# Exception
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "Please try again later."},
    )

@app.middleware("http")
async def asgi_exception_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
    except Exception as exc:
        return JSONResponse(
            status_code=500,
            content={"message": "Please try again later."},
        )
    return response


@app.get("/")
def root():
    return {"message": "this is Rainfall Model Server"}
