"""策略模块"""
from app.services.strategy.base_strategy import BaseStrategy, Signal, TradeOrder
from app.services.strategy.dual_ma_strategy import DualMAStrategy
from app.services.strategy.rsi_strategy import RSIStrategy
from app.services.strategy.bollinger_strategy import BollingerStrategy
from app.services.strategy.macd_strategy import MACDStrategy
from app.services.strategy.momentum_strategy import MomentumBreakoutStrategy
from app.services.strategy.ma_alignment_strategy import MAAlignmentStrategy

# 策略注册表
STRATEGY_REGISTRY = {
    "dual_ma": DualMAStrategy,
    "rsi": RSIStrategy,
    "bollinger": BollingerStrategy,
    "macd": MACDStrategy,
    "momentum": MomentumBreakoutStrategy,
    "ma_alignment": MAAlignmentStrategy,
}


def get_strategy(strategy_name: str, params: dict = None) -> BaseStrategy:
    """
    获取策略实例

    Args:
        strategy_name: 策略名称
        params: 策略参数

    Returns:
        BaseStrategy: 策略实例
    """
    if strategy_name not in STRATEGY_REGISTRY:
        raise ValueError(f"未知策略: {strategy_name}, 可用策略: {list(STRATEGY_REGISTRY.keys())}")

    strategy_class = STRATEGY_REGISTRY[strategy_name]
    return strategy_class(params)


def list_strategies() -> list:
    """列出所有可用策略"""
    strategies = []
    for name, cls in STRATEGY_REGISTRY.items():
        strategy = cls()
        strategies.append({
            "name": name,
            "display_name": strategy.name,
            "description": strategy.get_description()
        })
    return strategies
