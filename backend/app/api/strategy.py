"""策略管理API"""
from fastapi import APIRouter, Query
from typing import Optional, List

from app.services.strategy import list_strategies, get_strategy, STRATEGY_REGISTRY

router = APIRouter()


@router.get("/strategy/list")
async def get_strategy_list(
    strategy_type: Optional[str] = Query(None, description="策略类型: intraday/swing/hft")
):
    """获取策略列表"""
    strategies = list_strategies()
    return {
        "total": len(strategies),
        "data": strategies
    }


@router.get("/strategy/{strategy_id}")
async def get_strategy_detail(strategy_id: str):
    """获取策略详情"""
    if strategy_id not in STRATEGY_REGISTRY:
        return {"error": f"未知策略: {strategy_id}"}

    strategy = get_strategy(strategy_id)
    return {
        "id": strategy_id,
        "name": strategy.name,
        "description": strategy.get_description(),
        "params": strategy.get_params()
    }


@router.post("/strategy/create")
async def create_strategy(
    name: str,
    strategy_type: str,
    params: dict = {}
):
    """创建策略"""
    return {
        "message": "自定义策略功能开发中...",
        "data": None
    }


@router.put("/strategy/{strategy_id}")
async def update_strategy(
    strategy_id: str,
    params: dict = {}
):
    """更新策略参数"""
    if strategy_id not in STRATEGY_REGISTRY:
        return {"error": f"未知策略: {strategy_id}"}

    strategy = get_strategy(strategy_id, params)
    return {
        "id": strategy_id,
        "name": strategy.name,
        "params": strategy.get_params(),
        "message": "参数更新成功"
    }


@router.delete("/strategy/{strategy_id}")
async def delete_strategy(strategy_id: str):
    """删除策略"""
    return {
        "strategy_id": strategy_id,
        "message": "内置策略不可删除"
    }
