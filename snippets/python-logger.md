# Simple Python Logger

```py
import logging
import logging.handlers

def setup_logger(log_file, max_bytes, backup_count):
    logger = logging.getLogger('my_logger')
    logger.setLevel(logging.INFO)
    
    handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=max_bytes, backupCount=backup_count)
    
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    
    return logger

log_file = 'xxx.log'
max_bytes = 1024 * 1024  # 1MB
backup_count = 5

logger = setup_logger(log_file, max_bytes, backup_count)

logger.info("this is a test log")
```