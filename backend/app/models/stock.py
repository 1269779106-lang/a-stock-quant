"""股票数据模型"""
from sqlalchemy import Column, String, Float, Integer, Date, DateTime, BigInteger
from sqlalchemy.sql import func
from app.core.database import Base


class Stock(Base):
    """股票基本信息"""
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(10), unique=True, nullable=False, index=True, comment="股票代码")
    name = Column(String(50), nullable=False, comment="股票名称")
    market = Column(String(10), comment="市场: sh/sz/bj")
    industry = Column(String(50), comment="行业")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Stock(code={self.code}, name={self.name})>"


class StockDaily(Base):
    """股票日线数据"""
    __tablename__ = "stock_daily"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(10), nullable=False, index=True, comment="股票代码")
    date = Column(Date, nullable=False, comment="日期")
    open = Column(Float, comment="开盘价")
    close = Column(Float, comment="收盘价")
    high = Column(Float, comment="最高价")
    low = Column(Float, comment="最低价")
    volume = Column(BigInteger, comment="成交量")
    amount = Column(Float, comment="成交额")
    amplitude = Column(Float, comment="振幅")
    pct_change = Column(Float, comment="涨跌幅")
    change = Column(Float, comment="涨跌额")
    turnover = Column(Float, comment="换手率")
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<StockDaily(code={self.code}, date={self.date}, close={self.close})>"
