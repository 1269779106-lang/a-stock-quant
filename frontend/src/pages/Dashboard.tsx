import { useState, useEffect } from 'react'
import { Row, Col, Card, Statistic, Table, Tag, Typography, Spin } from 'antd'
import {
  ArrowUpOutlined,
  ArrowDownOutlined,
  StockOutlined,
  RiseOutlined,
} from '@ant-design/icons'
import { marketApi } from '../services/api'
import wsService from '../services/websocket'

const { Title, Text } = Typography

interface StockData {
  code: string;
  name: string;
  price: number;
  change: number;
  pct_change: number;
  volume: number;
}

const Dashboard: React.FC = () => {
  const [loading, setLoading] = useState(false)
  const [stockList, setStockList] = useState<any[]>([])
  const [realtimeData, setRealtimeData] = useState<Map<string, StockData>>(new Map())
  const watchlist = ['600519', '300750', '601318', '000858', '002594']

  // 加载股票列表
  useEffect(() => {
    loadStockList()
  }, [])

  // 建立WebSocket连接
  useEffect(() => {
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
  }, [])

  const loadStockList = async () => {
    setLoading(true)
    try {
      const res: any = await marketApi.getStockList()
      if (res.data) {
        setStockList(res.data.slice(0, 10))
      }
    } catch (error) {
      console.error('获取股票列表失败:', error)
    } finally {
      setLoading(false)
    }
  }

  // 计算总资产（模拟）
  const totalAssets = 1234567.89
  const todayProfit = 12345.67
  const todayProfitPercent = (todayProfit / totalAssets * 100).toFixed(2)

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
            ¥{data.price?.toFixed(2)}
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
        return (
          <Tag color={data.pct_change >= 0 ? 'red' : 'green'}>
            {data.pct_change >= 0 ? '+' : ''}{data.pct_change?.toFixed(2)}%
          </Tag>
        )
      },
    },
  ]

  return (
    <div>
      <Title level={4}>交易看板</Title>

      {/* 统计卡片 */}
      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="账户总资产"
              value={totalAssets}
              precision={2}
              prefix="¥"
              suffix={<RiseOutlined style={{ color: '#3f8600' }} />}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="今日盈亏"
              value={todayProfit}
              precision={2}
              prefix="¥"
              valueStyle={{ color: '#3f8600' }}
              suffix={
                <Text style={{ fontSize: 14, color: '#3f8600' }}>
                  +{todayProfitPercent}%
                </Text>
              }
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="持仓数量"
              value={5}
              suffix="只"
              prefix={<StockOutlined />}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="可用资金"
              value={456789.00}
              precision={2}
              prefix="¥"
            />
          </Card>
        </Col>
      </Row>

      {/* 自选股实时行情 */}
      <Row gutter={[16, 16]}>
        <Col xs={24} lg={14}>
          <Card title="自选股实时行情" extra={<Text type="secondary">实时更新中</Text>}>
            <Spin spinning={loading}>
              <Table
                columns={columns}
                dataSource={stockList}
                rowKey="code"
                pagination={false}
                size="small"
              />
            </Spin>
          </Card>
        </Col>

        <Col xs={24} lg={10}>
          <Card title="持仓明细">
            <Table
              columns={[
                { title: '股票', dataIndex: 'name', key: 'name' },
                { title: '数量', dataIndex: 'shares', key: 'shares' },
                {
                  title: '盈亏',
                  dataIndex: 'profit',
                  key: 'profit',
                  render: (val: number) => (
                    <Text style={{ color: val >= 0 ? '#f5222d' : '#52c41a' }}>
                      {val >= 0 ? '+' : ''}{val?.toFixed(2)}
                    </Text>
                  ),
                },
              ]}
              dataSource={[
                { code: '600519', name: '贵州茅台', shares: 100, profit: 3600 },
                { code: '300750', name: '宁德时代', shares: 500, profit: -3250 },
              ]}
              rowKey="code"
              pagination={false}
              size="small"
            />
          </Card>
        </Col>
      </Row>

      {/* 市场概况 */}
      <Row gutter={[16, 16]} style={{ marginTop: 16 }}>
        <Col span={24}>
          <Card title="市场概况">
            <Row gutter={[16, 16]}>
              <Col xs={12} sm={6}>
                <Statistic
                  title="上证指数"
                  value={3168.45}
                  precision={2}
                  valueStyle={{ color: '#3f8600' }}
                  prefix={<ArrowUpOutlined />}
                  suffix="+0.62%"
                />
              </Col>
              <Col xs={12} sm={6}>
                <Statistic
                  title="深证成指"
                  value={10234.56}
                  precision={2}
                  valueStyle={{ color: '#3f8600' }}
                  prefix={<ArrowUpOutlined />}
                  suffix="+0.85%"
                />
              </Col>
              <Col xs={12} sm={6}>
                <Statistic
                  title="创业板指"
                  value={2156.78}
                  precision={2}
                  valueStyle={{ color: '#3f8600' }}
                  prefix={<ArrowUpOutlined />}
                  suffix="+1.23%"
                />
              </Col>
              <Col xs={12} sm={6}>
                <Statistic
                  title="科创50"
                  value={987.65}
                  precision={2}
                  valueStyle={{ color: '#cf1322' }}
                  prefix={<ArrowDownOutlined />}
                  suffix="-0.34%"
                />
              </Col>
            </Row>
          </Card>
        </Col>
      </Row>
    </div>
  )
}

export default Dashboard
