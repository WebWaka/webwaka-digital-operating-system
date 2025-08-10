import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { 
  Activity, 
  Users, 
  Settings, 
  BarChart3, 
  Shield, 
  Globe, 
  Smartphone, 
  Heart,
  DollarSign,
  Building,
  UserCheck,
  Zap,
  Database,
  Monitor,
  AlertTriangle,
  CheckCircle,
  Clock,
  TrendingUp,
  MapPin,
  Languages,
  Wallet
} from 'lucide-react'
import './App.css'

// API Configuration
const API_BASE_URL = 'https://lnh8imcn0lxd.manus.space'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-background">
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/agents" element={<AgentsManagement />} />
          <Route path="/ubuntu" element={<UbuntuPhilosophy />} />
          <Route path="/white-label" element={<WhiteLabelManagement />} />
          <Route path="/referral" element={<ReferralSystem />} />
          <Route path="/payments" element={<PaymentSystems />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/settings" element={<SystemSettings />} />
        </Routes>
      </div>
    </Router>
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

