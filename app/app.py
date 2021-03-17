from odmantic import ObjectId
from app.models.sugerencia import Sugerencia
from fastapi import FastAPI
import datetime
from app.models.notificacion import Notificacion
from odmantic import AIOEngine

app = FastAPI()
engine = AIOEngine()

@app.get("/")
async def index():
    
    n = Notificacion(fechaActivacion = datetime.datetime.utcnow(),
                    contenido="La has liado chaval",
                    leido = False,
                    imagen="https://www.google.com",
                    id = ObjectId())

    await engine.save(n)

    return {"Notificacion":await engine.find(Notificacion, Notificacion.leido == False)}