import { useState } from 'react'
import { Card, Table, Button, Tag, Space, Modal, Form, Input, Select, Typography, Row, Col } from 'antd'
import { PlusOutlined, EditOutlined, DeleteOutlined, PlayCircleOutlined } from '@ant-design/icons'

const { Title, Text, Paragraph } = Typography

const mockStrategies = [
  {
    id: 'dual_ma',
    name: '双均线策略',
    type: '趋势跟踪',
    description: '快慢均线交叉策略，适合趋势行情',
    status: 'active',
    params: { fast_period: 5, slow_period: 20 },
  },
  {
    id: 'rsi',
    name: 'RSI策略',
    type: '反转策略',
    description: 'RSI超买超卖反转策略',
    status: 'inactive',
    params: { rsi_period: 14, oversold: 30, overbought: 70 },
  },
  {
    id: 'bollinger',
    name: '布林带策略',
    type: '通道策略',
    description: '布林带上下轨突破策略',
    status: 'active',
    params: { period: 20, std_dev: 2 },
  },
]

const columns = [
  {
    title: '策略名称',
    dataIndex: 'name',
    key: 'name',
    render: (text: string) => <Text strong>{text}</Text>,
  },
  {
    title: '类型',
    dataIndex: 'type',
    key: 'type',
    render: (text: string) => <Tag color="blue">{text}</Tag>,
  },
  {
    title: '描述',
    dataIndex: 'description',
    key: 'description',
  },
  {
    title: '状态',
    dataIndex: 'status',
    key: 'status',
    render: (status: string) => (
      <Tag color={status === 'active' ? 'green' : 'default'}>
        {status === 'active' ? '启用' : '停用'}
      </Tag>
    ),
  },
  {
    title: '操作',
    key: 'action',
    render: () => (
      <Space>
        <Button type="link" icon={<EditOutlined />}>编辑</Button>
        <Button type="link" icon={<PlayCircleOutlined />}>回测</Button>
        <Button type="link" danger icon={<DeleteOutlined />}>删除</Button>
      </Space>
    ),
  },
]

const Strategy: React.FC = () => {
  const [modalVisible, setModalVisible] = useState(false)

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 16 }}>
        <Title level={4}>策略管理</Title>
        <Button type="primary" icon={<PlusOutlined />} onClick={() => setModalVisible(true)}>
          新建策略
        </Button>
      </div>

      <Card>
        <Table
          columns={columns}
          dataSource={mockStrategies}
          rowKey="id"
          pagination={false}
        />
      </Card>

      {/* 策略说明卡片 */}
      <Row gutter={[16, 16]} style={{ marginTop: 16 }}>
        <Col span={24}>
          <Card title="内置策略说明">
            <Paragraph>
              <Text strong>1. 双均线策略：</Text>
              快线上穿慢线买入，下穿卖出。适合趋势行情。
            </Paragraph>
            <Paragraph>
              <Text strong>2. RSI策略：</Text>
              RSI低于30买入，高于70卖出。适合震荡行情。
            </Paragraph>
            <Paragraph>
              <Text strong>3. 布林带策略：</Text>
              价格触及下轨买入，触及上轨卖出。适合均值回归行情。
            </Paragraph>
          </Card>
        </Col>
      </Row>

      <Modal
        title="新建策略"
        open={modalVisible}
        onCancel={() => setModalVisible(false)}
        onOk={() => setModalVisible(false)}
      >
        <Form layout="vertical">
          <Form.Item label="策略名称" required>
            <Input placeholder="请输入策略名称" />
          </Form.Item>
          <Form.Item label="策略类型" required>
            <Select placeholder="请选择策略类型">
              <Select.Option value="trend">趋势跟踪</Select.Option>
              <Select.Option value="reversal">反转策略</Select.Option>
              <Select.Option value="channel">通道策略</Select.Option>
              <Select.Option value="custom">自定义</Select.Option>
            </Select>
          </Form.Item>
          <Form.Item label="策略描述">
            <Input.TextArea rows={3} placeholder="请输入策略描述" />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default Strategy
