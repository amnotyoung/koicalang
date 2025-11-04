"""
FastAPI application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import conversation, voice, scenarios

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="음성 기반 크메르어 학습 서비스 - Voice-based Khmer language learning platform",
    version="0.1.0",
    debug=settings.DEBUG,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "message": "Koica Lang API",
        "status": "running",
        "version": "0.1.0",
        "supported_languages": settings.SUPPORTED_LANGUAGES,
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "environment": settings.APP_ENV,
    }


# Include routers
app.include_router(conversation.router, prefix="/api/v1/conversation", tags=["conversation"])
app.include_router(voice.router, prefix="/api/v1/voice", tags=["voice"])
app.include_router(scenarios.router, prefix="/api/v1/scenarios", tags=["scenarios"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
    )
