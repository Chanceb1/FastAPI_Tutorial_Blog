from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.routers.blog_router import router as blog_router
from app.routers.user_router import router as user_router
from app.database import engine
from sqlmodel import SQLModel

app = FastAPI()

# create the database tables if they don't exist
SQLModel.metadata.create_all(engine)

origins = [
    "http://localhost:5000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# root endpoint
@app.get("/")
async def hello_world():
    return {"message": "Welcome to the FastAPI app!"}


# path parameter example
@app.post("/hello/{name}", tags=["Greetings"])
async def hello_name(name: str):
    return {"message": f"Hello, {name}!"}


# Example of another route with the same tag
@app.get("/goodbye/{name}", tags=["Greetings"])
async def goodbye(name: str):
    return {"message": f"Goodbye, {name}!"}


@app.post("/test", tags=["Query Parameters"])
async def test_endpoint(data: str | None = None):
    if data is None:
        return {"message": "No data received"}
    else:
        return {"message": f"Received data: {data}"}


# Example of a route with a different tag
@app.get("/status", tags=["System"])
async def system_status():
    return {"status": "operational"}


# include routers
app.include_router(blog_router)
app.include_router(user_router)


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="localhost", 
        port=5000,
        reload=True  # Enable hot reload
    )