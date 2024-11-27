import logging
from functools import wraps
from typing import Callable, TypeVar, ParamSpec

R = TypeVar("R")
P = ParamSpec("P")


def bs4_exceptions_handler(func: Callable[P, R]) -> Callable[P, R | None]:
    """Decorator to handle exceptions raised during parsing html pages using
    'BeautifulSoup' library

    Args:
        func (Callable[P, R]): Function or method performing parsing

    Returns:
        Callable[P, R | None]: Wrapper with exception handling
    """

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | None:
        try:
            return func(*args, **kwargs)
        except TypeError as e:
            logging.error(msg="Invalid bs4 input type", exc_info=e)
        except AttributeError as e:
            logging.error(msg="Attribute accessing error", exc_info=e)

    return wrapper
