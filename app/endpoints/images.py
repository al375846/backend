from fastapi import APIRouter, File, UploadFile
import shutil
import os

router = APIRouter(prefix="/images",
                   tags=["Images"])


@router.post("")
async def upload_images(file: UploadFile = File(...)):
    path = os.getcwd() + "/app/files/" + file.filename
    with open(path, "wb") as filesave:
        shutil.copyfileobj(file.file, filesave)
    return {"filename": file.filename}
