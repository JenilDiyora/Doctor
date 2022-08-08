from fastapi import FastAPI
from .view.doctor import router as DoctorRouter
import server.model.doctor 
from server.database import engine
from fastapi.staticfiles import StaticFiles
server.model.doctor.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.mount("/static", StaticFiles(directory="server"), name="static")

app.include_router(DoctorRouter, tags=["Doctor"], prefix="/Doctor")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this Patient registration app!"}