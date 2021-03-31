from fastapi import APIRouter, File, UploadFile
import shutil
import os

router = APIRouter(prefix="/notificaciones",
                   tags=["notificaciones"])


@router.post("/new")
async def generate_notification(file: UploadFile = File(...)):
    path = os.getcwd() + "/app/files/" + file.filename
    with open(path, "wb") as filesave:
        shutil.copyfileobj(file.file, filesave)
    return {"filename": file.filename}