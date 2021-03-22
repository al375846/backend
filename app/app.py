from fastapi import FastAPI
from starlette.responses import RedirectResponse

from app.db.db import start_db, close_mongo_connection
from app.endpoints.dispositivos import router as router_dispositivos
from app.endpoints.establecimientos import router as router_establecimientos
from app.endpoints.gestion import router as router_gestion
from app.endpoints.security import router as router_security
from app.endpoints.images import router as router_images

app = FastAPI()

app.add_event_handler("startup", start_db)
app.add_event_handler("shutdown", close_mongo_connection)

app.include_router(router_dispositivos)
app.include_router(router_security)
app.include_router(router_establecimientos)
app.include_router(router_gestion)
app.include_router(router_images)


@app.get("/", include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse("docs")
