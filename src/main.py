from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config.settings import get_settings
from src.presentation.api.error_handlers import add_exception_handlers
from src.presentation.api.routers.usuario_router import router as usuario_router

def create_application() -> FastAPI:
    settings = get_settings()
    
    app = FastAPI(
        title="FastAPI DDD Application",
        description="API desenvolvida com FastAPI seguindo os princípios de DDD",
        version="0.1.0",
        debug=settings.DEBUG
    )
    
    # Configuração CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Adicionar routers
    app.include_router(usuario_router, prefix="/api/v1")
    
    # Adicionar handlers de exceção
    add_exception_handlers(app)
    
    @app.get("/", tags=["Health"])
    async def health_check():
        return {"status": "ok", "message": "API is running"}
    
    return app

app = create_application()