from fastapi import FastAPI
import uvicorn

from src.app.routes import contacts
from src.app.routes import auth
# from src.app.routes import users

app = FastAPI()

app.include_router(contacts.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
# app.include_router(users.router, prefix="/api")

def main():
    uvicorn.run("src.app.main:app", host="127.0.0.1", port=8033, reload=True, workers=2)
    print("App started")
    