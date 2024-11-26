import logging
from functools import wraps
from typing import Any, Awaitable, Callable

import aiohttp
import requests


def request_exceptions_handler(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to handle exceptions raised during making HTTP requests with 'requests' library

    Args:
        func (Callable[..., Any]): Function or method performing an http request

    Returns:
        Callable[..., Any]: Wrapper with exception handling
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except requests.HTTPError as e:
            logging.error(msg="Произошла HTTP ошибка при подключении", exc_info=e)
        except requests.RequestException as e:
            logging.error(msg="Ошибка при подключении", exc_info=e)

    return wrapper


def async_request_exceptions_handler(
    coro: Callable[..., Awaitable[Any]]
) -> Callable[..., Awaitable[Any]]:
    """Decorator to handle exceptions raised during making async HTTP requests with "aiohttp" library

    Args:
        coro (Callable[..., Awaitable[Any]]): Function or method performing an async http request

    Returns:
        Callable[..., Awaitable[Any]]: Awaitable wrapper with exception handling
    """

    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return await coro(*args, **kwargs)
        except aiohttp.ClientError as e:
            logging.error(msg="Произошла HTTP ошибка при подключении", exc_info=e)

    return wrapper
