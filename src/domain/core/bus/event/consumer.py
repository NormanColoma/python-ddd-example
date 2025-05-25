from abc import ABC, abstractmethod


class Consumer(ABC):
    @abstractmethod
    def __init__(self, topic):
        self.topic = topic

    @abstractmethod
    def consume(self):
        raise NotImplementedError("Method publish must be implemented")
