from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from src.domain.exceptions.domain_exceptions import (
    DomainException,
    DomainValidationError,
    EntityNotFoundError,
    AuthenticationError,
    AuthorizationError
)

def add_exception_handlers(app: FastAPI):
    @app.exception_handler(DomainValidationError)
    async def domain_validation_exception_handler(request: Request, exc: DomainValidationError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(exc)}
        )
    
    @app.exception_handler(EntityNotFoundError)
    async def entity_not_found_exception_handler(request: Request, exc: EntityNotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(exc)}
        )
    
    @app.exception_handler(AuthenticationError)
    async def authentication_exception_handler(request: Request, exc: AuthenticationError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": str(exc)}
        )
    
    @app.exception_handler(AuthorizationError)
    async def authorization_exception_handler(request: Request, exc: AuthorizationError):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": str(exc)}
        )
    
    @app.exception_handler(DomainException)
    async def domain_exception_handler(request: Request, exc: DomainException):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": str(exc)}
        )