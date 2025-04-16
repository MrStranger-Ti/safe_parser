import abc
from typing import Any


class BaseFormatter(abc.ABC):
    @abc.abstractmethod
    def format(self, data: Any) -> Any:
        pass
