# A股量化交易系统

基于 Python + FastAPI + React 的 A股量化交易平台，支持日内交易和量化策略回测。

## 功能特性

- 📊 **实时行情展示** - K线图、技术指标、实时数据推送
- 📈 **量化策略回测** - 双均线、RSI、布林带等内置策略
- 🤖 **自动化交易** - 策略信号生成、回测验证
- ⚠️ **风险管理** - 最大回撤、夏普比率、胜率分析
- 📱 **交易看板** - Dashboard、持仓管理

## 技术栈

### 后端
- Python 3.11+
- FastAPI
- AKShare (A股数据)
- pandas / numpy

### 前端
- React 18
- TypeScript
- Vite
- Ant Design
- Zustand

## 快速开始

### 1. 启动后端

```bash
cd backend
pip install -r requirements.txt
python run.py
```

后端将在 http://localhost:8000 启动

### 2. 启动前端

```bash
cd frontend
npm install
npm run dev
```

前端将在 http://localhost:5173 启动

### 3. 访问系统

- 交易看板: http://localhost:5173/dashboard
- 行情数据: http://localhost:5173/market
- 策略管理: http://localhost:5173/strategy
- 回测系统: http://localhost:5173/backtest

## 内置策略

| 策略 | 类型 | 说明 |
|------|------|------|
| 双均线策略 | 趋势跟踪 | 快慢均线交叉 |
| RSI策略 | 反转策略 | 超买超卖反转 |
| 布林带策略 | 通道策略 | 价格通道突破 |

## 技术指标

支持 22 个技术指标：
- MA均线 (5/10/20/60)
- EMA均线 (12/26)
- MACD (DIF/DEA/HIST)
- RSI (14)
- KDJ (K/D/J)
- 布林带 (上/中/下)
- ATR (14)
- OBV
- 量比
- 成交量均线

## API文档

启动后端后访问: http://localhost:8000/docs

## 项目结构

```
a-stock-quant/
├── backend/          # 后端服务
│   ├── app/
│   │   ├── api/      # API接口
│   │   ├── core/     # 核心配置
│   │   └── services/ # 业务服务
│   └── requirements.txt
│
├── frontend/         # 前端应用
│   └── src/
│       ├── pages/    # 页面组件
│       └── services/ # API服务
│
├── strategies/       # 策略库
├── data/             # 数据存储
└── docs/             # 文档
```

## 文档

- [完整开发报告](docs/development-report.md)
- [最终测试报告](docs/test-report-final.md)

## 测试结果

| 策略 | 总收益 | 最大回撤 | 夏普比率 | 胜率 |
|------|--------|----------|----------|------|
| 双均线 | -3.13% | -8.61% | -0.73 | 20% |
| RSI | +1.67% | -8.33% | -0.03 | 50% |
| 布林带 | +3.01% | -9.37% | 0.13 | 67% |

## 许可证

MIT License
