import uvicorn
import logging.config
from dotenv import load_dotenv
import os

try:
    load_dotenv("app/.env")
except:
    raise FileNotFoundError("Archivo .env no encontrado.")

LOG_PATH_WINDOWS = os.getenv('LOG_PATH_WINDOWS')
path = os.path.join(LOG_PATH_WINDOWS, "fastjob", "uvicorn.log")

config = logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    },
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "formatter": "default",
            "level": "INFO",
            "filename": path
        }
    },
    "loggers": {
        "uvicorn": {
            "handlers": ["file"],
            "level": "INFO"
        }
    }
})

if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=False, log_level="info", log_config=config)