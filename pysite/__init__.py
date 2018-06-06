import logging
import sys
from logging import Logger, StreamHandler

from logmatic import JsonFormatter

from pysite.constants import DEBUG_MODE

# region Logging
# Get the log level from environment

logging.TRACE = 5
logging.addLevelName(logging.TRACE, "TRACE")


def monkeypatch_trace(self, msg, *args, **kwargs):
    """
    Log 'msg % args' with severity 'TRACE'.

    To pass exception information, use the keyword argument exc_info with
    a true value, e.g.

    logger.trace("Houston, we have an %s", "interesting problem", exc_info=1)
    """
    if self.isEnabledFor(logging.TRACE):
        self._log(logging.TRACE, msg, args, **kwargs)


Logger.trace = monkeypatch_trace
log_level = logging.TRACE
logging_handlers = []

if DEBUG_MODE:
    logging_handlers.append(StreamHandler(stream=sys.stdout))

    json_handler = logging.FileHandler(filename="log.json", mode="w")
    json_handler.formatter = JsonFormatter()
    logging_handlers.append(json_handler)
else:
    logging_handlers.append(logging.FileHandler(filename="log.txt", mode="w"))

    json_handler = logging.StreamHandler(stream=sys.stdout)
    json_handler.formatter = JsonFormatter()
    logging_handlers.append(json_handler)

logging.basicConfig(
    format="%(asctime)s pd.beardfist.com Site: | %(name)35s | %(levelname)8s | %(message)s",
    datefmt="%b %d %H:%M:%S",
    level=log_level,
    handlers=logging_handlers
)
# endregion
