"""回测引擎"""
import pandas as pd
import numpy as np
from typing import Optional, Dict
from dataclasses import dataclass
from datetime import datetime
from loguru import logger

from app.services.strategy.base_strategy import BaseStrategy, Signal

# 常量定义
CASH_RESERVE_RATIO = 0.95  # 保留5%现金
RISK_FREE_RATE = 0.03  # 无风险利率3%
TRADING_DAYS_PER_YEAR = 252  # 每年交易日


@dataclass
class BacktestResult:
    """回测结果"""
    strategy_name: str
    stock_code: str
    start_date: str
    end_date: str
    initial_capital: float
    final_capital: float
    total_return: float
    annual_return: float
    max_drawdown: float
    sharpe_ratio: float
    win_rate: float
    profit_loss_ratio: float
    total_trades: int
    winning_trades: int
    losing_trades: int
    trades: list
    equity_curve: pd.DataFrame


class BacktestEngine:
    """回测引擎"""

    def __init__(
        self,
        initial_capital: float = 1000000,
        commission: float = 0.0003,
        slippage: float = 0.001,
        stamp_tax: float = 0.001,
        stop_loss: float = 0.0,
        take_profit: float = 0.0
    ):
        """
        初始化回测引擎

        Args:
            initial_capital: 初始资金
            commission: 手续费率
            slippage: 滑点
            stamp_tax: 印花税 (卖出时收取)
            stop_loss: 止损比例 (0表示不止损)
            take_profit: 止盈比例 (0表示不止盈)
        """
        self.initial_capital = initial_capital
        self.commission = commission
        self.slippage = slippage
        self.stamp_tax = stamp_tax
        self.stop_loss = stop_loss
        self.take_profit = take_profit

        logger.info(f"初始化回测引擎: 初始资金={initial_capital}, 手续费={commission}, 滑点={slippage}, 止损={stop_loss}, 止盈={take_profit}")

    def run(self, strategy: BaseStrategy, df: pd.DataFrame) -> BacktestResult:
        """
        运行回测

        Args:
            strategy: 策略实例
            df: 行情数据

        Returns:
            BacktestResult: 回测结果
        """
        logger.info(f"开始回测: {strategy.name}")

        # 生成信号
        df = strategy.generate_signal(df.copy())

        # 初始化状态
        capital = self.initial_capital
        position = 0
        position_price = 0
        trades = []
        equity_curve = []

        # 遍历数据
        for i in range(len(df)):
            row = df.iloc[i]
            signal = row['signal']
            price = row['close']
            date = row.get('date', row.name)

            # 买入信号
            if signal == Signal.BUY.value and position == 0:
                # 计算可买数量
                available_capital = capital * CASH_RESERVE_RATIO
                shares = int(available_capital / price / 100) * 100

                if shares >= 100:
                    # 计算实际成本（含手续费和滑点）
                    actual_price = price * (1 + self.slippage)
                    cost = shares * actual_price
                    commission_fee = cost * self.commission
                    total_cost = cost + commission_fee

                    if total_cost <= capital:
                        capital -= total_cost
                        position = shares
                        position_price = actual_price

                        trades.append({
                            "type": "BUY",
                            "date": str(date),
                            "price": actual_price,
                            "shares": shares,
                            "cost": total_cost,
                            "commission": commission_fee
                        })

            # 卖出信号
            elif signal == Signal.SELL.value and position > 0:
                # 计算卖出收入
                actual_price = price * (1 - self.slippage)
                revenue = position * actual_price
                commission_fee = revenue * self.commission
                stamp_tax_fee = revenue * self.stamp_tax
                net_revenue = revenue - commission_fee - stamp_tax_fee

                capital += net_revenue

                trades.append({
                    "type": "SELL",
                    "date": str(date),
                    "price": actual_price,
                    "shares": position,
                    "revenue": net_revenue,
                    "commission": commission_fee,
                    "stamp_tax": stamp_tax_fee,
                    "profit": net_revenue - position * position_price
                })

                position = 0
                position_price = 0

            # 止损检查
            elif position > 0 and self.stop_loss > 0:
                loss_pct = (price - position_price) / position_price
                if loss_pct <= -self.stop_loss:
                    # 触发止损
                    actual_price = price * (1 - self.slippage)
                    revenue = position * actual_price
                    commission_fee = revenue * self.commission
                    stamp_tax_fee = revenue * self.stamp_tax
                    net_revenue = revenue - commission_fee - stamp_tax_fee

                    capital += net_revenue

                    trades.append({
                        "type": "STOP_LOSS",
                        "date": str(date),
                        "price": actual_price,
                        "shares": position,
                        "revenue": net_revenue,
                        "commission": commission_fee,
                        "stamp_tax": stamp_tax_fee,
                        "profit": net_revenue - position * position_price
                    })

                    position = 0
                    position_price = 0

            # 止盈检查
            elif position > 0 and self.take_profit > 0:
                profit_pct = (price - position_price) / position_price
                if profit_pct >= self.take_profit:
                    # 触发止盈
                    actual_price = price * (1 - self.slippage)
                    revenue = position * actual_price
                    commission_fee = revenue * self.commission
                    stamp_tax_fee = revenue * self.stamp_tax
                    net_revenue = revenue - commission_fee - stamp_tax_fee

                    capital += net_revenue

                    trades.append({
                        "type": "TAKE_PROFIT",
                        "date": str(date),
                        "price": actual_price,
                        "shares": position,
                        "revenue": net_revenue,
                        "commission": commission_fee,
                        "stamp_tax": stamp_tax_fee,
                        "profit": net_revenue - position * position_price
                    })

                    position = 0
                    position_price = 0

            # 记录权益
            total_equity = capital + position * price
            equity_curve.append({
                "date": date,
                "capital": capital,
                "position_value": position * price,
                "total_equity": total_equity
            })

        # 计算统计指标
        equity_df = pd.DataFrame(equity_curve)
        result = self._calculate_metrics(
            strategy_name=strategy.name,
            stock_code=df.iloc[0].get('code', 'unknown'),
            start_date=str(df.iloc[0].get('date', '')),
            end_date=str(df.iloc[-1].get('date', '')),
            equity_df=equity_df,
            trades=trades
        )

        logger.info(f"回测完成: 总收益={result.total_return:.2%}, 最大回撤={result.max_drawdown:.2%}")

        return result

    def _calculate_metrics(
        self,
        strategy_name: str,
        stock_code: str,
        start_date: str,
        end_date: str,
        equity_df: pd.DataFrame,
        trades: list
    ) -> BacktestResult:
        """计算回测指标"""

        # 基础数据
        initial_capital = self.initial_capital
        final_capital = equity_df['total_equity'].iloc[-1]

        # 总收益率
        total_return = (final_capital - initial_capital) / initial_capital

        # 年化收益率
        days = len(equity_df)
        annual_return = (1 + total_return) ** (TRADING_DAYS_PER_YEAR / days) - 1 if days > 0 else 0

        # 最大回撤
        cummax = equity_df['total_equity'].cummax()
        drawdown = (equity_df['total_equity'] - cummax) / cummax
        max_drawdown = drawdown.min()

        # 夏普比率
        returns = equity_df['total_equity'].pct_change().dropna()
        if len(returns) > 0 and returns.std() > 0:
            sharpe_ratio = (returns.mean() * TRADING_DAYS_PER_YEAR - RISK_FREE_RATE) / (returns.std() * np.sqrt(TRADING_DAYS_PER_YEAR))
        else:
            sharpe_ratio = 0

        # 交易统计
        sell_trades = [t for t in trades if t['type'] == 'SELL']
        winning_trades = len([t for t in sell_trades if t.get('profit', 0) > 0])
        losing_trades = len([t for t in sell_trades if t.get('profit', 0) <= 0])
        total_trades = len(sell_trades)

        # 胜率
        win_rate = winning_trades / total_trades if total_trades > 0 else 0

        # 盈亏比
        avg_win = np.mean([t['profit'] for t in sell_trades if t.get('profit', 0) > 0]) if winning_trades > 0 else 0
        avg_loss = abs(np.mean([t['profit'] for t in sell_trades if t.get('profit', 0) <= 0])) if losing_trades > 0 else 1
        profit_loss_ratio = avg_win / avg_loss if avg_loss > 0 else 0

        return BacktestResult(
            strategy_name=strategy_name,
            stock_code=stock_code,
            start_date=start_date,
            end_date=end_date,
            initial_capital=initial_capital,
            final_capital=final_capital,
            total_return=total_return,
            annual_return=annual_return,
            max_drawdown=max_drawdown,
            sharpe_ratio=sharpe_ratio,
            win_rate=win_rate,
            profit_loss_ratio=profit_loss_ratio,
            total_trades=total_trades,
            winning_trades=winning_trades,
            losing_trades=losing_trades,
            trades=trades,
            equity_curve=equity_df
        )
