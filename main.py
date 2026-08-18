from fastapi import FastAPI

from src.controllers.time_controller import router as time_router
from src.controllers.login_controller import router as login_router
from src.controllers.usuario_controller import router as usuario_router
from src.controllers.partida_controller import router as partida_router
from src.controllers.admin_controller import router as admin_router
from src.controllers.aposta_controller import router as aposta_router

from src.exceptions.business import (ExternalApiError,
                                     AuthorizationError,
                                     AuthenticationError,
                                     BusinessRuleError,
                                     ConflictError,
                                     NotFoundError)
from src.exceptions.handlers import (external_api_handler,
                                     authorization_handler,
                                     authentication_handler,
                                     business_rule_handler,
                                     conflict_handler,
                                     not_found_handler
                                     )

app = FastAPI()

app.include_router(login_router)
app.include_router(admin_router)
app.include_router(usuario_router)
app.include_router(aposta_router)
app.include_router(partida_router)
app.include_router(time_router)

app.add_exception_handler(ExternalApiError, external_api_handler)
app.add_exception_handler(AuthorizationError, authorization_handler)
app.add_exception_handler(AuthenticationError, authentication_handler)
app.add_exception_handler(BusinessRuleError, business_rule_handler)
app.add_exception_handler(ConflictError, conflict_handler)
app.add_exception_handler(NotFoundError, not_found_handler)