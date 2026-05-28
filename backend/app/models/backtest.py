"""回测记录数据模型"""
from sqlalchemy import Column, String, Integer, Float, Date, DateTime, JSON
from sqlalchemy.sql import func
from app.core.database import Base


class BacktestRecord(Base):
    """回测记录"""
    __tablename__ = "backtest_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    strategy_id = Column(Integer, nullable=False, comment="策略ID")
    stock_code = Column(String(10), nullable=False, comment="股票代码")
    start_date = Column(Date, nullable=False, comment="开始日期")
    end_date = Column(Date, nullable=False, comment="结束日期")
    initial_capital = Column(Float, default=100000.0, comment="初始资金")
    final_capital = Column(Float, comment="最终资金")
    total_return = Column(Float, comment="总收益率")
    annual_return = Column(Float, comment="年化收益率")
    max_drawdown = Column(Float, comment="最大回撤")
    sharpe_ratio = Column(Float, comment="夏普比率")
    win_rate = Column(Float, comment="胜率")
    total_trades = Column(Integer, comment="交易次数")
    result_data = Column(JSON, comment="详细结果JSON")
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<BacktestRecord(stock={self.stock_code}, return={self.total_return})>"
