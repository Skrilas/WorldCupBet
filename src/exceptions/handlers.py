from fastapi import Request
from fastapi.responses import JSONResponse

from src.exceptions.business import (
    NotFoundError,
    ConflictError,
    BusinessRuleError,
    AuthenticationError,
    AuthorizationError,
    ExternalApiError,
)


def not_found_handler(
    request: Request,
    exc: NotFoundError
):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)}
    )


def conflict_handler(
    request: Request,
    exc: ConflictError
):
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)}
    )


def business_rule_handler(
    request: Request,
    exc: BusinessRuleError
):
    return JSONResponse(
        status_code=422,
        content={"detail": str(exc)}
    )


def authentication_handler(
    request: Request,
    exc: AuthenticationError
):
    return JSONResponse(
        status_code=401,
        content={"detail": str(exc)}
    )


def authorization_handler(
    request: Request,
    exc: AuthorizationError
):
    return JSONResponse(
        status_code=403,
        content={"detail": str(exc)}
    )


def external_api_handler(
    request: Request,
    exc: ExternalApiError
):
    return JSONResponse(
        status_code=502,
        content={"detail": str(exc)}
    )