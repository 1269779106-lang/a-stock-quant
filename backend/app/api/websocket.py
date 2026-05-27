"""WebSocket实时数据推送API"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
import asyncio
from loguru import logger

from app.services.data.realtime_service import realtime_service

router = APIRouter()


@router.websocket("/ws/realtime/{stock_code}")
async def websocket_realtime(websocket: WebSocket, stock_code: str):
    """
    WebSocket实时数据推送

    连接后自动订阅指定股票的实时数据
    """
    await websocket.accept()
    logger.info(f"WebSocket连接建立: {stock_code}")

    # 订阅股票数据
    await realtime_service.subscribe(stock_code, websocket)

    try:
        # 发送初始数据
        data = realtime_service.get_realtime_data(stock_code)
        if data:
            import json
            await websocket.send_text(json.dumps(data, ensure_ascii=False))

        # 保持连接
        while True:
            try:
                # 接收客户端消息（心跳或取消订阅）
                message = await asyncio.wait_for(websocket.receive_text(), timeout=30)
                logger.debug(f"收到消息: {message}")
            except asyncio.TimeoutError:
                # 发送心跳
                try:
                    await websocket.send_text('{"type":"heartbeat"}')
                except Exception:
                    break
    except WebSocketDisconnect:
        logger.info(f"WebSocket断开: {stock_code}")
    except Exception as e:
        logger.error(f"WebSocket错误: {e}")
    finally:
        # 取消订阅
        await realtime_service.unsubscribe(stock_code, websocket)


@router.websocket("/ws/market")
async def websocket_market(websocket: WebSocket):
    """
    WebSocket市场数据推送

    推送多个股票的实时数据
    """
    await websocket.accept()
    logger.info("WebSocket市场数据连接建立")

    subscribed_stocks = set()

    try:
        while True:
            try:
                # 接收客户端消息
                message = await asyncio.wait_for(websocket.receive_text(), timeout=30)

                # 解析消息
                import json
                data = json.loads(message)

                if data.get("action") == "subscribe":
                    # 订阅股票
                    stock_codes = data.get("stocks", [])
                    for code in stock_codes:
                        subscribed_stocks.add(code)
                        await realtime_service.subscribe(code, websocket)
                    logger.info(f"订阅股票: {stock_codes}")

                elif data.get("action") == "unsubscribe":
                    # 取消订阅
                    stock_codes = data.get("stocks", [])
                    for code in stock_codes:
                        subscribed_stocks.discard(code)
                        await realtime_service.unsubscribe(code, websocket)
                    logger.info(f"取消订阅: {stock_codes}")

            except asyncio.TimeoutError:
                # 发送心跳
                try:
                    await websocket.send_text('{"type":"heartbeat"}')
                except Exception:
                    break

    except WebSocketDisconnect:
        logger.info("WebSocket市场数据断开")
    except Exception as e:
        logger.error(f"WebSocket市场数据错误: {e}")
    finally:
        # 清理订阅
        for code in subscribed_stocks:
            await realtime_service.unsubscribe(code, websocket)
