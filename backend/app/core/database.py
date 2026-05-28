"""数据库连接模块"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.core.logger import app_logger

# 创建数据库引擎
engine_kwargs = {
    "pool_pre_ping": True,
    "echo": False,  # 生产环境不记录SQL
}

# SQLite不支持这些连接池参数
if settings.DB_TYPE != "sqlite":
    engine_kwargs.update({
        "pool_size": 10,
        "max_overflow": 20,
    })
else:
    # SQLite配置
    engine_kwargs["connect_args"] = {"timeout": 10}

engine = create_engine(settings.get_database_url(), **engine_kwargs)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 基础模型类
Base = declarative_base()


def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """初始化数据库"""
    try:
        Base.metadata.create_all(bind=engine)
        app_logger.info("数据库初始化成功")
    except Exception as e:
        app_logger.error(f"数据库初始化失败: {e}")
        raise
