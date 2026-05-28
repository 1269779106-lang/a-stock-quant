"""行情数据API"""
from fastapi import APIRouter, Query, HTTPException
from typing import Optional

from app.services.data.akshare_service import akshare_service
from app.services.data.indicator_service import indicator_service
from app.utils.validators import validate_stock_code, validate_date, validate_period, validate_adjust

router = APIRouter()


@router.get("/market/stock/{stock_code}")
async def get_stock_info(stock_code: str):
    """获取股票基本信息"""
    if not validate_stock_code(stock_code):
        raise HTTPException(status_code=400, detail="股票代码格式错误，应为6位数字")

    quote = akshare_service.get_realtime_quote(stock_code)
    return {
        "code": stock_code,
        "data": quote
    }


@router.get("/market/kline/{stock_code}")
async def get_kline_data(
    stock_code: str,
    period: str = Query("daily", description="周期: daily/weekly/monthly/60min/30min/15min/5min/1min"),
    start_date: Optional[str] = Query(None, description="开始日期 YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="结束日期 YYYY-MM-DD"),
    adjust: str = Query("qfq", description="复权: qfq前复权/hfq后复权/空字符串不复权")
):
    """获取K线数据"""
    # 验证输入
    if not validate_stock_code(stock_code):
        raise HTTPException(status_code=400, detail="股票代码格式错误，应为6位数字")

    if not validate_period(period):
        raise HTTPException(status_code=400, detail="无效的K线周期")

    if not validate_date(start_date) or not validate_date(end_date):
        raise HTTPException(status_code=400, detail="日期格式错误，应为YYYY-MM-DD")

    if not validate_adjust(adjust):
        raise HTTPException(status_code=400, detail="无效的复权类型")

    if period == "daily":
        df = akshare_service.get_daily_data(stock_code, start_date, end_date, adjust)
    else:
        df = akshare_service.get_minute_data(stock_code, period, adjust)

    if df.empty:
        return {"code": stock_code, "data": [], "message": "获取数据失败"}

    # 添加技术指标
    df = indicator_service.add_all_indicators(df)

    # 转换为字典列表，处理nan值
    import math
    data = df.to_dict(orient='records')
    for record in data:
        for key, value in record.items():
            if isinstance(value, float) and math.isnan(value):
                record[key] = None

    return {
        "code": stock_code,
        "period": period,
        "count": len(data),
        "data": data
    }


@router.get("/market/realtime/{stock_code}")
async def get_realtime_quote(stock_code: str):
    """获取实时行情"""
    if not validate_stock_code(stock_code):
        raise HTTPException(status_code=400, detail="股票代码格式错误，应为6位数字")

    quote = akshare_service.get_realtime_quote(stock_code)
    return {
        "code": stock_code,
        "data": quote
    }


@router.get("/market/stock_list")
async def get_stock_list(
    market: Optional[str] = Query(None, description="市场: sh/sz/bj"),
    industry: Optional[str] = Query(None, description="行业板块")
):
    """获取股票列表"""
    # 验证市场参数
    if market and market not in ["sh", "sz", "bj"]:
        raise HTTPException(status_code=400, detail="无效的市场参数，应为sh/sz/bj")

    df = akshare_service.get_stock_list(market)

    if df.empty:
        return {"data": [], "message": "获取数据失败"}

    # 转换为字典列表
    data = df.head(100).to_dict(orient='records')

    return {
        "total": len(df),
        "data": data
    }
