from functools import wraps
from config.logger import logger


def log_call(func):
    @wraps(func)
    async def _wrapper(*args, **kwargs):
        logger.info(f"Calling {func.__name__} with args={args} kwargs={kwargs}")
        try:
            result = await func(*args, **kwargs)
            logger.info(f"{func.__name__} returned {result}")
            return result
        except Exception as e:
            logger.exception(f"Exception in {func.__name__}: {e}")
            raise

    return _wrapper
