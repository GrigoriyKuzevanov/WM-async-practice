import asyncio
import logging
import time
from parser.app import *
from parser.core.config import settings

from aiohttp import ClientSession, ClientTimeout

aiohttp_timeout = ClientTimeout(total=settings.AIOHTTP_TIMEOUT_TOTAL)

logging.basicConfig(level=logging.INFO)


async def main() -> None:
    """Main parser function:
    1. Fetch urls for downloading bulletin files
    2. Download bulletin files in .xls format
    3. Parse downloaded .xls files with bs4
    4. Save parsed data to DB
    """

    logging.info(msg="Start fetching urls for downloading bulletins files")
    
    page_numbers_range = range(settings.START_PAGE, settings.END_PAGE + 1)
    
    async with ClientSession(timeout=aiohttp_timeout) as session:
        tasks = [asyncio.create_task(get_pages(i, session)) for i in page_numbers_range]
        pages = await asyncio.gather(*tasks)

    links = []
    for page in pages:
        links.extend(get_links_from_page(page))

    logging.info(msg="Start downloading bulletins files")
    
    async with ClientSession(timeout=aiohttp_timeout) as session:
        tasks = [
            asyncio.create_task(download_bulletins_xls(link, session)) for link in links
        ]
        await asyncio.gather(*tasks)

    logging.info(msg="Start parsing xls files")
    
    data = []
    for date, _ in links:
        data.append(parse_xls_bulletin_to_dict(date))

    logging.info(msg="Start saving data to database")
    
    tasks = [asyncio.create_task(save_bulletin_to_db(item)) for item in data]
    await asyncio.gather(*tasks)
