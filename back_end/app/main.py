import sys
import uvicorn

from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.domains.users.router import router as user_router
from app.domains.log_files.router import router as log_files_router

BACK_END_ROOT = Path(__file__).resolve().parent.parent
if str(BACK_END_ROOT) not in sys.path:
    sys.path.insert(0, str(BACK_END_ROOT))



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
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(log_files_router, prefix="/log_files", tags=["Log Files"])


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )