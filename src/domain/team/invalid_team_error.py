from src.domain.core.applicaton_error import ApplicationError


class InvalidTeamError(ApplicationError):
    def __init__(self, message):
        super().__init__(message)
