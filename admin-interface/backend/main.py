"""Main FastAPI application with Antidote dependency injection."""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from antidote import world

# Import config first to ensure .env is loaded
from config import AppConfig
from database import DatabaseService
# Import modular routes
from auth.routes import router as auth_router
from sources.routes import router as sources_router


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    config: AppConfig = world[AppConfig]
    
    app = FastAPI(
        title=config.title,
        version=config.version,
        description=config.description
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.server.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(auth_router)
    app.include_router(sources_router)
    
    return app


app = create_app()


@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    print("🚀 Starting Grundrisse Admin API...")
    
    # Double-check environment is loaded
    config: AppConfig = world[AppConfig]
    print(f"📋 App: {config.title} v{config.version}")
    print(f"🗄️ Database: {config.database.host}:{config.database.port}/{config.database.database}")
    print(f"🌐 Server: {config.server.host}:{config.server.port} (debug={config.server.debug})")
    
    # Initialize database
    db_service: DatabaseService = world[DatabaseService]
    await db_service.initialize()
    
    print("✅ Application startup complete!")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown."""
    db_service: DatabaseService = world[DatabaseService]
    await db_service.close()


@app.get("/")
async def root():
    """Root endpoint with API information."""
    config: AppConfig = world[AppConfig]
    return {
        "message": f"{config.title}",
        "version": config.version,
        "database": "EdgeDB (Gel)"
    }


if __name__ == "__main__":
    import uvicorn
    config: AppConfig = world[AppConfig]
    uvicorn.run(
        app, 
        host=config.server.host, 
        port=config.server.port,
        debug=config.server.debug
    )