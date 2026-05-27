"""实时数据推送服务"""
import asyncio
import json
import os
from typing import Dict, List, Set
from datetime import datetime
from loguru import logger

# 禁用代理
for key in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy']:
    os.environ.pop(key, None)

import akshare as ak
import pandas as pd


class RealtimeDataService:
    """实时数据推送服务"""

    def __init__(self):
        self.name = "RealtimeData"
        self.subscribers: Dict[str, Set] = {}  # stock_code -> set of websocket connections
        self.running = False
        self.update_interval = 5  # 更新间隔（秒）
        logger.info(f"初始化 {self.name} 服务")

    async def subscribe(self, stock_code: str, websocket):
        """订阅股票实时数据"""
        if stock_code not in self.subscribers:
            self.subscribers[stock_code] = set()
        self.subscribers[stock_code].add(websocket)
        logger.info(f"新订阅: {stock_code}, 当前订阅数: {len(self.subscribers[stock_code])}")

    async def unsubscribe(self, stock_code: str, websocket):
        """取消订阅"""
        if stock_code in self.subscribers:
            self.subscribers[stock_code].discard(websocket)
            if not self.subscribers[stock_code]:
                del self.subscribers[stock_code]
            logger.info(f"取消订阅: {stock_code}")

    async def broadcast(self, stock_code: str, data: dict):
        """广播数据给订阅者"""
        if stock_code not in self.subscribers:
            return

        message = json.dumps(data, ensure_ascii=False)
        disconnected = set()

        for websocket in self.subscribers[stock_code]:
            try:
                await websocket.send_text(message)
            except Exception:
                disconnected.add(websocket)

        # 清理断开的连接
        for ws in disconnected:
            self.subscribers[stock_code].discard(ws)

    def get_realtime_data(self, stock_code: str) -> dict:
        """获取实时数据（使用最新K线）"""
        try:
            # 禁用代理
            for key in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy']:
                os.environ.pop(key, None)

            # 获取最新K线数据
            df = ak.stock_zh_a_hist(
                symbol=stock_code,
                period="daily",
                start_date=(datetime.now()).strftime("%Y%m%d"),
                end_date=datetime.now().strftime("%Y%m%d"),
                adjust="qfq"
            )

            if df.empty:
                # 如果今天没有数据，获取最近的数据
                df = ak.stock_zh_a_hist(
                    symbol=stock_code,
                    period="daily",
                    start_date=(datetime.now()).strftime("%Y%m%d"),
                    end_date=datetime.now().strftime("%Y%m%d"),
                    adjust="qfq"
                )

            if not df.empty:
                latest = df.iloc[-1]
                return {
                    "code": stock_code,
                    "name": self._get_stock_name(stock_code),
                    "price": float(latest["收盘"]),
                    "open": float(latest["开盘"]),
                    "high": float(latest["最高"]),
                    "low": float(latest["最低"]),
                    "volume": int(latest["成交量"]),
                    "amount": float(latest["成交额"]),
                    "change": float(latest["涨跌额"]),
                    "pct_change": float(latest["涨跌幅"]),
                    "timestamp": datetime.now().isoformat()
                }
        except Exception as e:
            logger.error(f"获取实时数据失败 {stock_code}: {e}")

        return None

    def _get_stock_name(self, stock_code: str) -> str:
        """获取股票名称"""
        try:
            df = ak.stock_info_a_code_name()
            stock = df[df["code"] == stock_code]
            if not stock.empty:
                return stock.iloc[0]["name"]
        except Exception:
            pass
        return stock_code

    async def start_push_loop(self):
        """启动推送循环"""
        self.running = True
        logger.info("启动实时数据推送循环")

        while self.running:
            try:
                # 遍历所有订阅的股票
                for stock_code in list(self.subscribers.keys()):
                    if not self.subscribers[stock_code]:
                        continue

                    data = self.get_realtime_data(stock_code)
                    if data:
                        await self.broadcast(stock_code, data)

                await asyncio.sleep(self.update_interval)
            except Exception as e:
                logger.error(f"推送循环错误: {e}")
                await asyncio.sleep(1)

    def stop_push_loop(self):
        """停止推送循环"""
        self.running = False
        logger.info("停止实时数据推送循环")


# 创建全局实例
realtime_service = RealtimeDataService()
