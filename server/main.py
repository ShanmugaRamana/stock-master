from fastapi import FastAPI
from core.database import engine
from models import user as user_model # Import to register models
from routes import auth

# Initialize Database Tables
user_model.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Stock Master API")

# Register Routes
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "Stock Master Server is Running (Modular Setup)"}