"""核心配置模块"""
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """应用配置"""

    # 基础配置
    APP_NAME: str = "A股量化交易系统"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    # API配置
    API_V1_PREFIX: str = "/api/v1"

    # 数据库配置
    DB_TYPE: str = "sqlite"  # sqlite 或 postgresql
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    DB_NAME: str = "astock_quant"
    DATABASE_URL: Optional[str] = None

    # Redis配置
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    # Tushare配置
    TUSHARE_TOKEN: str = ""

    # 数据存储路径
    DATA_DIR: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data")

    class Config:
        env_file = ".env"
        case_sensitive = True

    def get_database_url(self) -> str:
        """获取数据库连接URL"""
        if self.DATABASE_URL:
            return self.DATABASE_URL

        if self.DB_TYPE == "sqlite":
            db_path = os.path.join(self.DATA_DIR, "astock.db")
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            return f"sqlite:///{db_path}"

        if not self.DB_USER or not self.DB_PASSWORD:
            raise ValueError("数据库凭据未配置，请设置DB_USER和DB_PASSWORD环境变量")

        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
