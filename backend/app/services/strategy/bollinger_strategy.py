"""布林带策略"""
import pandas as pd
from app.services.strategy.base_strategy import BaseStrategy, Signal


class BollingerStrategy(BaseStrategy):
    """
    布林带策略

    策略逻辑：
    - 价格触及下轨，产生买入信号
    - 价格触及上轨，产生卖出信号

    参数：
    - period: 布林带周期 (默认20)
    - std_dev: 标准差倍数 (默认2)
    """

    def __init__(self, params: dict = None):
        default_params = {
            "period": 20,
            "std_dev": 2
        }
        if params:
            default_params.update(params)

        super().__init__("布林带策略", default_params)

    def get_description(self) -> str:
        return f"""
        布林带策略
        - 周期: {self.params['period']}
        - 标准差倍数: {self.params['std_dev']}
        - 买入条件: 价格触及下轨
        - 卖出条件: 价格触及上轨
        """

    def generate_signal(self, df: pd.DataFrame) -> pd.DataFrame:
        """生成交易信号"""
        period = self.params['period']
        std_dev = self.params['std_dev']

        # 计算布林带
        df['boll_mid'] = df['close'].rolling(window=period).mean()
        std = df['close'].rolling(window=period).std()
        df['boll_upper'] = df['boll_mid'] + std_dev * std
        df['boll_lower'] = df['boll_mid'] - std_dev * std

        # 初始化信号列
        df['signal'] = Signal.HOLD.value

        # 生成信号
        for i in range(1, len(df)):
            # 价格从下轨反弹 - 买入
            if (df['close'].iloc[i] > df['boll_lower'].iloc[i] and
                df['close'].iloc[i-1] <= df['boll_lower'].iloc[i-1]):
                df.iloc[i, df.columns.get_loc('signal')] = Signal.BUY.value

            # 价格触及上轨 - 卖出
            elif (df['close'].iloc[i] >= df['boll_upper'].iloc[i] and
                  df['close'].iloc[i-1] < df['boll_upper'].iloc[i-1]):
                df.iloc[i, df.columns.get_loc('signal')] = Signal.SELL.value

        return df
