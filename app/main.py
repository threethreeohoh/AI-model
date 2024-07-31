from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

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
        print(exec)
        return JSONResponse(
            status_code=500,
            content={"message": "Please try again later."},
        )
    return response

# Cors
origins = [
    "http://43.200.165.138:3000",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8080",
    "http://localhost:8000",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "this is Rainfall Model Server"}
