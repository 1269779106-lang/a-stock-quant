import { useState } from 'react'
import { Card, Form, Input, Select, Button, DatePicker, InputNumber, Statistic, Row, Col, Typography, Space, Divider, message, Spin } from 'antd'
import { LineChartOutlined, ExperimentOutlined } from '@ant-design/icons'
import { backtestApi } from '../services/api'
import dayjs from 'dayjs'

const { Title, Text } = Typography
const { RangePicker } = DatePicker

const Backtest: React.FC = () => {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)

  const onFinish = async (values: any) => {
    setLoading(true)
    try {
      const params = {
        strategy_id: values.strategy,
        stock_code: values.stockCode,
        start_date: values.dateRange[0].format('YYYY-MM-DD'),
        end_date: values.dateRange[1].format('YYYY-MM-DD'),
        initial_capital: values.capital || 1000000,
        commission: values.commission || 0.0003,
        slippage: values.slippage || 0.001,
      }

      const res: any = await backtestApi.runBacktest(params)

      if (res.error) {
        message.error(res.error)
        return
      }

      setResult(res)
      message.success('回测完成')
    } catch (error) {
      console.error('回测失败:', error)
      message.error('回测失败，请检查网络连接')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <Title level={4}>回测系统</Title>

      <Row gutter={[16, 16]}>
        <Col xs={24} lg={8}>
          <Card title="回测参数">
            <Form
              layout="vertical"
              onFinish={onFinish}
              initialValues={{
                strategy: 'dual_ma',
                stockCode: '600519',
                capital: 1000000,
                commission: 0.0003,
                slippage: 0.001,
              }}
            >
              <Form.Item label="选择策略" name="strategy" required>
                <Select placeholder="请选择策略">
                  <Select.Option value="dual_ma">双均线策略</Select.Option>
                  <Select.Option value="rsi">RSI策略</Select.Option>
                  <Select.Option value="bollinger">布林带策略</Select.Option>
                </Select>
              </Form.Item>

              <Form.Item label="股票代码" name="stockCode" required>
                <Input placeholder="如: 600519" />
              </Form.Item>

              <Form.Item label="回测周期" name="dateRange" required>
                <RangePicker
                  style={{ width: '100%' }}
                  defaultValue={[dayjs('2026-01-01'), dayjs('2026-05-27')]}
                />
              </Form.Item>

              <Form.Item label="初始资金" name="capital">
                <InputNumber
                  style={{ width: '100%' }}
                  min={10000}
                  step={100000}
                  formatter={(value) => `¥ ${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
                />
              </Form.Item>

              <Form.Item label="手续费率" name="commission">
                <InputNumber
                  style={{ width: '100%' }}
                  min={0}
                  max={0.01}
                  step={0.0001}
                />
              </Form.Item>

              <Form.Item label="滑点" name="slippage">
                <InputNumber
                  style={{ width: '100%' }}
                  min={0}
                  max={0.01}
                  step={0.001}
                />
              </Form.Item>

              <Form.Item>
                <Button
                  type="primary"
                  htmlType="submit"
                  loading={loading}
                  icon={<ExperimentOutlined />}
                  block
                >
                  开始回测
                </Button>
              </Form.Item>
            </Form>
          </Card>
        </Col>

        <Col xs={24} lg={16}>
          <Card title="回测结果">
            <Spin spinning={loading}>
              {result ? (
                <>
                  <Row gutter={[16, 16]}>
                    <Col xs={12} sm={8}>
                      <Statistic
                        title="总收益率"
                        value={result.total_return}
                        precision={2}
                        suffix="%"
                        valueStyle={{ color: result.total_return > 0 ? '#3f8600' : '#cf1322' }}
                      />
                    </Col>
                    <Col xs={12} sm={8}>
                      <Statistic
                        title="年化收益"
                        value={result.annual_return}
                        precision={2}
                        suffix="%"
                        valueStyle={{ color: result.annual_return > 0 ? '#3f8600' : '#cf1322' }}
                      />
                    </Col>
                    <Col xs={12} sm={8}>
                      <Statistic
                        title="最大回撤"
                        value={result.max_drawdown}
                        precision={2}
                        suffix="%"
                        valueStyle={{ color: '#cf1322' }}
                      />
                    </Col>
                    <Col xs={12} sm={8}>
                      <Statistic
                        title="夏普比率"
                        value={result.sharpe_ratio}
                        precision={2}
                      />
                    </Col>
                    <Col xs={12} sm={8}>
                      <Statistic
                        title="胜率"
                        value={result.win_rate}
                        precision={1}
                        suffix="%"
                      />
                    </Col>
                    <Col xs={12} sm={8}>
                      <Statistic
                        title="交易次数"
                        value={result.total_trades}
                        suffix="次"
                      />
                    </Col>
                  </Row>

                  <Divider />

                  <Row gutter={[16, 16]}>
                    <Col xs={12} sm={8}>
                      <Statistic
                        title="初始资金"
                        value={result.initial_capital}
                        precision={2}
                        prefix="¥"
                      />
                    </Col>
                    <Col xs={12} sm={8}>
                      <Statistic
                        title="最终资金"
                        value={result.final_capital}
                        precision={2}
                        prefix="¥"
                        valueStyle={{ color: result.final_capital > result.initial_capital ? '#3f8600' : '#cf1322' }}
                      />
                    </Col>
                    <Col xs={12} sm={8}>
                      <Statistic
                        title="盈亏比"
                        value={result.profit_loss_ratio}
                        precision={2}
                      />
                    </Col>
                  </Row>

                  <Divider />

                  <div style={{ height: 300, display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#fafafa', borderRadius: 8 }}>
                    <Space direction="vertical" align="center">
                      <LineChartOutlined style={{ fontSize: 48, color: '#1890ff' }} />
                      <Text type="secondary">资金曲线图（开发中）</Text>
                    </Space>
                  </div>
                </>
              ) : (
                <div style={{ height: 400, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <Space direction="vertical" align="center">
                    <ExperimentOutlined style={{ fontSize: 48, color: '#d9d9d9' }} />
                    <Text type="secondary">请设置参数后点击"开始回测"</Text>
                  </Space>
                </div>
              )}
            </Spin>
          </Card>
        </Col>
      </Row>
    </div>
  )
}

export default Backtest
