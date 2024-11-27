import logging
from functools import wraps
from typing import Awaitable, Callable, TypeVar, ParamSpec

import aiohttp
import requests

R = TypeVar("R")
P = ParamSpec("P")


def request_exceptions_handler(func: Callable[P, R]) -> Callable[P, R | None]:
    """Decorator to handle exceptions raised during making HTTP requests with 'requests' library

    Args:
        func (Callable[P, R]): Function or method performing an http request

    Returns:
        Callable[P, R | None]: Wrapper with exception handling
    """

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | None:
        try:
            return func(*args, **kwargs)
        except requests.HTTPError as e:
            logging.error(msg="Произошла HTTP ошибка при подключении", exc_info=e)
        except requests.RequestException as e:
            logging.error(msg="Ошибка при подключении", exc_info=e)

    return wrapper


def async_request_exceptions_handler(
    coro: Callable[P, Awaitable[R]]
) -> Callable[P, Awaitable[R | None]]:
    """Decorator to handle exceptions raised during making async HTTP requests with "aiohttp" library

    Args:
        coro (Callable[P, Awaitable[R]]): Function or method performing an async http request

    Returns:
        Callable[P, Awaitable[R | None]]: Awaitable wrapper with exception handling
    """

    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | None:
        try:
            return await coro(*args, **kwargs)
        except aiohttp.ClientError as e:
            logging.error(msg="Произошла HTTP ошибка при подключении", exc_info=e)

    return wrapper
