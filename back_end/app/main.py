from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(
	title="LogMind API",
	description="Plataforma de análise de logs com IA",
	version="1.0.0"
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


@app.get("/")
async def root():
	return {
		"message": "LogMind API",
		"status": "online"
	}


@app.get("/health")
async def health_check():
	return {
		"status": "healthy"
	}

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )