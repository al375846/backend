from fastapi import FastAPI
from starlette.responses import RedirectResponse

from app.endpoints.dispositivos import router as router_dispositivos
from app.endpoints.establecimientos import router as router_establecimientos
from app.endpoints.security import router as router_security

app = FastAPI()

app.include_router(router_dispositivos)
app.include_router(router_security)
app.include_router(router_establecimientos)


@app.get("/", include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse("docs")
