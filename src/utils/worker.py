from argparse import ArgumentParser

import uvicorn


def run_worker(
    fast_api_app_path: str,
    default_host: str = "127.0.0.1",
    default_port: int = 8081,
):
    parser = ArgumentParser()
    parser.add_argument("--host", type=str, default=default_host, help="Enter host")
    parser.add_argument("--port", type=int, default=default_port, help="Enter port")
    parser.add_argument("--reload", action="store_true", default=False)

    args = parser.parse_args()

    uvicorn.run(
        fast_api_app_path,
        host=args.host,
        port=args.port,
        loop="uvloop",
        reload=args.reload,
        reload_includes=".env",
    )
