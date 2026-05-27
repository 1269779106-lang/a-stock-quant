"""双均线策略"""
import pandas as pd
from app.services.strategy.base_strategy import BaseStrategy, Signal


class DualMAStrategy(BaseStrategy):
    """
    双均线策略

    策略逻辑：
    - 快线上穿慢线，产生买入信号
    - 快线下穿慢线，产生卖出信号

    参数：
    - fast_period: 快线周期 (默认5)
    - slow_period: 慢线周期 (默认20)
    """

    def __init__(self, params: dict = None):
        default_params = {
            "fast_period": 5,
            "slow_period": 20
        }
        if params:
            default_params.update(params)

        super().__init__("双均线策略", default_params)

    def get_description(self) -> str:
        return f"""
        双均线策略
        - 快线周期: {self.params['fast_period']}
        - 慢线周期: {self.params['slow_period']}
        - 买入条件: 快线上穿慢线
        - 卖出条件: 快线下穿慢线
        """

    def generate_signal(self, df: pd.DataFrame) -> pd.DataFrame:
        """生成交易信号"""
        fast_period = self.params['fast_period']
        slow_period = self.params['slow_period']

        # 计算均线
        df['ma_fast'] = df['close'].rolling(window=fast_period).mean()
        df['ma_slow'] = df['close'].rolling(window=slow_period).mean()

        # 初始化信号列
        df['signal'] = Signal.HOLD.value

        # 生成信号
        for i in range(1, len(df)):
            # 快线上穿慢线 - 买入
            if (df['ma_fast'].iloc[i] > df['ma_slow'].iloc[i] and
                df['ma_fast'].iloc[i-1] <= df['ma_slow'].iloc[i-1]):
                df.iloc[i, df.columns.get_loc('signal')] = Signal.BUY.value

            # 快线下穿慢线 - 卖出
            elif (df['ma_fast'].iloc[i] < df['ma_slow'].iloc[i] and
                  df['ma_fast'].iloc[i-1] >= df['ma_slow'].iloc[i-1]):
                df.iloc[i, df.columns.get_loc('signal')] = Signal.SELL.value

        return df
