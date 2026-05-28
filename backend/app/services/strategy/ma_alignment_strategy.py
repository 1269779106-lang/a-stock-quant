"""均线多头排列策略 - 基于quantitative-finance的Senior-Quantitative-Trader"""
import pandas as pd
from app.services.strategy.base_strategy import BaseStrategy, Signal


class MAAlignmentStrategy(BaseStrategy):
    """
    均线多头排列策略

    策略逻辑：
    - 多头排列（MA5>MA10>MA20>MA60），且价格站上MA5，产生买入信号
    - 空头排列（MA5<MA10<MA20<MA60），或价格跌破MA20，产生卖出信号
    - 结合RSI过滤假信号

    参数：
    - ma_periods: 均线周期列表 (默认[5, 10, 20, 60])
    - rsi_period: RSI周期 (默认14)
    - rsi_threshold: RSI阈值 (默认50)
    """

    def __init__(self, params: dict = None):
        default_params = {
            "ma_periods": [5, 10, 20, 60],
            "rsi_period": 14,
            "rsi_threshold": 50
        }
        if params:
            default_params.update(params)

        super().__init__("均线多头排列策略", default_params)

    def get_description(self) -> str:
        return f"""
        均线多头排列策略
        - 均线周期: {self.params['ma_periods']}
        - RSI周期: {self.params['rsi_period']}
        - RSI阈值: {self.params['rsi_threshold']}
        - 买入条件: 多头排列 + 价格站上MA5 + RSI>{self.params['rsi_threshold']}
        - 卖出条件: 空头排列 或 价格跌破MA20
        """

    def generate_signal(self, df: pd.DataFrame) -> pd.DataFrame:
        """生成交易信号"""
        ma_periods = self.params['ma_periods']
        rsi_period = self.params['rsi_period']
        rsi_threshold = self.params['rsi_threshold']

        # 计算均线
        for period in ma_periods:
            df[f'ma{period}'] = df['close'].rolling(window=period).mean()

        # 计算RSI
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=rsi_period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=rsi_period).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))

        # 初始化信号列
        df['signal'] = Signal.HOLD.value

        # 生成信号
        for i in range(1, len(df)):
            # 检查多头排列
            ma_values = [df[f'ma{p}'].iloc[i] for p in ma_periods]
            is_bullish_alignment = all(ma_values[j] > ma_values[j+1] for j in range(len(ma_values)-1))

            # 检查空头排列
            is_bearish_alignment = all(ma_values[j] < ma_values[j+1] for j in range(len(ma_values)-1))

            # 买入条件：多头排列 + 价格站上MA5 + RSI>阈值
            if (is_bullish_alignment and
                df['close'].iloc[i] > df[f'ma{ma_periods[0]}'].iloc[i] and
                df['rsi'].iloc[i] > rsi_threshold):
                df.iloc[i, df.columns.get_loc('signal')] = Signal.BUY.value

            # 卖出条件：空头排列 或 价格跌破MA20
            elif (is_bearish_alignment or
                  df['close'].iloc[i] < df[f'ma{ma_periods[2]}'].iloc[i]):
                df.iloc[i, df.columns.get_loc('signal')] = Signal.SELL.value

        return df
