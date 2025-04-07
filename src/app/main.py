from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from src.app.routes import contacts
from src.app.routes import auth
# from src.app.routes import users

app = FastAPI()

origins = [
    "http://127.0.0.1:8033",
    "http://localhost:8033",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(contacts.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
# app.include_router(users.router, prefix="/api")

def main():
    uvicorn.run("src.app.main:app", host="127.0.0.1", port=8000, reload=True, workers=2)
    print("App started")
    