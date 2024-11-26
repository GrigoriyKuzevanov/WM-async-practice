import logging
import os
from parser.core.config import settings
from parser.utils import async_request_exceptions_handler

import aiofiles
import aiofiles.os
from aiohttp import ClientSession


@async_request_exceptions_handler
async def download_bulletins_xls(
    bulletin_link: tuple[str, str], session: ClientSession
) -> None:
    """Download bulletin files by given link and save into <date-of-bulletin>.xls file
    to directory specified in project settings.

    Args:
        bulletin_link (tuple[str, str]): Tuple containing date of bulletin and link to download file
        session (ClientSession): aiohttp ClientSession object
    """

    os.makedirs(settings.DOWNLOAD_DIR, exist_ok=True)

    date, link = bulletin_link
    filename = f"{settings.DOWNLOAD_DIR}/{date}.xls"

    async with session.get(link) as response:
        response.raise_for_status()

        if response.status == 200:
            try:
                async with aiofiles.open(filename, "wb") as f:
                    await f.write(await response.read())
            except OSError as e:
                logging.error(msg="Error during saving file", exc_info=e)
