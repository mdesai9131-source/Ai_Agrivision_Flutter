from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.core.logging_config import setup_logging, logger
from app.api.prediction_routes import router as prediction_router
from app.services.predictor import predictor
from app.schemas.prediction_schema import HealthResponse

# Initialize logging
setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Production-grade Crop Disease Classification & Safe Farmer Guidance API",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception on {request.url.path}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred processing the request."
            }
        }
    )

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Service health check and model loading state."""
    return HealthResponse(
        status="healthy",
        model_loaded=predictor.is_model_loaded,
        version="1.0.0"
    )

# Include API v1 router
app.include_router(prediction_router, prefix=settings.API_V1_PREFIX, tags=["Crop Disease Prediction"])

@app.get("/", tags=["Root"])
async def root():
    return {
        "service": settings.PROJECT_NAME,
        "status": "online",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
