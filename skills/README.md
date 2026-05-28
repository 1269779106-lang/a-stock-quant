# 量化交易技能库

**下载日期**: 2026年5月28日

---

## 一、已下载技能仓库

### 1. Ricko12vPL/claude-code-skills
**路径**: `skills/claude-code-skills/`

**包含技能**:
- **quantitative-finance/** - 量化金融与交易
  - Senior-Quantitative-Developer.SKILL.md - 高级量化开发
  - Senior-Quantitative-Researcher.SKILL.md - 高级量化研究
  - Senior-Quantitative-Trader.SKILL.md - 高级量化交易
  - Senior-Systematic-Trader.SKILL.md - 高级系统化交易
  - SKILL.md - 量化金融完整框架

- **python-programming/** - Python编程规范
  - SKILL.md - PEP 8/257/484 规范

- **software-engineering/** - 软件工程
  - SOLID原则、设计模式、Clean Code

- **machine-learning/** - 机器学习工作流

### 2. tradermonty/claude-trading-skills
**路径**: `skills/claude-trading-skills/`

**包含技能**:
- **skills/** - 交易技能包
  - backtest-expert - 回测专家
  - breadth-chart-analyst - 宽度图表分析
  - breakout-trade-planner - 突破交易规划
  - canslim-screener - CANSLIM筛选
  - data-quality-checker - 数据质量检查
  - dividend-growth-pullback-screener - 股息增长回调筛选
  - downtrend-duration-analyzer - 下跌趋势分析
  - earnings-calendar - 财报日历
  - earnings-trade-analyzer - 财报交易分析
  - economic-calendar-fetcher - 经济日历获取
  - edge-candidate-agent - 边际候选代理
  - edge-concept-synthesizer - 边际概念合成
  - edge-hint-extractor - 边际提示提取
  - edge-pipeline-orchestrator - 边际管道编排
  - edge-signal-aggregator - 边际信号聚合
  - edge-strategy-designer - 边际策略设计

- **agents/** - 代理
  - scenario-analyst.md - 场景分析
  - strategy-reviewer.md - 策略审查

- **skillsets/** - 技能集
  - core-portfolio.yaml - 核心组合
  - market-regime.yaml - 市场状态
  - swing-opportunity.yaml - 摆动机会
  - trade-memory.yaml - 交易记忆

---

## 二、如何使用

### 量化金融技能
```python
# 使用量化研究框架
from skills.claude_code_skills.quantitative_finance import AlphaResearch

# 初始化研究
research = AlphaResearch(
    universe=['588000', '515880', '159952'],
    start_date='2026-01-01',
    end_date='2026-05-28'
)

# 加载数据
data = research.load_data()

# 生成信号
signals = research.generate_alpha(params={'lookback': 20, 'zscore_threshold': 2.0})

# 回测
results = research.backtest(signals, transaction_costs=0.001)
```

### 交易技能
```python
# 使用回测专家
from skills.claude_trading_skills.skills.backtest_expert import BacktestExpert

# 初始化回测
expert = BacktestExpert()

# 运行回测
results = expert.run_backtest(
    strategy='dual_ma',
    stock_code='588000',
    start_date='2026-01-01',
    end_date='2026-05-28'
)
```

---

## 三、技能应用场景

### 1. 策略开发
- 使用 **Senior-Quantitative-Researcher** 进行Alpha研究
- 使用 **edge-strategy-designer** 设计边际策略
- 使用 **backtest-expert** 进行回测验证

### 2. 风险管理
- 使用 **Senior-Quantitative-Trader** 进行风险管理
- 使用 **scenario-analyst** 进行场景分析
- 使用 **strategy-reviewer** 审查策略

### 3. 数据分析
- 使用 **data-quality-checker** 检查数据质量
- 使用 **breadth-chart-analyst** 分析市场宽度
- 使用 **economic-calendar-fetcher** 获取经济日历

### 4. 交易执行
- 使用 **breakout-trade-planner** 规划突破交易
- 使用 **earnings-trade-analyzer** 分析财报交易
- 使用 **downtrend-duration-analyzer** 分析下跌趋势

---

## 四、集成到项目

### 步骤1: 配置环境
```bash
# 安装依赖
pip install -r skills/claude-code-skills/requirements.txt
pip install -r skills/claude-trading-skills/requirements.txt
```

### 步骤2: 导入技能
```python
# 在项目中导入技能
import sys
sys.path.append('skills/claude-code-skills')
sys.path.append('skills/claude-trading-skills')
```

### 步骤3: 使用技能
```python
# 使用量化研究框架
from quantitative_finance import AlphaResearch

# 使用交易技能
from skills.backtest_expert import BacktestExpert
```

---

## 五、参考文档

### Ricko12vPL/claude-code-skills
- README: `skills/claude-code-skills/README.md`
- 量化金融: `skills/claude-code-skills/quantitative-finance/SKILL.md`
- Python规范: `skills/claude-code-skills/python-programming/SKILL.md`

### tradermonty/claude-trading-skills
- README: `skills/claude-trading-skills/README.md`
- CLAUDE.md: `skills/claude-trading-skills/CLAUDE.md`
- 技能索引: `skills/claude-trading-skills/skills-index.yaml`

---

## 六、注意事项

1. **许可证**: 请遵守各仓库的许可证要求
2. **依赖**: 需要安装相应的Python依赖
3. **数据**: 需要确保数据源可用
4. **测试**: 建议先在测试环境验证

---

*以上技能库已下载到本地，可根据需要使用。*
