"""回测系统API"""
from fastapi import APIRouter, Query
from typing import Optional

from app.services.strategy import get_strategy, STRATEGY_REGISTRY
from app.services.backtest.engine import BacktestEngine
from app.services.data.akshare_service import akshare_service

router = APIRouter()


@router.post("/backtest/run")
async def run_backtest(
    strategy_id: str = Query(..., description="策略ID"),
    stock_code: str = Query(..., description="股票代码"),
    start_date: str = Query(..., description="开始日期 YYYY-MM-DD"),
    end_date: str = Query(..., description="结束日期 YYYY-MM-DD"),
    initial_capital: float = Query(1000000, description="初始资金"),
    commission: float = Query(0.0003, description="手续费率"),
    slippage: float = Query(0.001, description="滑点")
):
    """运行回测"""
    # 验证策略
    if strategy_id not in STRATEGY_REGISTRY:
        return {"error": f"未知策略: {strategy_id}"}

    # 获取K线数据
    df = akshare_service.get_daily_data(stock_code, start_date, end_date)
    if df.empty:
        return {"error": f"获取K线数据失败: {stock_code}"}

    # 初始化策略和回测引擎
    strategy = get_strategy(strategy_id)
    engine = BacktestEngine(
        initial_capital=initial_capital,
        commission=commission,
        slippage=slippage
    )

    # 运行回测
    result = engine.run(strategy, df)

    return {
        "strategy_name": result.strategy_name,
        "stock_code": result.stock_code,
        "start_date": str(result.start_date),
        "end_date": str(result.end_date),
        "initial_capital": result.initial_capital,
        "final_capital": round(result.final_capital, 2),
        "total_return": round(result.total_return * 100, 2),
        "annual_return": round(result.annual_return * 100, 2),
        "max_drawdown": round(result.max_drawdown * 100, 2),
        "sharpe_ratio": round(result.sharpe_ratio, 2),
        "win_rate": round(result.win_rate * 100, 2),
        "profit_loss_ratio": round(result.profit_loss_ratio, 2),
        "total_trades": result.total_trades,
        "winning_trades": result.winning_trades,
        "losing_trades": result.losing_trades,
        "trades": result.trades
    }


@router.get("/backtest/result/{backtest_id}")
async def get_backtest_result(backtest_id: str):
    """获取回测结果"""
    return {
        "backtest_id": backtest_id,
        "message": "回测历史功能开发中..."
    }


@router.get("/backtest/history")
async def get_backtest_history(
    strategy_id: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    """获取回测历史"""
    return {
        "data": [],
        "message": "回测历史功能开发中..."
    }
