"""日志配置模块"""
import sys
from loguru import logger
from app.core.config import settings


def setup_logger():
    """配置日志系统"""

    # 移除默认处理器
    logger.remove()

    # 控制台输出
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="DEBUG" if settings.DEBUG else "INFO",
        colorize=True
    )

    # 文件输出 - 普通日志
    logger.add(
        f"{settings.DATA_DIR}/logs/app.log",
        rotation="10 MB",
        retention="30 days",
        compression="zip",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="INFO",
        encoding="utf-8"
    )

    # 文件输出 - 错误日志
    logger.add(
        f"{settings.DATA_DIR}/logs/error.log",
        rotation="10 MB",
        retention="30 days",
        compression="zip",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="ERROR",
        encoding="utf-8"
    )

    # 文件输出 - 交易日志
    logger.add(
        f"{settings.DATA_DIR}/logs/trading.log",
        rotation="1 day",
        retention="365 days",
        compression="zip",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="INFO",
        encoding="utf-8"
    )

    return logger


# 初始化日志
app_logger = setup_logger()
