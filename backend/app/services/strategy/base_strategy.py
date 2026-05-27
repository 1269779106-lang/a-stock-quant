"""策略基类"""
from abc import ABC, abstractmethod
import pandas as pd
from typing import Optional, Dict, List
from dataclasses import dataclass
from enum import Enum
from loguru import logger


class Signal(Enum):
    """交易信号"""
    BUY = 1       # 买入
    SELL = -1     # 卖出
    HOLD = 0      # 持有


@dataclass
class TradeOrder:
    """交易订单"""
    stock_code: str
    signal: Signal
    price: float
    volume: int
    timestamp: str
    strategy_name: str
    reason: str = ""


class BaseStrategy(ABC):
    """策略基类"""

    def __init__(self, name: str, params: dict = None):
        """
        初始化策略

        Args:
            name: 策略名称
            params: 策略参数
        """
        self.name = name
        self.params = params or {}
        self.positions = {}  # 持仓
        self.trades = []     # 交易记录
        logger.info(f"初始化策略: {name}")

    @abstractmethod
    def generate_signal(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        生成交易信号

        Args:
            df: 包含行情数据的DataFrame

        Returns:
            DataFrame: 添加了signal列的DataFrame
        """
        pass

    @abstractmethod
    def get_description(self) -> str:
        """获取策略描述"""
        pass

    def get_params(self) -> dict:
        """获取策略参数"""
        return self.params

    def set_params(self, params: dict):
        """设置策略参数"""
        self.params.update(params)

    def calculate_position_size(self, capital: float, price: float, risk_ratio: float = 0.1) -> int:
        """
        计算仓位大小

        Args:
            capital: 可用资金
            price: 股票价格
            risk_ratio: 风险比例

        Returns:
            int: 买入股数 (100的整数倍)
        """
        risk_amount = capital * risk_ratio
        shares = int(risk_amount / price / 100) * 100
        return max(shares, 100)

    def calculate_stop_loss(self, entry_price: float, atr: float, multiplier: float = 2.0) -> float:
        """
        计算止损价格

        Args:
            entry_price: 入场价格
            atr: ATR值
            multiplier: ATR倍数

        Returns:
            float: 止损价格
        """
        return entry_price - atr * multiplier

    def calculate_take_profit(self, entry_price: float, atr: float, multiplier: float = 3.0) -> float:
        """
        计算止盈价格

        Args:
            entry_price: 入场价格
            atr: ATR值
            multiplier: ATR倍数

        Returns:
            float: 止盈价格
        """
        return entry_price + atr * multiplier
