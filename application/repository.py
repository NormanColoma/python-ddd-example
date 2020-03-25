from abc import abstractmethod


class Repository:
    @abstractmethod
    def save(self) -> str: raise NotImplementedError
