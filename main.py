#main.py
from fastapi import FastAPI
from app.core.database import engine, Base
from app.routers import spy_cats, missions, targets

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Spy Cat Agency API",
    version="1.0.0",
    description="A comprehensive CRUD application for managing spy cats, missions, and targets"
)

app.include_router(spy_cats.router)
app.include_router(missions.router)
app.include_router(targets.router)

@app.get("/")
def root():
    return {"message": "Welcome to Spy Cat Agency API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
