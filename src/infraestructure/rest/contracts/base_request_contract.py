from typing import Protocol


class BaseRequestContract(Protocol):
    @staticmethod
    def contract() -> dict:
        pass
