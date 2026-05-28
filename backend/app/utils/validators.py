"""输入验证工具模块"""
import re
from typing import Optional


def validate_stock_code(stock_code: str) -> bool:
    """
    验证股票代码格式

    Args:
        stock_code: 股票代码

    Returns:
        bool: 是否有效
    """
    # A股代码格式：6位数字
    if not stock_code:
        return False
    return bool(re.match(r'^\d{6}$', stock_code))


def validate_date(date_str: Optional[str]) -> bool:
    """
    验证日期格式

    Args:
        date_str: 日期字符串 (YYYY-MM-DD)

    Returns:
        bool: 是否有效
    """
    if not date_str:
        return True  # 可选参数
    return bool(re.match(r'^\d{4}-\d{2}-\d{2}$', date_str))


def validate_period(period: str) -> bool:
    """
    验证K线周期

    Args:
        period: 周期类型

    Returns:
        bool: 是否有效
    """
    valid_periods = ["daily", "weekly", "monthly", "60min", "30min", "15min", "5min", "1min"]
    return period in valid_periods


def validate_adjust(adjust: str) -> bool:
    """
    验证复权类型

    Args:
        adjust: 复权类型

    Returns:
        bool: 是否有效
    """
    valid_adjusts = ["qfq", "hfq", ""]
    return adjust in valid_adjusts


def sanitize_input(text: str) -> str:
    """
    清理输入字符串，防止注入

    Args:
        text: 输入文本

    Returns:
        str: 清理后的文本
    """
    # 移除潜在危险字符
    dangerous_chars = [';', '--', "'", '"', '\\', '/', '*']
    result = text
    for char in dangerous_chars:
        result = result.replace(char, '')
    return result.strip()
