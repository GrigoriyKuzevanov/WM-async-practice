from parser.core.config import settings
from parser.utils import (async_request_exceptions_handler,
                          bs4_exceptions_handler)

from aiohttp import ClientSession
from bs4 import BeautifulSoup


@bs4_exceptions_handler
def get_links_from_page(page_text: str, limit: int = 10) -> list[tuple[str, str]]:
    """Parses given HTML page and extracts 'limit' dates and links to
    download daily trade results. By default every trade results page
    on Spimex website contains 10 links to download.

    Args:
        page_text (str): Page content
        limit (int, optional): Limit to extract links. Defaults to 10.

    Returns:
        list[tuple[str, str]]: List of tuples in format (trading date, url to download bulletin)
    """

    results = []

    bs = BeautifulSoup(page_text, "html.parser")

    link_divs = bs.find_all("div", class_="accordeon-inner__item", limit=limit)

    if not link_divs:
        return results
    
    for div in link_divs:
        link_a = div.find("a", class_="accordeon-inner__item-title")
        date_span = div.find("span")

        if link_a and date_span:
            results.append((date_span.text, settings.BASE_URL + link_a.get("href")))

    return results


@async_request_exceptions_handler
async def get_pages(page_number: int, session: ClientSession) -> str:
    """Makes an async request to fetch HTML content from page with given number.
    Spimex website uses pagination to represent daily trade results, to fetch page
    result you must give page number parameter in format ?page=page-<page number>.

    Args:
        page_number (int): Page number to fetch trade results (1 - last results)
        session (ClientSession): aiohttp session object

    Returns:
        str: Page content
    """

    url = settings.TRADE_RESULTS_URL
    params = {"page": f"page-{page_number}"}

    async with session.get(url, params=params) as response:
        page_text = await response.text()

    return page_text
