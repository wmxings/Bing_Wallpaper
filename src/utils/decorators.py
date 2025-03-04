import time
import logging
from functools import wraps
from typing import Type, Tuple, Optional, Callable
from .exceptions import BingWallpaperError

logger = logging.getLogger(__name__)


def retry(
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    tries: int = 3,
    delay: float = 1,
    backoff: float = 2,
    logger: Optional[logging.Logger] = None,
) -> Callable:
    """
    重试装饰器
    :param exceptions: 需要捕获的异常类型
    :param tries: 最大重试次数
    :param delay: 初始延迟时间（秒）
    :param backoff: 延迟时间的增长因子
    :param logger: 日志记录器
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            _tries, _delay = tries, delay
            while _tries > 0:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    _tries -= 1
                    if _tries == 0:
                        raise BingWallpaperError(f"重试{tries}次后仍然失败: {str(e)}")

                    if logger:
                        logger.warning(
                            f"{func.__name__} 失败，{_tries}次重试剩余。错误: {str(e)}"
                        )

                    time.sleep(_delay)
                    _delay *= backoff
            return None
        return wrapper
    return decorator
