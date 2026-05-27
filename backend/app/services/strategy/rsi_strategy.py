"""RSI超买超卖策略"""
import pandas as pd
from app.services.strategy.base_strategy import BaseStrategy, Signal


class RSIStrategy(BaseStrategy):
    """
    RSI超买超卖策略

    策略逻辑：
    - RSI低于超卖线，产生买入信号
    - RSI高于超买线，产生卖出信号

    参数：
    - rsi_period: RSI周期 (默认14)
    - oversold: 超卖线 (默认30)
    - overbought: 超买线 (默认70)
    """

    def __init__(self, params: dict = None):
        default_params = {
            "rsi_period": 14,
            "oversold": 30,
            "overbought": 70
        }
        if params:
            default_params.update(params)

        super().__init__("RSI策略", default_params)

    def get_description(self) -> str:
        return f"""
        RSI超买超卖策略
        - RSI周期: {self.params['rsi_period']}
        - 超卖线: {self.params['oversold']}
        - 超买线: {self.params['overbought']}
        - 买入条件: RSI < {self.params['oversold']}
        - 卖出条件: RSI > {self.params['overbought']}
        """

    def generate_signal(self, df: pd.DataFrame) -> pd.DataFrame:
        """生成交易信号"""
        period = self.params['rsi_period']
        oversold = self.params['oversold']
        overbought = self.params['overbought']

        # 计算RSI
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))

        # 初始化信号列
        df['signal'] = Signal.HOLD.value

        # 生成信号
        for i in range(1, len(df)):
            # RSI从超卖区域回升 - 买入
            if df['rsi'].iloc[i] > oversold and df['rsi'].iloc[i-1] <= oversold:
                df.iloc[i, df.columns.get_loc('signal')] = Signal.BUY.value

            # RSI进入超买区域 - 卖出
            elif df['rsi'].iloc[i] > overbought and df['rsi'].iloc[i-1] <= overbought:
                df.iloc[i, df.columns.get_loc('signal')] = Signal.SELL.value

        return df
