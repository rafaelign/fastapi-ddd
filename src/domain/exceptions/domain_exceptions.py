class DomainException(Exception):
    """Exceção base para todos os erros de domínio."""
    pass

class DomainValidationError(DomainException):
    """Exceção lançada quando uma regra de validação de domínio é violada."""
    pass

class EntityNotFoundError(DomainException):
    """Exceção lançada quando uma entidade não é encontrada."""
    pass

class AuthenticationError(DomainException):
    """Exceção lançada quando há um erro de autenticação."""
    pass

class AuthorizationError(DomainException):
    """Exceção lançada quando há um erro de autorização."""
    pass