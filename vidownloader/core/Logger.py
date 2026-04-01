import logging
import warnings
from datetime import datetime

from vidownloader.core.Constants import Paths


class FileHandler(logging.FileHandler):
    def __init__(self, filename, *args, **kwargs):
        kwargs["encoding"] = "utf-8"
        super().__init__(filename, *args, **kwargs)

    def emit(self, record):
        try:
            msg = self.format(record)

            if hasattr(self.stream, "write"):
                self.stream.write(msg + self.terminator)
            else:
                self.stream.write(
                    (msg + self.terminator).encode("utf-8", errors="replace")
                )

            self.flush()
        except UnicodeEncodeError as e:
            try:
                sanitized_msg = (
                    self.format(record)
                    .encode("ascii", errors="replace")
                    .decode("ascii")
                )
                self.stream.write(
                    f"[Unicode Error in Log Message - Original error: {str(e)}] {sanitized_msg}"
                    + self.terminator
                )
                self.flush()
            except Exception:
                self.handleError(record)
        except Exception:
            self.handleError(record)


class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_file = Paths.LOGS / f"log_{timestamp}.log"

        log_file.parent.mkdir(parents=True, exist_ok=True)

        file_handler = FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)

        if hasattr(stream_handler.stream, "reconfigure"):
            try:
                stream_handler.stream.reconfigure(encoding="utf-8")
            except Exception:
                pass

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)

        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

        logging.basicConfig(
            level=logging.DEBUG, handlers=[file_handler, stream_handler]
        )
        warnings.showwarning = self.log_warning

    def log_warning(self, message, category, filename, lineno, file=None, line=None):
        logger = logging.getLogger("root")
        logger.warning("%s:%s: %s: %s", filename, lineno, category.__name__, message)

    def get_logger(self, class_name):
        return logging.getLogger(class_name)


get_logger = Logger().get_logger
