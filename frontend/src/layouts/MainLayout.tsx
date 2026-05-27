import { useState } from 'react'
import { Outlet, useNavigate, useLocation } from 'react-router-dom'
import { Layout, Menu, theme, Typography } from 'antd'
import {
  DashboardOutlined,
  StockOutlined,
  ExperimentOutlined,
  LineChartOutlined,
  SettingOutlined,
} from '@ant-design/icons'

const { Header, Sider, Content } = Layout
const { Title } = Typography

const menuItems = [
  {
    key: '/dashboard',
    icon: <DashboardOutlined />,
    label: '交易看板',
  },
  {
    key: '/market',
    icon: <StockOutlined />,
    label: '行情数据',
  },
  {
    key: '/strategy',
    icon: <ExperimentOutlined />,
    label: '策略管理',
  },
  {
    key: '/backtest',
    icon: <LineChartOutlined />,
    label: '回测系统',
  },
  {
    key: '/settings',
    icon: <SettingOutlined />,
    label: '系统设置',
  },
]

const MainLayout: React.FC = () => {
  const [collapsed, setCollapsed] = useState(false)
  const navigate = useNavigate()
  const location = useLocation()
  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken()

  const onMenuClick = (info: { key: string }) => {
    navigate(info.key)
  }

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider
        collapsible
        collapsed={collapsed}
        onCollapse={setCollapsed}
        theme="dark"
      >
        <div style={{ height: 64, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <Title level={4} style={{ color: '#fff', margin: 0 }}>
            {collapsed ? 'AQ' : 'A股量化'}
          </Title>
        </div>
        <Menu
          theme="dark"
          defaultSelectedKeys={['/dashboard']}
          selectedKeys={[location.pathname]}
          mode="inline"
          items={menuItems}
          onClick={onMenuClick}
        />
      </Sider>
      <Layout>
        <Header style={{ padding: '0 24px', background: colorBgContainer }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Title level={4} style={{ margin: 0 }}>
              A股量化交易系统
            </Title>
            <span style={{ color: '#666' }}>
              {new Date().toLocaleString('zh-CN')}
            </span>
          </div>
        </Header>
        <Content style={{ margin: '16px' }}>
          <div
            style={{
              padding: 24,
              minHeight: 360,
              background: colorBgContainer,
              borderRadius: borderRadiusLG,
            }}
          >
            <Outlet />
          </div>
        </Content>
      </Layout>
    </Layout>
  )
}

export default MainLayout
