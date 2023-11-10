

from fastapi import FastAPI
from app.routes import user_router, test_router

app = FastAPI()

@app.get('/')
def health_check():
    return "API is running. Access docs http://127.0.0.1:8000/docs"

app.include_router(user_router)
app.include_router(test_router)
