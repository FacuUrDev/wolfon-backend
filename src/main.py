from fastapi import FastAPI

from src.application.routers import cards, users

app = FastAPI(
    title="Wolfon Project API",
    description="API para gestionar tarjetas y usuarios.",
    version="0.1.0"
)

# Routers en la aplicación principal.
# Añade "prefijo" para que todas las rutas dentro de ese router
# empiecen con él (ej. /api/cards/some-id).
app.include_router(cards.router, prefix="/api/cards", tags=["Cards"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])


@app.get("/")
async def read_root():
    return {"message": "Welcome to the Wolfon API"}
