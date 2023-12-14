from abc import abstractmethod, ABC


class ApplicationCommand(ABC):
    @abstractmethod
    def getFields(self) -> dict: raise NotImplementedError
