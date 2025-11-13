# backend/app/core/logging_setup.py
import logging
import sys
from logging import StreamHandler, Formatter

def configure_logging():
    handler = StreamHandler(stream=sys.stdout)
    fmt = "%(asctime)s %(levelname)s %(name)s %(message)s"
    handler.setFormatter(Formatter(fmt))
    root = logging.getLogger()
    root.setLevel("INFO")
    # avoid duplicate handlers in reload scenarios
    if not any(isinstance(h, StreamHandler) for h in root.handlers):
        root.addHandler(handler)
    # uvicorn loggers
    logging.getLogger("uvicorn").handlers = [handler]
    logging.getLogger("uvicorn.error").handlers = [handler]
    logging.getLogger("uvicorn.access").handlers = [handler]
