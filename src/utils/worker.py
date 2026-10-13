import importlib.util
import sys
from argparse import ArgumentParser

import uvicorn

from config import settings


def _pick_loop() -> str:
    if sys.platform == "win32":
        if importlib.util.find_spec("winloop"):
            import winloop

            winloop.install()
        return "asyncio"
    return "uvloop" if importlib.util.find_spec("uvloop") else "asyncio"


def run_worker(
    fast_api_app_path: str,
    default_host: str | None = None,
    default_port: int | None = None,
):
    parser = ArgumentParser()
    parser.add_argument("--host", type=str, default=default_host or settings.server.host)
    parser.add_argument("--port", type=int, default=default_port or settings.server.port)
    parser.add_argument("--reload", action="store_true", default=False)

    args = parser.parse_args()

    uvicorn.run(
        fast_api_app_path,
        host=args.host,
        port=args.port,
        loop=_pick_loop(),
        reload=args.reload,
        reload_includes=[".env"] if args.reload else None,
    )
