"""动量突破策略 - 基于trading-skills的edge-strategy-designer"""
import pandas as pd
import numpy as np
from app.services.strategy.base_strategy import BaseStrategy, Signal


class MomentumBreakoutStrategy(BaseStrategy):
    """
    动量突破策略

    策略逻辑：
    - 价格突破N日高点，且成交量放大，产生买入信号
    - 价格跌破N日低点，或跌破移动平均线，产生卖出信号
    - 结合ATR进行动态止损

    参数：
    - breakout_period: 突破周期 (默认20)
    - volume_threshold: 成交量放大倍数 (默认1.5)
    - ma_period: 移动平均线周期 (默认20)
    - atr_period: ATR周期 (默认14)
    - atr_multiplier: ATR止损倍数 (默认2.0)
    """

    def __init__(self, params: dict = None):
        default_params = {
            "breakout_period": 20,
            "volume_threshold": 1.5,
            "ma_period": 20,
            "atr_period": 14,
            "atr_multiplier": 2.0
        }
        if params:
            default_params.update(params)

        super().__init__("动量突破策略", default_params)

    def get_description(self) -> str:
        return f"""
        动量突破策略
        - 突破周期: {self.params['breakout_period']}日
        - 成交量阈值: {self.params['volume_threshold']}倍
        - 均线周期: {self.params['ma_period']}日
        - ATR周期: {self.params['atr_period']}日
        - ATR止损倍数: {self.params['atr_multiplier']}
        - 买入条件: 价格突破N日高点 + 成交量放大
        - 卖出条件: 价格跌破N日低点 或 跌破均线
        """

    def generate_signal(self, df: pd.DataFrame) -> pd.DataFrame:
        """生成交易信号"""
        breakout_period = self.params['breakout_period']
        volume_threshold = self.params['volume_threshold']
        ma_period = self.params['ma_period']
        atr_period = self.params['atr_period']
        atr_multiplier = self.params['atr_multiplier']

        # 计算N日高点和低点
        df['high_n'] = df['high'].rolling(window=breakout_period).max()
        df['low_n'] = df['low'].rolling(window=breakout_period).min()

        # 计算移动平均线
        df['ma'] = df['close'].rolling(window=ma_period).mean()

        # 计算成交量均线
        df['vol_ma'] = df['volume'].rolling(window=breakout_period).mean()

        # 计算ATR
        high_low = df['high'] - df['low']
        high_close = abs(df['high'] - df['close'].shift())
        low_close = abs(df['low'] - df['close'].shift())
        true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        df['atr'] = true_range.rolling(window=atr_period).mean()

        # 初始化信号列
        df['signal'] = Signal.HOLD.value

        # 生成信号
        for i in range(1, len(df)):
            # 买入条件：价格突破N日高点 + 成交量放大
            if (df['close'].iloc[i] > df['high_n'].iloc[i-1] and
                df['volume'].iloc[i] > df['vol_ma'].iloc[i] * volume_threshold):
                df.iloc[i, df.columns.get_loc('signal')] = Signal.BUY.value

            # 卖出条件：价格跌破N日低点 或 跌破均线
            elif (df['close'].iloc[i] < df['low_n'].iloc[i-1] or
                  df['close'].iloc[i] < df['ma'].iloc[i]):
                df.iloc[i, df.columns.get_loc('signal')] = Signal.SELL.value

        return df
