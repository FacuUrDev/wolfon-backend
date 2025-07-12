from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.application.routers import cards, users

app = FastAPI(
    title="Wolfon Project API",
    description="API para gestionar tarjetas y usuarios.",
    version="0.1.0"
)

# --- INICIO: Configuración de CORS ---
# Define la lista de orígenes permitidos. En este caso, tu frontend de Vite.
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)
# --- FIN: Configuración de CORS ---

# Routers en la aplicación principal.
# Añade "prefijo" para que todas las rutas dentro de ese router
# empiecen con él (ej. /api/cards/some-id).
app.include_router(cards.router, prefix="/api/cards", tags=["Cards"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])


@app.get("/")
async def read_root():
    return {"message": "Welcome to the Wolfon API"}
