import logging
from functools import wraps
from typing import Any, Callable


def bs4_exceptions_handler(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to handle exceptions raised during parsing html pages using
    'BeautifulSoup' library

    Args:
        func (Callable[..., Any]): Function or method performing parsing

    Returns:
        Callable[..., Any]: Wrapper with exception handling
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except TypeError as e:
            logging.error(msg="Invalid bs4 input type", exc_info=e)
        except AttributeError as e:
            logging.error(msg="Attribute accessing error", exc_info=e)

    return wrapper
