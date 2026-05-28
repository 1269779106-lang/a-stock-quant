"""策略数据模型"""
from sqlalchemy import Column, String, Integer, Text, DateTime, JSON
from sqlalchemy.sql import func
from app.core.database import Base


class Strategy(Base):
    """交易策略"""
    __tablename__ = "strategies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, comment="策略名称")
    type = Column(String(50), nullable=False, comment="策略类型: dual_ma/rsi/bollinger/macd")
    description = Column(Text, comment="策略描述")
    parameters = Column(JSON, comment="策略参数JSON")
    status = Column(String(20), default="active", comment="状态: active/inactive")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Strategy(name={self.name}, type={self.type})>"
