import { useEffect, useRef } from 'react'
import { createChart, IChartApi, ISeriesApi, CandlestickData, HistogramData, ColorType, Time } from 'lightweight-charts'

interface KlineData {
  date: string
  open: number
  close: number
  high: number
  low: number
  volume: number
}

interface KlineChartProps {
  data: KlineData[]
  width?: number
  height?: number
}

const KlineChart: React.FC<KlineChartProps> = ({ data, width = 800, height = 400 }) => {
  const chartContainerRef = useRef<HTMLDivElement>(null)
  const chartRef = useRef<IChartApi | null>(null)
  const candlestickSeriesRef = useRef<ISeriesApi<'Candlestick'> | null>(null)
  const volumeSeriesRef = useRef<ISeriesApi<'Histogram'> | null>(null)

  useEffect(() => {
    if (!chartContainerRef.current) return

    // 创建图表
    const chart = createChart(chartContainerRef.current, {
      width,
      height,
      layout: {
        background: { type: ColorType.Solid, color: '#ffffff' },
        textColor: '#333',
      },
      grid: {
        vertLines: { color: '#f0f0f0' },
        horzLines: { color: '#f0f0f0' },
      },
      crosshair: {
        mode: 0,
      },
      rightPriceScale: {
        borderColor: '#e0e0e0',
      },
      timeScale: {
        borderColor: '#e0e0e0',
        timeVisible: false,
      },
    })

    chartRef.current = chart

    // 添加K线系列
    const candlestickSeries = chart.addCandlestickSeries({
      upColor: '#f5222d',
      downColor: '#52c41a',
      borderUpColor: '#f5222d',
      borderDownColor: '#52c41a',
      wickUpColor: '#f5222d',
      wickDownColor: '#52c41a',
    })

    candlestickSeriesRef.current = candlestickSeries

    // 添加成交量系列
    const volumeSeries = chart.addHistogramSeries({
      color: '#26a69a',
      priceFormat: {
        type: 'volume',
      },
      priceScaleId: '',
    })

    volumeSeriesRef.current = volumeSeries

    // 设置成交量系列的位置
    volumeSeries.priceScale().applyOptions({
      scaleMargins: {
        top: 0.8,
        bottom: 0,
      },
    })

    return () => {
      chart.remove()
    }
  }, [width, height])

  useEffect(() => {
    if (!data || data.length === 0 || !candlestickSeriesRef.current || !volumeSeriesRef.current) return

    // 转换K线数据
    const candlestickData: CandlestickData[] = data.map(item => ({
      time: item.date as Time,
      open: item.open,
      high: item.high,
      low: item.low,
      close: item.close,
    }))

    // 转换成交量数据
    const volumeData: HistogramData[] = data.map(item => ({
      time: item.date as Time,
      value: item.volume,
      color: item.close >= item.open ? 'rgba(245, 34, 45, 0.5)' : 'rgba(82, 196, 26, 0.5)',
    }))

    // 设置数据
    candlestickSeriesRef.current.setData(candlestickData)
    volumeSeriesRef.current.setData(volumeData)

    // 自动调整视图
    chartRef.current?.timeScale().fitContent()
  }, [data])

  return <div ref={chartContainerRef} />
}

export default KlineChart
