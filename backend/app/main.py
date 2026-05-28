"""A股量化交易系统 - 主应用入口"""
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings


# 应用生命周期管理
@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期"""
    # 延迟导入避免循环导入
    from app.core.logger import app_logger
    from app.core.database import init_db
    from app.services.data.realtime_service import realtime_service

    app_logger.info(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} 启动中...")

    # 初始化数据库
    init_db()

    # 启动实时数据推送循环（后台任务）
    push_task = asyncio.create_task(realtime_service.start_push_loop())

    app_logger.info(f"✅ {settings.APP_NAME} 启动成功")
    yield

    # 停止推送循环
    realtime_service.stop_push_loop()
    push_task.cancel()

    app_logger.info(f"👋 {settings.APP_NAME} 关闭中...")


# 创建FastAPI应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="A股量化交易系统API",
    lifespan=lifespan
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # 前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 健康检查
@app.get("/")
async def root():
    """根路径"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}


# 导入API路由 (延迟导入)
from app.api import market, strategy, backtest, websocket

app.include_router(market.router, prefix=settings.API_V1_PREFIX, tags=["行情数据"])
app.include_router(strategy.router, prefix=settings.API_V1_PREFIX, tags=["策略管理"])
app.include_router(backtest.router, prefix=settings.API_V1_PREFIX, tags=["回测系统"])
app.include_router(websocket.router, tags=["WebSocket实时数据"])
