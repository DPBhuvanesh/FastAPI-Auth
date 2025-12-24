from fastapi import FastAPI
from auth.router import router as auth_router
from users.router import router as user_router
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)

@app.get("/")
async def root():
    return {"message": "Hello FastAPI!"}


origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

