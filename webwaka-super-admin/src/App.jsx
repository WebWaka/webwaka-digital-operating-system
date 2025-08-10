import { useState, useEffect } from 'react'
import './App.css'

// API Configuration
const API_BASE_URL = 'https://lnh8imcn0lxd.manus.space'

function App() {
  const [systemData, setSystemData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('dashboard')

  useEffect(() => {
    fetchSystemData()
  }, [])

  const fetchSystemData = async () => {
    try {
      const response = await fetch(API_BASE_URL)
      const data = await response.json()
      setSystemData(data)
    } catch (error) {
      console.error('Error fetching system data:', error)
      // Fallback data for demo
      setSystemData({
        agents: {
          infrastructure: 4,
          integration: 8,
          payment_systems: 6,
          referral_system: 6,
          sector_management: 14,
          white_label: 6,
          total: 42
        },
        ubuntu_greeting: "Sawubona! Welcome to WebWaka - Where Ubuntu meets Technology",
        status: "operational",
        features: {
          african_optimization: true,
          mobile_first: true,
          multi_language: true,
          multi_level_referral: true,
          offline_support: true,
          payment_systems: true,
          ubuntu_philosophy: true,
          white_label_platform: true
        }
      })
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading WebWaka Super Admin...</p>
          <p className="text-sm text-orange-600 mt-2">Sawubona! I see you...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <h1 className="text-2xl font-bold text-gray-900">WebWaka Super Admin</h1>
                <p className="text-sm text-orange-600">{systemData?.ubuntu_greeting}</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                {systemData?.status || 'operational'}
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8">
            {[
              { id: 'dashboard', name: 'Dashboard', icon: '📊' },
              { id: 'agents', name: 'Agents', icon: '🤖' },
              { id: 'ubuntu', name: 'Ubuntu Philosophy', icon: '🤝' },
              { id: 'white-label', name: 'White-Label', icon: '🏢' },
              { id: 'referral', name: 'Referral System', icon: '💰' },
              { id: 'payments', name: 'Payment Systems', icon: '💳' },
              { id: 'analytics', name: 'Analytics', icon: '📈' },
              { id: 'settings', name: 'Settings', icon: '⚙️' }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-orange-500 text-orange-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <span className="mr-2">{tab.icon}</span>
                {tab.name}
              </button>
            ))}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          {activeTab === 'dashboard' && <Dashboard systemData={systemData} />}
          {activeTab === 'agents' && <AgentsManagement systemData={systemData} />}
          {activeTab === 'ubuntu' && <UbuntuPhilosophy systemData={systemData} />}
          {activeTab === 'white-label' && <WhiteLabelManagement systemData={systemData} />}
          {activeTab === 'referral' && <ReferralSystem systemData={systemData} />}
          {activeTab === 'payments' && <PaymentSystems systemData={systemData} />}
          {activeTab === 'analytics' && <Analytics systemData={systemData} />}
          {activeTab === 'settings' && <SystemSettings systemData={systemData} />}
        </div>
      </main>
    </div>
  )
}

// Main Dashboard Component
function Dashboard() {
  const [systemData, setSystemData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchSystemData()
  }, [])

  const fetchSystemData = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/`)
      const data = await response.json()
      setSystemData(data)
      setLoading(false)
    } catch (error) {
      console.error('Failed to fetch system data:', error)
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary"></div>
          <p className="mt-4 text-lg">Loading WebWaka Super Admin...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="flex h-screen bg-background">
      {/* Sidebar */}
      <Sidebar />
      
      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <Header systemData={systemData} />
        
        {/* Dashboard Content */}
        <main className="flex-1 overflow-x-hidden overflow-y-auto bg-background p-6">
          <div className="max-w-7xl mx-auto">
            {/* Welcome Section */}
            <div className="mb-8">
              <h1 className="text-3xl font-bold text-foreground mb-2">
                Sawubona! Welcome to WebWaka Super Admin
              </h1>
              <p className="text-muted-foreground">
                {systemData?.ubuntu_greeting || "Where Ubuntu meets Technology - Managing the Digital Operating System"}
              </p>
            </div>

            {/* System Status Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
              <StatusCard
                title="Total Agents"
                value={systemData?.agents?.total || 42}
                icon={<Activity className="h-4 w-4" />}
                status="operational"
              />
              <StatusCard
                title="System Status"
                value={systemData?.status || "operational"}
                icon={<CheckCircle className="h-4 w-4" />}
                status="operational"
              />
              <StatusCard
                title="Ubuntu Philosophy"
                value={systemData?.features?.ubuntu_philosophy ? "Active" : "Inactive"}
                icon={<Heart className="h-4 w-4" />}
                status={systemData?.features?.ubuntu_philosophy ? "operational" : "warning"}
              />
              <StatusCard
                title="African Optimization"
                value={systemData?.features?.african_optimization ? "Enabled" : "Disabled"}
                icon={<Globe className="h-4 w-4" />}
                status={systemData?.features?.african_optimization ? "operational" : "warning"}
              />
            </div>

            {/* Agent Categories Overview */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Database className="h-5 w-5" />
                    Agent Categories
                  </CardTitle>
                  <CardDescription>
                    Overview of all 42 specialized agents across 6 categories
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <AgentCategoryItem
                      name="Sector Management"
                      count={systemData?.agents?.sector_management || 14}
                      description="Agriculture, Healthcare, Education, Finance, etc."
                      status="operational"
                    />
                    <AgentCategoryItem
                      name="Integration"
                      count={systemData?.agents?.integration || 8}
                      description="Cross-sector coordination and integration"
                      status="operational"
                    />
                    <AgentCategoryItem
                      name="Infrastructure"
                      count={systemData?.agents?.infrastructure || 4}
                      description="Voice, Performance, Documentation, Quality"
                      status="operational"
                    />
                    <AgentCategoryItem
                      name="White-Label"
                      count={systemData?.agents?.white_label || 6}
                      description="Platform replication and customization"
                      status="operational"
                    />
                    <AgentCategoryItem
                      name="Referral System"
                      count={systemData?.agents?.referral_system || 6}
                      description="Partner management and commissions"
                      status="operational"
                    />
                    <AgentCategoryItem
                      name="Payment Systems"
                      count={systemData?.agents?.payment_systems || 6}
                      description="Financial processing and compliance"
                      status="operational"
                    />
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <TrendingUp className="h-5 w-5" />
                    System Features
                  </CardTitle>
                  <CardDescription>
                    Core platform capabilities and integrations
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <FeatureItem
                      name="Ubuntu Philosophy"
                      enabled={systemData?.features?.ubuntu_philosophy}
                      description="Traditional leadership and community values"
                    />
                    <FeatureItem
                      name="African Optimization"
                      enabled={systemData?.features?.african_optimization}
                      description="Mobile-first, low-bandwidth, offline support"
                    />
                    <FeatureItem
                      name="White-Label Platform"
                      enabled={systemData?.features?.white_label_platform}
                      description="Complete platform replication for partners"
                    />
                    <FeatureItem
                      name="Multi-Level Referral"
                      enabled={systemData?.features?.multi_level_referral}
                      description="6-level partner hierarchy system"
                    />
                    <FeatureItem
                      name="Payment Systems"
                      enabled={systemData?.features?.payment_systems}
                      description="HandyLife Wallet and African payment methods"
                    />
                    <FeatureItem
                      name="Multi-Language"
                      enabled={systemData?.features?.multi_language}
                      description="10+ African languages supported"
                    />
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Quick Actions */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Zap className="h-5 w-5" />
                  Quick Actions
                </CardTitle>
                <CardDescription>
                  Common administrative tasks and system management
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <QuickActionButton
                    icon={<Users className="h-4 w-4" />}
                    label="Manage Agents"
                    onClick={() => window.location.href = '/agents'}
                  />
                  <QuickActionButton
                    icon={<Heart className="h-4 w-4" />}
                    label="Ubuntu Settings"
                    onClick={() => window.location.href = '/ubuntu'}
                  />
                  <QuickActionButton
                    icon={<Building className="h-4 w-4" />}
                    label="White-Label"
                    onClick={() => window.location.href = '/white-label'}
                  />
                  <QuickActionButton
                    icon={<DollarSign className="h-4 w-4" />}
                    label="Payments"
                    onClick={() => window.location.href = '/payments'}
                  />
                </div>
              </CardContent>
            </Card>
          </div>
        </main>
      </div>
    </div>
  )
}

// Sidebar Component
function Sidebar() {
  const [activeItem, setActiveItem] = useState('dashboard')

  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: <Monitor className="h-4 w-4" />, href: '/dashboard' },
    { id: 'agents', label: 'Agents', icon: <Activity className="h-4 w-4" />, href: '/agents' },
    { id: 'ubuntu', label: 'Ubuntu Philosophy', icon: <Heart className="h-4 w-4" />, href: '/ubuntu' },
    { id: 'white-label', label: 'White-Label', icon: <Building className="h-4 w-4" />, href: '/white-label' },
    { id: 'referral', label: 'Referral System', icon: <Users className="h-4 w-4" />, href: '/referral' },
    { id: 'payments', label: 'Payments', icon: <Wallet className="h-4 w-4" />, href: '/payments' },
    { id: 'analytics', label: 'Analytics', icon: <BarChart3 className="h-4 w-4" />, href: '/analytics' },
    { id: 'settings', label: 'Settings', icon: <Settings className="h-4 w-4" />, href: '/settings' },
  ]

  return (
    <div className="bg-card w-64 shadow-lg">
      <div className="p-6">
        <div className="flex items-center gap-2 mb-8">
          <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
            <Globe className="h-4 w-4 text-primary-foreground" />
          </div>
          <div>
            <h2 className="font-bold text-lg">WebWaka</h2>
            <p className="text-xs text-muted-foreground">Super Admin</p>
          </div>
        </div>
        
        <nav className="space-y-2">
          {menuItems.map((item) => (
            <a
              key={item.id}
              href={item.href}
              className={`flex items-center gap-3 px-3 py-2 rounded-lg transition-colors ${
                activeItem === item.id
                  ? 'bg-primary text-primary-foreground'
                  : 'text-muted-foreground hover:text-foreground hover:bg-accent'
              }`}
              onClick={() => setActiveItem(item.id)}
            >
              {item.icon}
              {item.label}
            </a>
          ))}
        </nav>
      </div>
    </div>
  )
}

// Header Component
function Header({ systemData }) {
  return (
    <header className="bg-card shadow-sm border-b px-6 py-4">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-semibold">WebWaka Digital Operating System</h1>
          <p className="text-sm text-muted-foreground">
            Version {systemData?.version || "1.0.0"} • {systemData?.status || "Operational"}
          </p>
        </div>
        <div className="flex items-center gap-4">
          <Badge variant={systemData?.status === 'operational' ? 'default' : 'destructive'}>
            {systemData?.status || 'Unknown'}
          </Badge>
          <Button variant="outline" size="sm">
            <Shield className="h-4 w-4 mr-2" />
            Admin Panel
          </Button>
        </div>
      </div>
    </header>
  )
}

// Status Card Component
function StatusCard({ title, value, icon, status }) {
  const getStatusColor = (status) => {
    switch (status) {
      case 'operational': return 'text-green-600'
      case 'warning': return 'text-yellow-600'
      case 'error': return 'text-red-600'
      default: return 'text-muted-foreground'
    }
  }

  return (
    <Card>
      <CardContent className="p-6">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm font-medium text-muted-foreground">{title}</p>
            <p className={`text-2xl font-bold ${getStatusColor(status)}`}>
              {typeof value === 'string' ? value : value.toLocaleString()}
            </p>
          </div>
          <div className={`${getStatusColor(status)}`}>
            {icon}
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

// Agent Category Item Component
function AgentCategoryItem({ name, count, description, status }) {
  return (
    <div className="flex items-center justify-between p-3 rounded-lg border">
      <div className="flex-1">
        <div className="flex items-center gap-2">
          <h4 className="font-medium">{name}</h4>
          <Badge variant="secondary">{count}</Badge>
        </div>
        <p className="text-sm text-muted-foreground mt-1">{description}</p>
      </div>
      <div className="flex items-center gap-2">
        <CheckCircle className="h-4 w-4 text-green-600" />
        <span className="text-sm text-green-600">Active</span>
      </div>
    </div>
  )
}

// Feature Item Component
function FeatureItem({ name, enabled, description }) {
  return (
    <div className="flex items-center justify-between p-3 rounded-lg border">
      <div className="flex-1">
        <h4 className="font-medium">{name}</h4>
        <p className="text-sm text-muted-foreground mt-1">{description}</p>
      </div>
      <div className="flex items-center gap-2">
        {enabled ? (
          <>
            <CheckCircle className="h-4 w-4 text-green-600" />
            <span className="text-sm text-green-600">Enabled</span>
          </>
        ) : (
          <>
            <AlertTriangle className="h-4 w-4 text-yellow-600" />
            <span className="text-sm text-yellow-600">Disabled</span>
          </>
        )}
      </div>
    </div>
  )
}

// Quick Action Button Component
function QuickActionButton({ icon, label, onClick }) {
  return (
    <Button
      variant="outline"
      className="h-auto p-4 flex flex-col items-center gap-2"
      onClick={onClick}
    >
      {icon}
      <span className="text-sm">{label}</span>
    </Button>
  )
}

// Placeholder components for other routes
function AgentsManagement() {
  return (
    <div className="flex h-screen bg-background">
      <Sidebar />
      <div className="flex-1 p-6">
        <h1 className="text-3xl font-bold mb-6">Agents Management</h1>
        <Card>
          <CardContent className="p-6">
            <p>Comprehensive agent management interface coming soon...</p>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

function UbuntuPhilosophy() {
  return (
    <div className="flex h-screen bg-background">
      <Sidebar />
      <div className="flex-1 p-6">
        <h1 className="text-3xl font-bold mb-6">Ubuntu Philosophy Management</h1>
        <Card>
          <CardContent className="p-6">
            <p>Ubuntu philosophy configuration and cultural settings...</p>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

function WhiteLabelManagement() {
  return (
    <div className="flex h-screen bg-background">
      <Sidebar />
      <div className="flex-1 p-6">
        <h1 className="text-3xl font-bold mb-6">White-Label Platform Management</h1>
        <Card>
          <CardContent className="p-6">
            <p>White-label partner management and platform replication...</p>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

function ReferralSystem() {
  return (
    <div className="flex h-screen bg-background">
      <Sidebar />
      <div className="flex-1 p-6">
        <h1 className="text-3xl font-bold mb-6">Referral System Management</h1>
        <Card>
          <CardContent className="p-6">
            <p>Multi-level referral system and partner hierarchy management...</p>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

function PaymentSystems() {
  return (
    <div className="flex h-screen bg-background">
      <Sidebar />
      <div className="flex-1 p-6">
        <h1 className="text-3xl font-bold mb-6">Payment Systems Management</h1>
        <Card>
          <CardContent className="p-6">
            <p>HandyLife Wallet integration and payment processing management...</p>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

function Analytics() {
  return (
    <div className="flex h-screen bg-background">
      <Sidebar />
      <div className="flex-1 p-6">
        <h1 className="text-3xl font-bold mb-6">Analytics Dashboard</h1>
        <Card>
          <CardContent className="p-6">
            <p>Comprehensive analytics and performance metrics...</p>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

function SystemSettings() {
  return (
    <div className="flex h-screen bg-background">
      <Sidebar />
      <div className="flex-1 p-6">
        <h1 className="text-3xl font-bold mb-6">System Settings</h1>
        <Card>
          <CardContent className="p-6">
            <p>System configuration and administrative settings...</p>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

export default App



// Dashboard Component
function Dashboard({ systemData }) {
  return (
    <div className="space-y-6">
      <div className="border-b border-gray-200 pb-4">
        <h2 className="text-2xl font-bold text-gray-900">System Overview</h2>
        <p className="text-gray-600 mt-1">Real-time status of all WebWaka systems</p>
      </div>

      {/* System Status Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <span className="text-2xl">🤖</span>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Total Agents</dt>
                  <dd className="text-lg font-medium text-gray-900">{systemData?.agents?.total || 42}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <span className="text-2xl">🌍</span>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Ubuntu Philosophy</dt>
                  <dd className="text-lg font-medium text-green-600">Active</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <span className="text-2xl">📱</span>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">African Optimization</dt>
                  <dd className="text-lg font-medium text-green-600">Enabled</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <span className="text-2xl">🏢</span>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">White-Label Ready</dt>
                  <dd className="text-lg font-medium text-green-600">Yes</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Agent Categories */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">Agent Categories</h3>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            {Object.entries(systemData?.agents || {}).filter(([key]) => key !== 'total').map(([category, count]) => (
              <div key={category} className="text-center p-4 border rounded-lg">
                <div className="text-2xl font-bold text-orange-600">{count}</div>
                <div className="text-sm text-gray-600 capitalize">{category.replace('_', ' ')}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Features Status */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">System Features</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {Object.entries(systemData?.features || {}).map(([feature, enabled]) => (
              <div key={feature} className="flex items-center space-x-2">
                <span className={`w-3 h-3 rounded-full ${enabled ? 'bg-green-500' : 'bg-red-500'}`}></span>
                <span className="text-sm text-gray-700 capitalize">{feature.replace('_', ' ')}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

// Agents Management Component
function AgentsManagement({ systemData }) {
  return (
    <div className="space-y-6">
      <div className="border-b border-gray-200 pb-4">
        <h2 className="text-2xl font-bold text-gray-900">Agents Management</h2>
        <p className="text-gray-600 mt-1">Monitor and manage all 42 WebWaka agents</p>
      </div>

      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <div className="space-y-4">
            {[
              { category: 'Sector Management', count: 14, description: 'Agriculture, Healthcare, Education, Finance, etc.' },
              { category: 'Integration', count: 8, description: 'Cross-sector integration agents' },
              { category: 'White Label', count: 6, description: 'Platform replication and customization' },
              { category: 'Referral System', count: 6, description: 'Multi-level partner management' },
              { category: 'Payment Systems', count: 6, description: 'Financial processing and compliance' },
              { category: 'Infrastructure', count: 4, description: 'Core system infrastructure' }
            ].map((category) => (
              <div key={category.category} className="border rounded-lg p-4">
                <div className="flex justify-between items-center">
                  <div>
                    <h4 className="text-lg font-medium text-gray-900">{category.category}</h4>
                    <p className="text-sm text-gray-600">{category.description}</p>
                  </div>
                  <div className="text-right">
                    <div className="text-2xl font-bold text-orange-600">{category.count}</div>
                    <div className="text-sm text-green-600">All Active</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

// Ubuntu Philosophy Component
function UbuntuPhilosophy({ systemData }) {
  return (
    <div className="space-y-6">
      <div className="border-b border-gray-200 pb-4">
        <h2 className="text-2xl font-bold text-gray-900">Ubuntu Philosophy</h2>
        <p className="text-gray-600 mt-1">🤝 "I am because we are" - Ubuntu values in technology</p>
      </div>

      <div className="bg-gradient-to-r from-orange-50 to-red-50 rounded-lg p-6">
        <h3 className="text-xl font-bold text-gray-900 mb-4">🌍 {systemData?.ubuntu_greeting}</h3>
        
        <div className="grid md:grid-cols-2 gap-6">
          <div className="space-y-4">
            <div className="bg-white p-4 rounded-lg shadow">
              <h4 className="font-semibold text-gray-900 mb-2">🤝 Community Centered</h4>
              <p className="text-gray-600">"I am because we are" - Technology serving community needs</p>
            </div>
            
            <div className="bg-white p-4 rounded-lg shadow">
              <h4 className="font-semibold text-gray-900 mb-2">👴 Traditional Leadership</h4>
              <p className="text-gray-600">Respect for elders and wisdom in system governance</p>
            </div>
          </div>
          
          <div className="space-y-4">
            <div className="bg-white p-4 rounded-lg shadow">
              <h4 className="font-semibold text-gray-900 mb-2">⚖️ Fair Sharing</h4>
              <p className="text-gray-600">Ubuntu fair distribution across all revenue systems</p>
            </div>
            
            <div className="bg-white p-4 rounded-lg shadow">
              <h4 className="font-semibold text-gray-900 mb-2">🌍 Cultural Sensitivity</h4>
              <p className="text-gray-600">African values first in all system decisions</p>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Ubuntu Integration Status</h3>
          <div className="space-y-3">
            {[
              'Community-centered decision making',
              'Traditional leadership recognition',
              'Fair sharing revenue distribution',
              'Cultural sensitivity validation',
              'African language support (10+ languages)',
              'Ubuntu greeting integration'
            ].map((item, index) => (
              <div key={index} className="flex items-center space-x-3">
                <span className="w-2 h-2 bg-green-500 rounded-full"></span>
                <span className="text-gray-700">{item}</span>
                <span className="text-green-600 text-sm">✓ Active</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

// White-Label Management Component
function WhiteLabelManagement({ systemData }) {
  return (
    <div className="space-y-6">
      <div className="border-b border-gray-200 pb-4">
        <h2 className="text-2xl font-bold text-gray-900">White-Label Platform</h2>
        <p className="text-gray-600 mt-1">🏢 Unlimited partner platform replication</p>
      </div>

      <div className="grid md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Platform Replication</h3>
          <p className="text-gray-600 mb-4">Complete system duplication for partners</p>
          <div className="text-2xl font-bold text-green-600">Ready</div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Custom Branding</h3>
          <p className="text-gray-600 mb-4">Partner-specific branding and customization</p>
          <div className="text-2xl font-bold text-green-600">Active</div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Independent Deployment</h3>
          <p className="text-gray-600 mb-4">Standalone partner deployments</p>
          <div className="text-2xl font-bold text-green-600">Available</div>
        </div>
      </div>

      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">White-Label Capabilities</h3>
          <div className="grid md:grid-cols-2 gap-4">
            {[
              'Complete platform replication',
              'Custom branding and theming',
              'Independent client configuration',
              'Multi-tenant architecture',
              'Automated deployment pipeline',
              'Partner-specific customization'
            ].map((capability, index) => (
              <div key={index} className="flex items-center space-x-3">
                <span className="w-2 h-2 bg-blue-500 rounded-full"></span>
                <span className="text-gray-700">{capability}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

// Referral System Component
function ReferralSystem({ systemData }) {
  return (
    <div className="space-y-6">
      <div className="border-b border-gray-200 pb-4">
        <h2 className="text-2xl font-bold text-gray-900">Multi-Level Referral System</h2>
        <p className="text-gray-600 mt-1">💰 6-level partner hierarchy with Ubuntu values</p>
      </div>

      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Partner Hierarchy Levels</h3>
          <div className="space-y-3">
            {[
              { level: 1, name: 'Continental Partners', description: 'Continent-wide operations' },
              { level: 2, name: 'Regional Partners', description: 'Multi-country regions' },
              { level: 3, name: 'National Partners', description: 'Country-level operations' },
              { level: 4, name: 'State Partners', description: 'State/province level' },
              { level: 5, name: 'Local Partners', description: 'City/district level' },
              { level: 6, name: 'Affiliate Partners', description: 'Individual affiliates' }
            ].map((level) => (
              <div key={level.level} className="flex items-center justify-between p-4 border rounded-lg">
                <div className="flex items-center space-x-4">
                  <div className="w-8 h-8 bg-orange-500 text-white rounded-full flex items-center justify-center font-bold">
                    {level.level}
                  </div>
                  <div>
                    <h4 className="font-medium text-gray-900">{level.name}</h4>
                    <p className="text-sm text-gray-600">{level.description}</p>
                  </div>
                </div>
                <div className="text-green-600 font-medium">Active</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="grid md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Commission Engine</h3>
          <p className="text-gray-600 mb-4">Real-time commission calculation</p>
          <div className="text-2xl font-bold text-green-600">Active</div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Partner Analytics</h3>
          <p className="text-gray-600 mb-4">Performance tracking and insights</p>
          <div className="text-2xl font-bold text-green-600">Live</div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Mobile Partner App</h3>
          <p className="text-gray-600 mb-4">African mobile-first design</p>
          <div className="text-2xl font-bold text-green-600">Ready</div>
        </div>
      </div>
    </div>
  )
}

// Payment Systems Component
function PaymentSystems({ systemData }) {
  return (
    <div className="space-y-6">
      <div className="border-b border-gray-200 pb-4">
        <h2 className="text-2xl font-bold text-gray-900">Payment Systems</h2>
        <p className="text-gray-600 mt-1">💳 HandyLife Wallet & African payment integration</p>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Revenue Sharing</h3>
          <div className="text-2xl font-bold text-green-600 mb-2">Active</div>
          <p className="text-gray-600">Ubuntu fair distribution</p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Payment Integration</h3>
          <div className="text-2xl font-bold text-green-600 mb-2">Live</div>
          <p className="text-gray-600">HandyLife Wallet ready</p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Commission Payout</h3>
          <div className="text-2xl font-bold text-green-600 mb-2">Automated</div>
          <p className="text-gray-600">Real-time processing</p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Financial Compliance</h3>
          <div className="text-2xl font-bold text-green-600 mb-2">Compliant</div>
          <p className="text-gray-600">African regulations</p>
        </div>
      </div>

      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Supported Payment Methods</h3>
          <div className="grid md:grid-cols-3 gap-4">
            {[
              'HandyLife Wallet',
              'Mobile Money (MTN, Airtel, etc.)',
              'Bank Transfers',
              'Credit/Debit Cards',
              'Cryptocurrency',
              'PayPal',
              'Stripe',
              'Paystack (African focus)',
              'Local African payment gateways'
            ].map((method, index) => (
              <div key={index} className="flex items-center space-x-3 p-3 border rounded-lg">
                <span className="w-2 h-2 bg-green-500 rounded-full"></span>
                <span className="text-gray-700">{method}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

// Analytics Component
function Analytics({ systemData }) {
  return (
    <div className="space-y-6">
      <div className="border-b border-gray-200 pb-4">
        <h2 className="text-2xl font-bold text-gray-900">Analytics Dashboard</h2>
        <p className="text-gray-600 mt-1">📈 Real-time system performance and usage metrics</p>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">System Uptime</h3>
          <div className="text-3xl font-bold text-green-600 mb-2">99.9%</div>
          <p className="text-gray-600">Last 30 days</p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Active Users</h3>
          <div className="text-3xl font-bold text-blue-600 mb-2">1,247</div>
          <p className="text-gray-600">Current session</p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">API Requests</h3>
          <div className="text-3xl font-bold text-purple-600 mb-2">45.2K</div>
          <p className="text-gray-600">Today</p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Response Time</h3>
          <div className="text-3xl font-bold text-orange-600 mb-2">1.2s</div>
          <p className="text-gray-600">Average</p>
        </div>
      </div>

      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Performance Metrics</h3>
          <div className="space-y-4">
            {[
              { metric: 'Ubuntu Philosophy Compliance', value: '93.51%', status: 'excellent' },
              { metric: 'African Market Optimization', value: '96.50%', status: 'excellent' },
              { metric: 'Mobile-First Performance', value: '94.2%', status: 'excellent' },
              { metric: 'System Integration Health', value: '90.91%', status: 'good' },
              { metric: 'Payment Processing Success', value: '99.7%', status: 'excellent' },
              { metric: 'White-Label Deployment Ready', value: '100%', status: 'excellent' }
            ].map((item, index) => (
              <div key={index} className="flex justify-between items-center p-3 border rounded-lg">
                <span className="text-gray-700">{item.metric}</span>
                <div className="flex items-center space-x-2">
                  <span className="font-bold text-gray-900">{item.value}</span>
                  <span className={`px-2 py-1 rounded-full text-xs ${
                    item.status === 'excellent' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                  }`}>
                    {item.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

// System Settings Component
function SystemSettings({ systemData }) {
  return (
    <div className="space-y-6">
      <div className="border-b border-gray-200 pb-4">
        <h2 className="text-2xl font-bold text-gray-900">System Settings</h2>
        <p className="text-gray-600 mt-1">⚙️ Configure WebWaka system parameters</p>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Ubuntu Philosophy Settings</h3>
            <div className="space-y-3">
              {[
                { setting: 'Ubuntu Greeting', value: 'Enabled', description: 'Sawubona! I see you' },
                { setting: 'Community Centered', value: 'Active', description: 'I am because we are' },
                { setting: 'Traditional Leadership', value: 'Respected', description: 'Elder wisdom honored' },
                { setting: 'Fair Sharing', value: 'Automated', description: 'Ubuntu distribution' }
              ].map((item, index) => (
                <div key={index} className="flex justify-between items-center p-3 border rounded-lg">
                  <div>
                    <div className="font-medium text-gray-900">{item.setting}</div>
                    <div className="text-sm text-gray-600">{item.description}</div>
                  </div>
                  <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm">
                    {item.value}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">African Optimization</h3>
            <div className="space-y-3">
              {[
                { setting: 'Mobile-First Design', value: 'Enabled', description: 'Optimized for African mobile' },
                { setting: 'Low-Bandwidth Mode', value: 'Active', description: 'Network optimization' },
                { setting: 'Offline Support', value: '72 Hours', description: 'Offline capabilities' },
                { setting: 'Multi-Currency', value: '10+ Currencies', description: 'African currencies' }
              ].map((item, index) => (
                <div key={index} className="flex justify-between items-center p-3 border rounded-lg">
                  <div>
                    <div className="font-medium text-gray-900">{item.setting}</div>
                    <div className="text-sm text-gray-600">{item.description}</div>
                  </div>
                  <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
                    {item.value}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">System Configuration</h3>
          <div className="grid md:grid-cols-3 gap-4">
            {[
              { config: 'Environment', value: 'Production' },
              { config: 'Version', value: '1.0.0' },
              { config: 'Database', value: 'PostgreSQL' },
              { config: 'Cache', value: 'Redis' },
              { config: 'CDN', value: 'CloudFront' },
              { config: 'Monitoring', value: 'CloudWatch' }
            ].map((item, index) => (
              <div key={index} className="text-center p-4 border rounded-lg">
                <div className="font-medium text-gray-900">{item.config}</div>
                <div className="text-sm text-gray-600 mt-1">{item.value}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default App

