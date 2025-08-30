from fastapi import FastAPI
from app.routers import chat_api

app = FastAPI()


app.include_router(chat_api.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    