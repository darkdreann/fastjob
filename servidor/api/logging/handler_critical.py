import logging, logging.handlers
from api.logging.logging_config import FORMATTER
from api.utils.functions.env_config import CONFIG

EMAIL_HANDLER = logging.handlers.SMTPHandler(
    mailhost=(CONFIG.SMTP_SERVER, CONFIG.SMTP_PORT),
    fromaddr=CONFIG.SMTP_EMAIL,
    toaddrs=CONFIG.EMAIL_TO_SEND,
    subject=CONFIG.SUBJECT,
    credentials=(CONFIG.SMTP_EMAIL, CONFIG.SMTP_PASSWORD),
    secure=()
)

EMAIL_HANDLER.setLevel(logging.CRITICAL)
EMAIL_HANDLER.setFormatter(FORMATTER)
