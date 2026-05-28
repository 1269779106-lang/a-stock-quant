"""MACD策略 - 基于quantitative-finance技能"""
import pandas as pd
from app.services.strategy.base_strategy import BaseStrategy, Signal


class MACDStrategy(BaseStrategy):
    """
    MACD策略

    策略逻辑：
    - MACD金叉（DIF上穿DEA），产生买入信号
    - MACD死叉（DIF下穿DEA），产生卖出信号
    - 结合MACD柱状图判断趋势强度

    参数：
    - fast_period: 快线周期 (默认12)
    - slow_period: 慢线周期 (默认26)
    - signal_period: 信号线周期 (默认9)
    """

    def __init__(self, params: dict = None):
        default_params = {
            "fast_period": 12,
            "slow_period": 26,
            "signal_period": 9
        }
        if params:
            default_params.update(params)

        super().__init__("MACD策略", default_params)

    def get_description(self) -> str:
        return f"""
        MACD策略
        - 快线周期: {self.params['fast_period']}
        - 慢线周期: {self.params['slow_period']}
        - 信号线周期: {self.params['signal_period']}
        - 买入条件: MACD金叉（DIF上穿DEA）
        - 卖出条件: MACD死叉（DIF下穿DEA）
        """

    def generate_signal(self, df: pd.DataFrame) -> pd.DataFrame:
        """生成交易信号"""
        fast_period = self.params['fast_period']
        slow_period = self.params['slow_period']
        signal_period = self.params['signal_period']

        # 计算EMA
        ema_fast = df['close'].ewm(span=fast_period, adjust=False).mean()
        ema_slow = df['close'].ewm(span=slow_period, adjust=False).mean()

        # 计算MACD
        df['macd_dif'] = ema_fast - ema_slow
        df['macd_dea'] = df['macd_dif'].ewm(span=signal_period, adjust=False).mean()
        df['macd_hist'] = 2 * (df['macd_dif'] - df['macd_dea'])

        # 初始化信号列
        df['signal'] = Signal.HOLD.value

        # 生成信号
        for i in range(1, len(df)):
            # MACD金叉 - 买入
            if (df['macd_dif'].iloc[i] > df['macd_dea'].iloc[i] and
                df['macd_dif'].iloc[i-1] <= df['macd_dea'].iloc[i-1]):
                df.iloc[i, df.columns.get_loc('signal')] = Signal.BUY.value

            # MACD死叉 - 卖出
            elif (df['macd_dif'].iloc[i] < df['macd_dea'].iloc[i] and
                  df['macd_dif'].iloc[i-1] >= df['macd_dea'].iloc[i-1]):
                df.iloc[i, df.columns.get_loc('signal')] = Signal.SELL.value

        return df
