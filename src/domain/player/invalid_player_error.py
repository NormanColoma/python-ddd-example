from src.domain.core.applicaton_error import ApplicationError


class InvalidPlayerError(ApplicationError):
    def __init__(self, message):
        super().__init__(message)
