"""技术指标计算服务"""
import pandas as pd
import numpy as np
from typing import Optional
from loguru import logger


class IndicatorService:
    """技术指标计算服务类"""

    def __init__(self):
        logger.info("初始化技术指标服务")

    def add_ma(self, df: pd.DataFrame, periods: list = [5, 10, 20, 60]) -> pd.DataFrame:
        """
        添加移动平均线

        Args:
            df: 包含close列的DataFrame
            periods: 均线周期列表

        Returns:
            DataFrame: 添加了MA列的DataFrame
        """
        for period in periods:
            df[f'ma{period}'] = df['close'].rolling(window=period).mean()
        return df

    def add_ema(self, df: pd.DataFrame, periods: list = [12, 26]) -> pd.DataFrame:
        """添加指数移动平均线"""
        for period in periods:
            df[f'ema{period}'] = df['close'].ewm(span=period, adjust=False).mean()
        return df

    def add_macd(self, df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
        """
        添加MACD指标

        Args:
            df: DataFrame
            fast: 快线周期
            slow: 慢线周期
            signal: 信号线周期

        Returns:
            DataFrame: 添加了MACD相关列的DataFrame
        """
        ema_fast = df['close'].ewm(span=fast, adjust=False).mean()
        ema_slow = df['close'].ewm(span=slow, adjust=False).mean()

        df['macd_dif'] = ema_fast - ema_slow
        df['macd_dea'] = df['macd_dif'].ewm(span=signal, adjust=False).mean()
        df['macd_hist'] = 2 * (df['macd_dif'] - df['macd_dea'])

        return df

    def add_rsi(self, df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
        """
        添加RSI指标

        Args:
            df: DataFrame
            period: RSI周期

        Returns:
            DataFrame: 添加了RSI列的DataFrame
        """
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

        rs = gain / loss
        df[f'rsi{period}'] = 100 - (100 / (1 + rs))

        return df

    def add_kdj(self, df: pd.DataFrame, n: int = 9, m1: int = 3, m2: int = 3) -> pd.DataFrame:
        """
        添加KDJ指标

        Args:
            df: DataFrame
            n: RSV周期
            m1: K值平滑系数
            m2: D值平滑系数

        Returns:
            DataFrame: 添加了KDJ列的DataFrame
        """
        low_n = df['low'].rolling(window=n).min()
        high_n = df['high'].rolling(window=n).max()

        rsv = (df['close'] - low_n) / (high_n - low_n) * 100

        df['kdj_k'] = rsv.ewm(com=m1-1, adjust=False).mean()
        df['kdj_d'] = df['kdj_k'].ewm(com=m2-1, adjust=False).mean()
        df['kdj_j'] = 3 * df['kdj_k'] - 2 * df['kdj_d']

        return df

    def add_bollinger(self, df: pd.DataFrame, period: int = 20, std_dev: int = 2) -> pd.DataFrame:
        """
        添加布林带指标

        Args:
            df: DataFrame
            period: 周期
            std_dev: 标准差倍数

        Returns:
            DataFrame: 添加了布林带列的DataFrame
        """
        df['boll_mid'] = df['close'].rolling(window=period).mean()
        std = df['close'].rolling(window=period).std()

        df['boll_upper'] = df['boll_mid'] + std_dev * std
        df['boll_lower'] = df['boll_mid'] - std_dev * std

        return df

    def add_volume_ma(self, df: pd.DataFrame, periods: list = [5, 10, 20]) -> pd.DataFrame:
        """添加成交量均线"""
        for period in periods:
            df[f'vol_ma{period}'] = df['volume'].rolling(window=period).mean()
        return df

    def add_atr(self, df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
        """
        添加ATR指标 (平均真实波幅)

        Args:
            df: DataFrame
            period: ATR周期

        Returns:
            DataFrame: 添加了ATR列的DataFrame
        """
        high_low = df['high'] - df['low']
        high_close = abs(df['high'] - df['close'].shift())
        low_close = abs(df['low'] - df['close'].shift())

        true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        df[f'atr{period}'] = true_range.rolling(window=period).mean()

        return df

    def add_obv(self, df: pd.DataFrame) -> pd.DataFrame:
        """添加OBV指标 (能量潮)"""
        obv = [0]
        for i in range(1, len(df)):
            if df['close'].iloc[i] > df['close'].iloc[i-1]:
                obv.append(obv[-1] + df['volume'].iloc[i])
            elif df['close'].iloc[i] < df['close'].iloc[i-1]:
                obv.append(obv[-1] - df['volume'].iloc[i])
            else:
                obv.append(obv[-1])

        df['obv'] = obv
        return df

    def add_volume_ratio(self, df: pd.DataFrame, period: int = 5) -> pd.DataFrame:
        """添加量比指标"""
        df['volume_ratio'] = df['volume'] / df['volume'].rolling(window=period).mean()
        return df

    def add_all_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """添加所有常用技术指标"""
        df = self.add_ma(df)
        df = self.add_ema(df)
        df = self.add_macd(df)
        df = self.add_rsi(df)
        df = self.add_kdj(df)
        df = self.add_bollinger(df)
        df = self.add_volume_ma(df)
        df = self.add_atr(df)
        df = self.add_obv(df)
        df = self.add_volume_ratio(df)
        return df


# 创建全局实例
indicator_service = IndicatorService()
