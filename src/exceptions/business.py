class WorldCupError(Exception):
    pass

class NotFoundError(WorldCupError):
    pass

class BusinessRuleError(WorldCupError):
    pass

class AuthenticationError(WorldCupError):
    pass

class AuthorizationError(WorldCupError):
    pass

class ConflictError(WorldCupError):
    pass

class ExternalApiError(WorldCupError):
    pass