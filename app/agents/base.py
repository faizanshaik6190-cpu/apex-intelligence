from abc import ABC, abstractmethod

class BaseAgent(ABC):
    name: str = "BaseAgent"

    @abstractmethod
    def run(self, *args, **kwargs):
        raise NotImplementedError
