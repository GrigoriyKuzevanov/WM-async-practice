import time
import logging
import asyncio
from parser.main import main

if __name__ == "__main__":
    start_time = time.perf_counter()
    asyncio.run(main())
    logging.info(msg=f"Working time: {time.perf_counter() - start_time}")
