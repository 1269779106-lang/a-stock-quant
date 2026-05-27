# A股量化交易系统 - 完整开发报告

**项目名称**: A股量化交易系统
**项目位置**: D:/a-stock-quant
**开发日期**: 2026-05-27
**开发者**: Claude Code

---

## 一、项目概述

### 1.1 项目目标

构建一个完整的A股量化交易平台，支持：
- A股行情数据获取与展示
- 量化策略开发与回测
- 实时数据推送
- 交易看板（Dashboard）

### 1.2 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| 后端 | Python + FastAPI | Web框架 |
| 数据源 | AKShare | A股免费数据 |
| 数据库 | SQLite/PostgreSQL | 数据存储 |
| 前端 | React + TypeScript | UI框架 |
| UI库 | Ant Design | 组件库 |
| 图表 | TradingView | K线图表 |
| 状态管理 | Zustand | 前端状态 |
| 实时推送 | WebSocket | 实时数据 |

---

## 二、项目结构

```
D:/a-stock-quant/
├── backend/                    # 后端服务
│   ├── app/
│   │   ├── api/               # API接口
│   │   │   ├── market.py      # 行情API
│   │   │   ├── strategy.py    # 策略API
│   │   │   ├── backtest.py    # 回测API
│   │   │   └── websocket.py   # WebSocket API
│   │   ├── core/              # 核心配置
│   │   │   ├── config.py      # 配置管理
│   │   │   ├── logger.py      # 日志系统
│   │   │   └── database.py    # 数据库连接
│   │   ├── services/          # 业务服务
│   │   │   ├── data/          # 数据服务
│   │   │   │   ├── akshare_service.py    # AKShare数据
│   │   │   │   ├── indicator_service.py  # 技术指标
│   │   │   │   └── realtime_service.py   # 实时数据
│   │   │   ├── strategy/      # 策略引擎
│   │   │   │   ├── base_strategy.py      # 策略基类
│   │   │   │   ├── dual_ma_strategy.py   # 双均线策略
│   │   │   │   ├── rsi_strategy.py       # RSI策略
│   │   │   │   └── bollinger_strategy.py # 布林带策略
│   │   │   └── backtest/      # 回测系统
│   │   │       └── engine.py  # 回测引擎
│   │   └── main.py            # 主应用入口
│   ├── requirements.txt       # Python依赖
│   └── run.py                 # 启动脚本
│
├── frontend/                   # 前端应用
│   ├── src/
│   │   ├── layouts/           # 布局组件
│   │   │   └── MainLayout.tsx # 主布局
│   │   ├── pages/             # 页面组件
│   │   │   ├── Dashboard.tsx  # 交易看板
│   │   │   ├── Market.tsx     # 行情数据
│   │   │   ├── Strategy.tsx   # 策略管理
│   │   │   └── Backtest.tsx   # 回测系统
│   │   ├── services/          # API服务
│   │   │   ├── api.ts         # HTTP API
│   │   │   └── websocket.ts   # WebSocket服务
│   │   ├── stores/            # 状态管理
│   │   │   └── useStore.ts    # Zustand Store
│   │   ├── App.tsx            # 主应用
│   │   └── main.tsx           # 入口文件
│   ├── package.json           # 前端依赖
│   └── vite.config.ts         # Vite配置
│
├── strategies/                 # 策略库（扩展用）
│   ├── intraday/              # 日内策略
│   ├── swing/                 # 波段策略
│   └── hft/                   # 高频策略
│
├── data/                       # 数据存储
│   ├── market/                # 行情数据
│   ├── cache/                 # 数据缓存
│   └── logs/                  # 日志文件
│
└── docs/                       # 文档
    ├── development-report.md  # 本报告
    ├── test-report-final.md   # 最终测试报告
    └── test-report-phase*.md  # 各阶段报告
```

---

## 三、开发历程

### 3.1 第一阶段：基础框架搭建

**时间**: 2026-05-27 13:30 - 14:00

**完成内容**:
- 创建项目目录结构
- 后端FastAPI框架搭建
- 前端React+Vite框架搭建
- 核心配置模块
- 日志系统
- 数据库配置

**关键文件**:
- `backend/app/main.py` - FastAPI主应用
- `backend/app/core/config.py` - 配置管理
- `backend/app/core/logger.py` - 日志系统
- `frontend/src/App.tsx` - React主应用
- `frontend/src/layouts/MainLayout.tsx` - 主布局

### 3.2 第二阶段：数据服务开发

**时间**: 2026-05-27 14:00 - 14:30

**完成内容**:
- AKShare数据服务封装
- 技术指标计算服务（22个指标）
- 策略引擎基类
- 3个内置策略（双均线、RSI、布林带）
- 回测引擎

**关键文件**:
- `backend/app/services/data/akshare_service.py` - 数据服务
- `backend/app/services/data/indicator_service.py` - 技术指标
- `backend/app/services/strategy/base_strategy.py` - 策略基类
- `backend/app/services/backtest/engine.py` - 回测引擎

**技术指标清单**:
- MA均线: ma5, ma10, ma20, ma60
- EMA均线: ema12, ema26
- MACD: macd_dif, macd_dea, macd_hist
- RSI: rsi14
- KDJ: kdj_k, kdj_d, kdj_j
- 布林带: boll_mid, boll_upper, boll_lower
- ATR: atr14
- OBV: obv
- 量比: volume_ratio
- 成交量均线: vol_ma5, vol_ma10, vol_ma20

### 3.3 第三阶段：API接口开发

**时间**: 2026-05-27 14:30 - 15:00

**完成内容**:
- 行情数据API
- 策略管理API
- 回测系统API
- 前后端联调

**API清单**:
- `GET /api/v1/market/stock_list` - 股票列表
- `GET /api/v1/market/kline/{code}` - K线数据+技术指标
- `GET /api/v1/market/realtime/{code}` - 实时行情
- `GET /api/v1/strategy/list` - 策略列表
- `POST /api/v1/backtest/run` - 运行回测

### 3.4 第四阶段：实时数据推送

**时间**: 2026-05-27 15:00 - 15:30

**完成内容**:
- WebSocket服务端
- 实时数据推送服务
- 前端WebSocket客户端
- 行情页面实时更新

**WebSocket端点**:
- `ws://localhost:8000/ws/realtime/{code}` - 单股票实时数据
- `ws://localhost:8000/ws/market` - 多股票市场数据

### 3.5 第五阶段：测试验收

**时间**: 2026-05-27 15:30 - 16:40

**完成内容**:
- 功能测试
- 量化交易测试
- 策略回测验证
- 问题修复

---

## 四、核心功能说明

### 4.1 数据服务

**AKShare数据服务** (`akshare_service.py`)

```python
# 获取股票列表
df = akshare_service.get_stock_list(market='sh')  # 沪市

# 获取K线数据
df = akshare_service.get_daily_data('600519', start_date='2026-01-01')

# 获取实时行情
quote = akshare_service.get_realtime_quote('600519')
```

**注意事项**:
- 网络代理问题：Windows系统代理可能导致连接失败
- 缓存机制：数据获取失败时自动加载缓存
- 缓存位置：`D:/a-stock-quant/data/cache/`

### 4.2 技术指标

**指标服务** (`indicator_service.py`)

```python
from app.services.data.indicator_service import indicator_service

# 添加所有技术指标
df = indicator_service.add_all_indicators(df)

# 添加单个指标
df = indicator_service.add_ma(df, periods=[5, 10, 20])
df = indicator_service.add_macd(df)
df = indicator_service.add_rsi(df, period=14)
```

### 4.3 策略引擎

**策略基类** (`base_strategy.py`)

```python
from app.services.strategy.base_strategy import BaseStrategy, Signal

class MyStrategy(BaseStrategy):
    def generate_signal(self, df):
        # 生成交易信号
        # Signal.BUY = 1 (买入)
        # Signal.SELL = -1 (卖出)
        # Signal.HOLD = 0 (持有)
        return df
```

**内置策略**:
1. **双均线策略** (dual_ma) - 趋势跟踪
2. **RSI策略** (rsi) - 超买超卖反转
3. **布林带策略** (bollinger) - 通道突破

### 4.4 回测系统

**回测引擎** (`engine.py`)

```python
from app.services.backtest.engine import BacktestEngine
from app.services.strategy import get_strategy

# 初始化
strategy = get_strategy('dual_ma')
engine = BacktestEngine(
    initial_capital=1000000,
    commission=0.0003,  # 手续费
    slippage=0.001      # 滑点
)

# 运行回测
result = engine.run(strategy, df)

# 查看结果
print(f'总收益率: {result.total_return:.2%}')
print(f'最大回撤: {result.max_drawdown:.2%}')
print(f'夏普比率: {result.sharpe_ratio:.2f}')
```

### 4.5 实时数据推送

**WebSocket服务** (`realtime_service.py`)

```javascript
// 前端使用
import wsService from './services/websocket';

// 连接
wsService.connect();

// 订阅股票
wsService.subscribeStock('600519', (data) => {
  console.log(data.price, data.pct_change);
});
```

---

## 五、启动指南

### 5.1 后端启动

```bash
# 进入后端目录
cd D:/a-stock-quant/backend

# 安装依赖
pip install -r requirements.txt

# 启动服务
python run.py
```

后端将在 http://localhost:8000 启动
API文档：http://localhost:8000/docs

### 5.2 前端启动

```bash
# 进入前端目录
cd D:/a-stock-quant/frontend

# 安装依赖
npm install

# 启动服务
npm run dev
```

前端将在 http://localhost:5173 启动

### 5.3 访问系统

- 交易看板: http://localhost:5173/dashboard
- 行情数据: http://localhost:5173/market
- 策略管理: http://localhost:5173/strategy
- 回测系统: http://localhost:5173/backtest

---

## 六、测试结果

### 6.1 功能测试

| 测试项 | 状态 | 说明 |
|--------|------|------|
| 后端服务启动 | ✅ | 正常运行 |
| 股票列表API | ✅ | 5524只A股 |
| K线数据API | ✅ | 含技术指标 |
| 策略列表API | ✅ | 3个策略 |
| 回测系统 | ✅ | 完整流程 |
| WebSocket | ✅ | 实时推送 |

### 6.2 量化交易测试

| 策略 | 总收益 | 最大回撤 | 夏普比率 | 胜率 |
|------|--------|----------|----------|------|
| 双均线 | -3.13% | -8.61% | -0.73 | 20% |
| RSI | +1.67% | -8.33% | -0.03 | 50% |
| 布林带 | +3.01% | -9.37% | 0.13 | 67% |

---

## 七、已知问题

### 7.1 网络代理问题

**问题**: Windows系统代理 (127.0.0.1:7890) 导致AKShare连接失败

**解决方案**:
1. 使用缓存机制：网络失败时自动加载缓存
2. 手动禁用代理：关闭系统代理设置

### 7.2 数据缓存有限

**问题**: 缓存数据只有16条，回测数据不足

**解决方案**:
1. 在网络正常时获取更多历史数据
2. 手动下载数据保存到缓存目录

---

## 八、下一步开发计划

### 8.1 短期计划

| 优先级 | 任务 | 说明 |
|--------|------|------|
| P0 | 获取更多历史数据 | 用于更准确的回测 |
| P1 | K线图表集成 | TradingView Lightweight Charts |
| P1 | 完善行情详情页面 | 个股详情、分时图 |
| P2 | 参数优化 | 网格搜索/遗传算法 |

### 8.2 中期计划

| 优先级 | 任务 | 说明 |
|--------|------|------|
| P1 | 实盘交易对接 | QMT/券商API |
| P1 | 风险管理系统 | 仓位管理、止损止盈 |
| P2 | 更多策略 | 日内策略、高频策略 |
| P2 | 用户登录 | 认证和权限管理 |

### 8.3 长期计划

| 优先级 | 任务 | 说明 |
|--------|------|------|
| P2 | 机器学习策略 | LSTM、强化学习 |
| P3 | 多账户支持 | 多账户管理 |
| P3 | 移动端适配 | 响应式设计 |

---

## 九、依赖清单

### 9.1 后端依赖 (requirements.txt)

```
fastapi==0.109.0
uvicorn[standard]==0.27.0
pandas==2.2.0
numpy==1.26.3
akshare==1.12.0
pydantic==2.5.3
pydantic-settings==2.1.0
loguru==0.7.2
httpx==0.26.0
scipy==1.12.0
websockets==16.0
```

### 9.2 前端依赖 (package.json)

```json
{
  "react": "^18.2.0",
  "react-dom": "^18.2.0",
  "react-router-dom": "^6.21.0",
  "axios": "^1.6.5",
  "antd": "^5.12.0",
  "@ant-design/icons": "^5.2.6",
  "lightweight-charts": "^4.1.0",
  "zustand": "^4.4.7"
}
```

---

## 十、联系方式

如有问题，请通过以下方式联系：

- 项目位置: D:/a-stock-quant
- GitHub: (待配置)

---

**报告生成时间**: 2026-05-27 16:45
**报告版本**: v1.0
