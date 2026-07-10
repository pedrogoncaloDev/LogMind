import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

BACK_END_ROOT = Path(__file__).resolve().parent.parent
if str(BACK_END_ROOT) not in sys.path:
    sys.path.insert(0, str(BACK_END_ROOT))

from app.routers.user_routes import router as user_router

app = FastAPI(
    title="LogMind API",
    description="Plataforma de análise de logs com IA",
    version="1.0.0",
    contact={
        "name": "Pedro Henrique Gonçalo de Oliveira",
        "email": "pedro.gonsalo939@gmail.com"
    },
    license_info={
        "name": "MIT",
    }
)

# CORS
app.add_middleware(
	CORSMiddleware,
	allow_origins=[
		"http://localhost:3000",
		"http://localhost:5173",
	],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


@app.get("/health")
async def health_check():
	return {
		"status": "healthy"
	}

# Rotas
# POST /users -> criar usuário
app.include_router(user_router, prefix="/users", tags=["Users"])


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )