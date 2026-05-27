import { create } from 'zustand'

interface AppState {
  // 用户信息
  user: any

  // 自选股列表
  watchlist: string[]

  // 当前选中的股票
  selectedStock: string | null

  // 策略列表
  strategies: any[]

  // Actions
  setUser: (user: any) => void
  setWatchlist: (list: string[]) => void
  addToWatchlist: (code: string) => void
  removeFromWatchlist: (code: string) => void
  setSelectedStock: (code: string | null) => void
  setStrategies: (strategies: any[]) => void
}

const useStore = create<AppState>((set) => ({
  // 初始状态
  user: null,
  watchlist: ['600519', '300750', '601318', '000858', '002594'],
  selectedStock: null,
  strategies: [],

  // Actions
  setUser: (user) => set({ user }),

  setWatchlist: (list) => set({ watchlist: list }),

  addToWatchlist: (code) =>
    set((state) => ({
      watchlist: [...state.watchlist, code],
    })),

  removeFromWatchlist: (code) =>
    set((state) => ({
      watchlist: state.watchlist.filter((c) => c !== code),
    })),

  setSelectedStock: (code) => set({ selectedStock: code }),

  setStrategies: (strategies) => set({ strategies }),
}))

export default useStore
