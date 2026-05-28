"""分析API - 趋势评分、卖点预测、风险评估"""
from fastapi import APIRouter, Query, HTTPException
from typing import Optional
import numpy as np

from app.services.data.akshare_service import akshare_service
from app.utils.validators import validate_stock_code, validate_date

router = APIRouter()


@router.get("/analysis/trend_score/{stock_code}")
async def get_trend_score(
    stock_code: str,
    start_date: Optional[str] = Query(None, description="开始日期 YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="结束日期 YYYY-MM-DD")
):
    """获取趋势评分"""
    if not validate_stock_code(stock_code):
        raise HTTPException(status_code=400, detail="股票代码格式错误，应为6位数字")

    # 获取K线数据
    df = akshare_service.get_daily_data(stock_code, start_date, end_date)
    if df.empty:
        return {"error": f"获取K线数据失败: {stock_code}"}

    closes = df['close'].values
    highs = df['high'].values
    lows = df['low'].values

    # 计算均线
    ma5 = np.mean(closes[-5:]) if len(closes) >= 5 else closes[-1]
    ma10 = np.mean(closes[-10:]) if len(closes) >= 10 else closes[-1]
    ma20 = np.mean(closes[-20:]) if len(closes) >= 20 else closes[-1]
    ma60 = np.mean(closes[-60:]) if len(closes) >= 60 else closes[-1]

    # 计算RSI
    returns = np.diff(closes) / closes[:-1]
    gains = returns[returns > 0][-14:]
    losses = -returns[returns < 0][-14:]
    avg_gain = np.mean(gains) if len(gains) > 0 else 0
    avg_loss = np.mean(losses) if len(losses) > 0 else 0.001
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    # 计算MACD
    ema12 = closes[-1]  # 简化计算
    ema26 = closes[-1]
    macd_hist = ema12 - ema26

    # 趋势评分
    score = 0
    factors = []

    # 均线评分
    current_price = closes[-1]
    if current_price > ma5:
        score += 10
        factors.append("价格在MA5上方")
    if current_price > ma10:
        score += 15
        factors.append("价格在MA10上方")
    if current_price > ma20:
        score += 20
        factors.append("价格在MA20上方")
    if current_price > ma60:
        score += 25
        factors.append("价格在MA60上方")
    if ma5 > ma10 > ma20:
        score += 20
        factors.append("多头排列")

    # RSI评分
    if rsi > 70:
        factors.append("RSI超买")
    elif rsi > 60:
        score += 10
        factors.append("RSI偏强")
    elif rsi < 30:
        factors.append("RSI超卖")
    else:
        factors.append("RSI中性")

    # MACD评分
    if macd_hist > 0:
        score += 10
        factors.append("MACD红柱")

    # 趋势判断
    if score >= 80:
        trend = "强势上涨"
    elif score >= 60:
        trend = "上涨趋势"
    elif score >= 40:
        trend = "震荡整理"
    elif score >= 20:
        trend = "下跌趋势"
    else:
        trend = "强势下跌"

    return {
        "stock_code": stock_code,
        "current_price": float(current_price),
        "trend_score": score,
        "trend": trend,
        "factors": factors,
        "indicators": {
            "ma5": float(ma5),
            "ma10": float(ma10),
            "ma20": float(ma20),
            "ma60": float(ma60),
            "rsi": float(rsi)
        }
    }


@router.get("/analysis/sell_points/{stock_code}")
async def get_sell_points(
    stock_code: str,
    start_date: Optional[str] = Query(None, description="开始日期 YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="结束日期 YYYY-MM-DD")
):
    """获取卖点预测"""
    if not validate_stock_code(stock_code):
        raise HTTPException(status_code=400, detail="股票代码格式错误，应为6位数字")

    # 获取K线数据
    df = akshare_service.get_daily_data(stock_code, start_date, end_date)
    if df.empty:
        return {"error": f"获取K线数据失败: {stock_code}"}

    closes = df['close'].values
    highs = df['high'].values
    lows = df['low'].values

    # 计算布林带
    bb_period = 20
    bb_middle = np.mean(closes[-bb_period:])
    bb_std = np.std(closes[-bb_period:])
    bb_upper = bb_middle + 2 * bb_std
    bb_lower = bb_middle - 2 * bb_std

    # 计算均线
    ma5 = np.mean(closes[-5:]) if len(closes) >= 5 else closes[-1]
    ma20 = np.mean(closes[-20:]) if len(closes) >= 20 else closes[-1]

    # 计算近期高低点
    high_20d = np.max(highs[-20:]) if len(highs) >= 20 else np.max(highs)
    low_20d = np.min(lows[-20:]) if len(lows) >= 20 else np.min(lows)
    high_60d = np.max(highs[-60:]) if len(highs) >= 60 else np.max(highs)

    # 卖点预测
    current_price = closes[-1]
    sell_points = [
        {"level": "第一目标位", "price": float(bb_upper), "type": "布林上轨", "action": "减仓30%"},
        {"level": "第二目标位", "price": float(high_20d), "type": "20日最高", "action": "再减仓30%"},
        {"level": "第三目标位", "price": float(high_60d), "type": "60日最高", "action": "清仓"}
    ]

    # 支撑位
    support_levels = [
        {"level": "第一支撑", "price": float(ma20), "type": "MA20", "action": "观察"},
        {"level": "第二支撑", "price": float(bb_middle), "type": "布林中轨", "action": "减仓50%"},
        {"level": "第三支撑", "price": float(bb_lower), "type": "布林下轨", "action": "清仓"}
    ]

    return {
        "stock_code": stock_code,
        "current_price": float(current_price),
        "sell_points": sell_points,
        "support_levels": support_levels
    }


@router.get("/analysis/risk_assessment/{stock_code}")
async def get_risk_assessment(
    stock_code: str,
    start_date: Optional[str] = Query(None, description="开始日期 YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="结束日期 YYYY-MM-DD")
):
    """获取风险评估"""
    if not validate_stock_code(stock_code):
        raise HTTPException(status_code=400, detail="股票代码格式错误，应为6位数字")

    # 获取K线数据
    df = akshare_service.get_daily_data(stock_code, start_date, end_date)
    if df.empty:
        return {"error": f"获取K线数据失败: {stock_code}"}

    closes = df['close'].values

    # 计算收益率
    returns = np.diff(closes) / closes[:-1]

    # 计算风险指标
    total_return = (closes[-1] / closes[0] - 1) * 100
    annual_return = total_return * (252 / len(closes))
    annual_vol = np.std(returns) * np.sqrt(252) * 100
    sharpe = annual_return / annual_vol if annual_vol > 0 else 0

    # 计算最大回撤
    cum_returns = np.cumprod([1 + r for r in returns])
    running_max = np.maximum.accumulate(cum_returns)
    drawdown = (cum_returns - running_max) / running_max
    max_drawdown = np.min(drawdown) * 100

    # 计算VaR
    var_95 = np.percentile(returns, 5) * 100
    var_99 = np.percentile(returns, 1) * 100

    # 计算胜率
    win_rate = np.sum(returns > 0) / len(returns) * 100

    # 风险等级
    if max_drawdown > -10:
        risk_level = "低风险"
    elif max_drawdown > -20:
        risk_level = "中风险"
    elif max_drawdown > -30:
        risk_level = "高风险"
    else:
        risk_level = "极高风险"

    return {
        "stock_code": stock_code,
        "current_price": float(closes[-1]),
        "risk_level": risk_level,
        "metrics": {
            "total_return": float(total_return),
            "annual_return": float(annual_return),
            "annual_volatility": float(annual_vol),
            "sharpe_ratio": float(sharpe),
            "max_drawdown": float(max_drawdown),
            "var_95": float(var_95),
            "var_99": float(var_99),
            "win_rate": float(win_rate)
        }
    }
