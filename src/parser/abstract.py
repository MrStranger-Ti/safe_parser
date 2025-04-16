import abc
import logging
from typing import Any, TypeVar

import requests
from requests import Response

from src import config
from src.parser.format.base import BaseFormatter

log = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseFormatter)


class XMLParser(abc.ABC):
    def __init__(
        self,
        url: str,
        params: dict[str, str] | None = None,
        headers: dict[str, str] | None = None,
        formatters_classes: list[T] | None = None,
    ):
        self.url: str = url
        self.params: dict[str, str] = params or {}
        self.headers: dict[str, str] = headers or {}
        self.formatters_classes: list[T] | None = (
            formatters_classes or config.DEFAULT_FORMATTERS
        )

    def get_response(self) -> Response:
        try:
            response = requests.get(
                url=self.url,
                params=self.params,
                headers=self.headers,
                timeout=5,
            )
            if response.status_code != 200:
                raise requests.exceptions.HTTPError(
                    f"Status code is not 200 ({response.status_code})"
                )

        except (requests.exceptions.Timeout, requests.exceptions.HTTPError) as exc:
            log.error(str(exc))
            raise exc

        except requests.exceptions.ConnectionError as exc:
            log.error(f"{str(exc)}. Maybe you set invalid URL?")
            raise exc

        return response

    def get_data(self) -> Any:
        response = self.get_response()
        xml = response.content
        parsed_data = self._parse(xml)
        return parsed_data

    def process_formatters(self, data: Any) -> Any:
        formated_data = {}
        for formatter_class in self.formatters_classes:
            formatter = formatter_class()
            formatter_data = formatter.format(data=data)
            formated_data.update(formatter_data)

        return formated_data or data

    @abc.abstractmethod
    def _parse(self, xml: bytes) -> Any:
        pass
