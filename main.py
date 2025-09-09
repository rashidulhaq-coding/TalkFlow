from fastapi import FastAPI
from app.routers import chat_api,auth_api

app = FastAPI()


app.include_router(chat_api.router,tags=["Chat"])
app.include_router(auth_api.auth_router,tags=["Authentication"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
    