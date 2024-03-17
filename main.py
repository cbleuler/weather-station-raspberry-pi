import logging
import asyncio
from pathlib import Path

from runner import Runner

logging.basicConfig(level=logging.INFO, format="%(asctime)s;%(levelname)s;%(message)s")


if __name__ == "__main__":
    runner = Runner.init_from_config_file(config_file=Path("config/dev.yaml"))
    asyncio.run(runner.run())
