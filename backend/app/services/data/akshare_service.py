"""AKShare数据服务 - A股免费数据源"""
import os
import akshare as ak
import pandas as pd
import requests
from datetime import datetime, date, timedelta
from typing import Optional, List
from loguru import logger

# 数据缓存目录 - 使用相对路径
CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "data", "cache")
os.makedirs(CACHE_DIR, exist_ok=True)

# 禁用代理的请求会话
_session = requests.Session()
_session.trust_env = False  # 不使用系统代理

# 列名映射常量
COLUMN_RENAME_MAP = {
    "日期": "date",
    "开盘": "open",
    "收盘": "close",
    "最高": "high",
    "最低": "low",
    "成交量": "volume",
    "成交额": "amount",
    "振幅": "amplitude",
    "涨跌幅": "pct_change",
    "涨跌额": "change",
    "换手率": "turnover",
    "股票代码": "code",
    "时间": "datetime"
}


def get_cache_path(stock_code: str, data_type: str) -> str:
    """获取缓存文件路径"""
    return os.path.join(CACHE_DIR, f"{stock_code}_{data_type}.csv")


def load_cache(stock_code: str, data_type: str) -> Optional[pd.DataFrame]:
    """加载缓存数据"""
    cache_path = get_cache_path(stock_code, data_type)
    if os.path.exists(cache_path):
        try:
            df = pd.read_csv(cache_path)
            # 重命名列（如果是中文列名）
            df = df.rename(columns=COLUMN_RENAME_MAP)
            return df
        except Exception as e:
            logger.warning(f"加载缓存失败 {cache_path}: {e}")
    return None


def save_cache(stock_code: str, data_type: str, df: pd.DataFrame):
    """保存数据到缓存"""
    cache_path = get_cache_path(stock_code, data_type)
    try:
        df.to_csv(cache_path, index=False)
    except Exception as e:
        logger.error(f"保存缓存失败: {e}")


class AKShareService:
    """AKShare数据服务类"""

    def __init__(self):
        self.name = "AKShare"
        logger.info(f"初始化 {self.name} 数据服务")

    def get_stock_list(self, market: Optional[str] = None) -> pd.DataFrame:
        """
        获取股票列表

        Args:
            market: 市场类型 (sh沪市/sz深市/bj北交所/None全部)

        Returns:
            DataFrame: 股票列表
        """
        try:
            df = ak.stock_info_a_code_name()
            if market:
                if market == "sh":
                    df = df[df["code"].str.startswith("6")]
                elif market == "sz":
                    df = df[df["code"].str.startswith(("0", "3"))]
                elif market == "bj":
                    df = df[df["code"].str.startswith(("4", "8"))]
            return df
        except Exception as e:
            logger.error(f"获取股票列表失败: {e}", exc_info=True)
            return pd.DataFrame()

    def get_daily_data(
        self,
        stock_code: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        adjust: str = "qfq"
    ) -> pd.DataFrame:
        """
        获取日线数据

        Args:
            stock_code: 股票代码 (如 000001)
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
            adjust: 复权类型 (qfq前复权/hfq后复权/空字符串不复权)

        Returns:
            DataFrame: 日线数据
        """
        try:
            if not start_date:
                start_date = (datetime.now() - timedelta(days=365)).strftime("%Y%m%d")
            else:
                start_date = start_date.replace("-", "")

            if not end_date:
                end_date = datetime.now().strftime("%Y%m%d")
            else:
                end_date = end_date.replace("-", "")

            # 尝试使用腾讯接口（更稳定）
            try:
                market_prefix = "sz" if stock_code.startswith(("0", "3")) else "sh"
                symbol = f"{market_prefix}{stock_code}"
                df = ak.stock_zh_a_hist_tx(
                    symbol=symbol,
                    start_date=start_date,
                    end_date=end_date
                )
                if not df.empty:
                    # 腾讯接口返回的amount是成交量（手），需要重命名
                    if 'volume' not in df.columns and 'amount' in df.columns:
                        df = df.rename(columns={'amount': 'volume'})
                        df['amount'] = df['volume'] * df['close'] * 100  # 估算成交额
                    # 保存到缓存
                    save_cache(stock_code, "daily", df)
                    return df
            except Exception as e:
                logger.warning(f"腾讯接口失败 {stock_code}: {e}")

            # 备选：使用东方财富接口
            df = ak.stock_zh_a_hist(
                symbol=stock_code,
                period="daily",
                start_date=start_date,
                end_date=end_date,
                adjust=adjust
            )

            # 重命名列
            df = df.rename(columns=COLUMN_RENAME_MAP)

            # 保存到缓存
            if not df.empty:
                save_cache(stock_code, "daily", df)

            return df
        except Exception as e:
            logger.error(f"获取日线数据失败 {stock_code}: {e}")
            # 尝试从缓存加载
            cached_df = load_cache(stock_code, "daily")
            if cached_df is not None:
                logger.info(f"使用缓存数据: {stock_code}")
                return cached_df
            return pd.DataFrame()

    def get_minute_data(
        self,
        stock_code: str,
        period: str = "5",
        adjust: str = "qfq"
    ) -> pd.DataFrame:
        """
        获取分钟线数据

        Args:
            stock_code: 股票代码
            period: 周期 (1/5/15/30/60)
            adjust: 复权类型

        Returns:
            DataFrame: 分钟线数据
        """
        try:
            df = ak.stock_zh_a_hist_min_em(
                symbol=stock_code,
                period=period,
                adjust=adjust
            )

            # 重命名列
            df = df.rename(columns=COLUMN_RENAME_MAP)

            return df
        except Exception as e:
            logger.error(f"获取分钟线数据失败 {stock_code}: {e}", exc_info=True)
            return pd.DataFrame()

    def get_realtime_quote(self, stock_code: str) -> dict:
        """
        获取实时行情 (使用最新K线数据作为备选方案)

        Args:
            stock_code: 股票代码

        Returns:
            dict: 实时行情数据
        """
        try:
            # 尝试使用实时行情接口
            try:
                df = ak.stock_zh_a_spot_em()
                stock = df[df["代码"] == stock_code]

                if not stock.empty:
                    row = stock.iloc[0]
                    return {
                        "code": row["代码"],
                        "name": row["名称"],
                        "price": row["最新价"],
                        "change": row["涨跌额"],
                        "pct_change": row["涨跌幅"],
                        "open": row["今开"],
                        "high": row["最高"],
                        "low": row["最低"],
                        "pre_close": row["昨收"],
                        "volume": row["成交量"],
                        "amount": row["成交额"],
                        "turnover": row["换手率"],
                        "pe": row.get("市盈率-动态", None),
                        "pb": row.get("市净率", None),
                        "total_mv": row.get("总市值", None),
                        "circ_mv": row.get("流通市值", None)
                    }
            except Exception:
                pass

            # 备选方案：使用最新K线数据
            logger.info(f"使用K线数据作为实时行情: {stock_code}")
            df = self.get_daily_data(stock_code, start_date=(datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d"))

            if df.empty:
                return {}

            latest = df.iloc[-1]
            prev = df.iloc[-2] if len(df) > 1 else latest

            # 获取股票名称
            stock_name = self._get_stock_name(stock_code)

            return {
                "code": stock_code,
                "name": stock_name,
                "price": float(latest["close"]),
                "change": float(latest["close"] - prev["close"]),
                "pct_change": float((latest["close"] - prev["close"]) / prev["close"] * 100),
                "open": float(latest["open"]),
                "high": float(latest["high"]),
                "low": float(latest["low"]),
                "pre_close": float(prev["close"]),
                "volume": int(latest["volume"]),
                "amount": float(latest.get("amount", 0)),
                "turnover": float(latest.get("turnover", 0)),
                "pe": None,
                "pb": None,
                "total_mv": None,
                "circ_mv": None,
                "date": str(latest["date"]),
                "is_kline_data": True
            }
        except Exception as e:
            logger.error(f"获取实时行情失败 {stock_code}: {e}")
            return {}

    def _get_stock_name(self, stock_code: str) -> str:
        """获取股票名称"""
        try:
            df = self.get_stock_list()
            stock = df[df["code"] == stock_code]
            if not stock.empty:
                return stock.iloc[0]["name"]
        except Exception:
            pass
        return stock_code

    def get_industry_list(self) -> pd.DataFrame:
        """获取行业板块列表"""
        try:
            df = ak.stock_board_industry_name_em()
            return df
        except Exception as e:
            logger.error(f"获取行业板块失败: {e}")
            return pd.DataFrame()

    def get_concept_list(self) -> pd.DataFrame:
        """获取概念板块列表"""
        try:
            df = ak.stock_board_concept_name_em()
            return df
        except Exception as e:
            logger.error(f"获取概念板块失败: {e}")
            return pd.DataFrame()

    def get_stock_fund_flow(self, stock_code: str) -> pd.DataFrame:
        """获取个股资金流向"""
        try:
            df = ak.stock_individual_fund_flow(stock=stock_code, market="sh" if stock_code.startswith("6") else "sz")
            return df
        except Exception as e:
            logger.error(f"获取资金流向失败 {stock_code}: {e}")
            return pd.DataFrame()


# 创建全局实例
akshare_service = AKShareService()
