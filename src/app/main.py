from fastapi import FastAPI
import uvicorn

from src.app.routes import contacts

app = FastAPI()

app.include_router(contacts.router, prefix="/api")

def main():
    uvicorn.run("src.app.main:app", host="127.0.0.1", port=8033, reload=True, workers=2)
    print("App started")
    