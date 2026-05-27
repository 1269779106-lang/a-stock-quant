import axios from 'axios'

// 创建axios实例
const api = axios.create({
  baseURL: '/api/v1',
  timeout: 60000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

// 行情API
export const marketApi = {
  // 获取股票列表
  getStockList: (params?: { market?: string }) =>
    api.get('/market/stock_list', { params }),

  // 获取K线数据（含技术指标）
  getKlineData: (stockCode: string, params: {
    period?: string
    start_date?: string
    end_date?: string
    adjust?: string
  }) => api.get(`/market/kline/${stockCode}`, { params }),

  // 获取实时行情
  getRealtimeQuote: (stockCode: string) =>
    api.get(`/market/realtime/${stockCode}`),
}

// 策略API
export const strategyApi = {
  // 获取策略列表
  getStrategyList: () =>
    api.get('/strategy/list'),

  // 获取策略详情
  getStrategyDetail: (strategyId: string) =>
    api.get(`/strategy/${strategyId}`),

  // 更新策略参数
  updateStrategy: (strategyId: string, params: Record<string, any>) =>
    api.put(`/strategy/${strategyId}`, null, { params }),
}

// 回测API
export const backtestApi = {
  // 运行回测
  runBacktest: (params: {
    strategy_id: string
    stock_code: string
    start_date: string
    end_date: string
    initial_capital?: number
    commission?: number
    slippage?: number
  }) => api.post('/backtest/run', null, { params }),

  // 获取回测历史
  getBacktestHistory: (params?: {
    strategy_id?: string
    page?: number
    page_size?: number
  }) => api.get('/backtest/history', { params }),
}

export default api
