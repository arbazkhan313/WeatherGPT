from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.weather import router as weather_router
from app.api.location import router as location_router
from app.api.agent import router as agent_router
from app.api.forecast import router as forecast_router


app = FastAPI(
    title="WeatherGPT API",
    description="Agentic AI-powered weather intelligence system",
    version="1.0.0"
)


# =========================
# CORS CONFIGURATION
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# API ROUTES
# =========================

app.include_router(weather_router)
app.include_router(location_router)
app.include_router(agent_router)
app.include_router(forecast_router)


# =========================
# ROOT
# =========================

@app.get("/")
def root():
    return {
        "message": "WeatherGPT API is running!",
        "status": "success"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
