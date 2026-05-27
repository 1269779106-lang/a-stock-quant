import { useState, useEffect, useCallback } from 'react'
import { Card, Input, Table, Tag, Row, Col, Typography, Tabs, Space, Statistic, Spin, message } from 'antd'
import { SearchOutlined, ArrowUpOutlined, ArrowDownOutlined } from '@ant-design/icons'
import { marketApi } from '../services/api'
import wsService from '../services/websocket'

const { Title, Text } = Typography

interface StockData {
  code: string;
  name: string;
  price: number;
  change: number;
  pct_change: number;
  open: number;
  high: number;
  low: number;
  volume: number;
  amount: number;
}

const Market: React.FC = () => {
  const [searchCode, setSearchCode] = useState('')
  const [stockList, setStockList] = useState<any[]>([])
  const [realtimeData, setRealtimeData] = useState<Map<string, StockData>>(new Map())
  const [loading, setLoading] = useState(false)
  const [watchlist, setWatchlist] = useState<string[]>(['600519', '300750', '601318', '000858', '002594'])

  // 加载股票列表
  useEffect(() => {
    loadStockList()
  }, [])

  // 建立WebSocket连接
  useEffect(() => {
    // 连接市场数据WebSocket
    wsService.connect()

    // 订阅自选股数据
    watchlist.forEach(code => {
      wsService.subscribeStock(code, (data: StockData) => {
        setRealtimeData(prev => new Map(prev).set(code, data))
      })
    })

    return () => {
      wsService.disconnect()
    }
  }, [watchlist])

  const loadStockList = async () => {
    setLoading(true)
    try {
      const res: any = await marketApi.getStockList()
      if (res.data) {
        setStockList(res.data.slice(0, 50))
      }
    } catch (error) {
      console.error('获取股票列表失败:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = async () => {
    if (!searchCode) return

    setLoading(true)
    try {
      const res: any = await marketApi.getRealtimeQuote(searchCode)
      if (res.data) {
        setRealtimeData(prev => new Map(prev).set(searchCode, res.data))
        message.success(`已添加 ${searchCode} 到实时监控`)
      }
    } catch (error) {
      message.error('获取股票数据失败')
    } finally {
      setLoading(false)
    }
  }

  const columns = [
    {
      title: '代码',
      dataIndex: 'code',
      key: 'code',
      render: (text: string) => <Text code>{text}</Text>,
    },
    {
      title: '名称',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: '最新价',
      key: 'price',
      render: (_: any, record: any) => {
        const data = realtimeData.get(record.code)
        if (!data) return <Text type="secondary">--</Text>
        return (
          <Text style={{ color: data.change >= 0 ? '#f5222d' : '#52c41a', fontWeight: 'bold' }}>
            {data.price?.toFixed(2)}
          </Text>
        )
      },
    },
    {
      title: '涨跌幅',
      key: 'pct_change',
      render: (_: any, record: any) => {
        const data = realtimeData.get(record.code)
        if (!data) return <Text type="secondary">--</Text>
        const color = data.pct_change >= 0 ? '#f5222d' : '#52c41a'
        return (
          <Tag color={data.pct_change >= 0 ? 'red' : 'green'}>
            {data.pct_change >= 0 ? '+' : ''}{data.pct_change?.toFixed(2)}%
          </Tag>
        )
      },
    },
    {
      title: '涨跌额',
      key: 'change',
      render: (_: any, record: any) => {
        const data = realtimeData.get(record.code)
        if (!data) return <Text type="secondary">--</Text>
        return (
          <Text style={{ color: data.change >= 0 ? '#f5222d' : '#52c41a' }}>
            {data.change >= 0 ? '+' : ''}{data.change?.toFixed(2)}
          </Text>
        )
      },
    },
    {
      title: '开盘',
      key: 'open',
      render: (_: any, record: any) => {
        const data = realtimeData.get(record.code)
        return data ? <Text>{data.open?.toFixed(2)}</Text> : <Text type="secondary">--</Text>
      },
    },
    {
      title: '最高',
      key: 'high',
      render: (_: any, record: any) => {
        const data = realtimeData.get(record.code)
        return data ? <Text style={{ color: '#f5222d' }}>{data.high?.toFixed(2)}</Text> : <Text type="secondary">--</Text>
      },
    },
    {
      title: '最低',
      key: 'low',
      render: (_: any, record: any) => {
        const data = realtimeData.get(record.code)
        return data ? <Text style={{ color: '#52c41a' }}>{data.low?.toFixed(2)}</Text> : <Text type="secondary">--</Text>
      },
    },
    {
      title: '成交量',
      key: 'volume',
      render: (_: any, record: any) => {
        const data = realtimeData.get(record.code)
        if (!data) return <Text type="secondary">--</Text>
        return <Text>{(data.volume / 10000).toFixed(0)}万手</Text>
      },
    },
  ]

  return (
    <div>
      <Title level={4}>行情数据</Title>

      <Card style={{ marginBottom: 16 }}>
        <Space>
          <Input
            placeholder="输入股票代码搜索 (如: 600519)"
            prefix={<SearchOutlined />}
            value={searchCode}
            onChange={(e) => setSearchCode(e.target.value)}
            onPressEnter={handleSearch}
            style={{ width: 300 }}
          />
          <button onClick={handleSearch} style={{ padding: '4px 16px' }}>
            搜索
          </button>
        </Space>
      </Card>

      {/* 实时行情概览 */}
      <Row gutter={[16, 16]} style={{ marginBottom: 16 }}>
        {watchlist.slice(0, 4).map(code => {
          const data = realtimeData.get(code)
          return (
            <Col xs={12} sm={6} key={code}>
              <Card size="small">
                <Statistic
                  title={data?.name || code}
                  value={data?.price || 0}
                  precision={2}
                  prefix="¥"
                  suffix={
                    <Text style={{ fontSize: 14, color: (data?.pct_change || 0) >= 0 ? '#f5222d' : '#52c41a' }}>
                      {(data?.pct_change || 0) >= 0 ? '+' : ''}{(data?.pct_change || 0).toFixed(2)}%
                    </Text>
                  }
                  valueStyle={{ color: (data?.change || 0) >= 0 ? '#f5222d' : '#52c41a' }}
                />
              </Card>
            </Col>
          )
        })}
      </Row>

      <Tabs
        defaultActiveKey="watchlist"
        items={[
          {
            key: 'watchlist',
            label: '自选股',
            children: (
              <Card>
                <Spin spinning={loading}>
                  <Table
                    columns={columns}
                    dataSource={stockList.filter(s => watchlist.includes(s.code))}
                    rowKey="code"
                    pagination={false}
                    size="small"
                  />
                </Spin>
              </Card>
            ),
          },
          {
            key: 'all',
            label: '全部A股',
            children: (
              <Card>
                <Spin spinning={loading}>
                  <Table
                    columns={columns}
                    dataSource={stockList}
                    rowKey="code"
                    pagination={{ pageSize: 20 }}
                    size="small"
                  />
                </Spin>
              </Card>
            ),
          },
        ]}
      />
    </div>
  )
}

export default Market
