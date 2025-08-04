import React, { useState, useEffect } from 'react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, LineChart, Line, AreaChart, Area
} from 'recharts';
import { 
  TrendingUp, TrendingDown, Users, Package, DollarSign, 
  AlertTriangle, CheckCircle, Clock, Activity, Zap
} from 'lucide-react';
import VoiceInterface from './VoiceInterface';

const SystemDashboard = ({ 
  currentSystem = 'dashboard', 
  onSystemChange,
  culturalContext = {},
  user = null 
}) => {
  const [dashboardData, setDashboardData] = useState({});
  const [isLoading, setIsLoading] = useState(true);
  const [activeMetrics, setActiveMetrics] = useState([]);
  const [realtimeUpdates, setRealtimeUpdates] = useState(true);

  // System configurations with African business context
  const systemConfigs = {
    dashboard: {
      title: 'Business Overview',
      color: '#3b82f6',
      metrics: ['revenue', 'customers', 'inventory', 'employees']
    },
    pos: {
      title: 'Point of Sale',
      color: '#10b981',
      metrics: ['daily_sales', 'transactions', 'top_products', 'payment_methods']
    },
    inventory: {
      title: 'Inventory Management',
      color: '#f59e0b',
      metrics: ['stock_levels', 'low_stock', 'reorder_points', 'turnover_rate']
    },
    crm: {
      title: 'Customer Relations',
      color: '#8b5cf6',
      metrics: ['customer_satisfaction', 'lead_conversion', 'retention_rate', 'lifetime_value']
    },
    hr: {
      title: 'Human Resources',
      color: '#ef4444',
      metrics: ['employee_count', 'attendance', 'performance', 'training_completion']
    },
    financial: {
      title: 'Financial Management',
      color: '#06b6d4',
      metrics: ['cash_flow', 'profit_margin', 'expenses', 'budget_variance']
    },
    supply_chain: {
      title: 'Supply Chain',
      color: '#84cc16',
      metrics: ['supplier_performance', 'delivery_times', 'cost_savings', 'quality_scores']
    },
    project: {
      title: 'Project Management',
      color: '#f97316',
      metrics: ['project_completion', 'resource_utilization', 'budget_adherence', 'timeline_performance']
    },
    healthcare: {
      title: 'Healthcare Management',
      color: '#ec4899',
      metrics: ['patient_satisfaction', 'appointment_efficiency', 'treatment_outcomes', 'resource_utilization']
    },
    education: {
      title: 'Education Management',
      color: '#6366f1',
      metrics: ['student_performance', 'attendance_rates', 'course_completion', 'teacher_effectiveness']
    },
    agriculture: {
      title: 'Agriculture Management',
      color: '#22c55e',
      metrics: ['crop_yield', 'weather_impact', 'resource_efficiency', 'market_prices']
    },
    restaurant: {
      title: 'Restaurant Management',
      color: '#f59e0b',
      metrics: ['table_turnover', 'food_cost', 'customer_satisfaction', 'waste_reduction']
    }
  };

  // Sample data generation for African business contexts
  const generateSampleData = (system) => {
    const baseData = {
      dashboard: {
        revenue: { value: 125000, change: 12.5, trend: 'up' },
        customers: { value: 1250, change: 8.3, trend: 'up' },
        inventory: { value: 450, change: -5.2, trend: 'down' },
        employees: { value: 28, change: 3.7, trend: 'up' },
        charts: {
          revenue_trend: [
            { month: 'Jan', revenue: 95000, expenses: 75000 },
            { month: 'Feb', revenue: 105000, expenses: 78000 },
            { month: 'Mar', revenue: 115000, expenses: 82000 },
            { month: 'Apr', revenue: 125000, expenses: 85000 }
          ],
          customer_segments: [
            { name: 'Retail', value: 45, color: '#3b82f6' },
            { name: 'Wholesale', value: 30, color: '#10b981' },
            { name: 'Online', value: 25, color: '#f59e0b' }
          ]
        }
      },
      pos: {
        daily_sales: { value: 4250, change: 15.2, trend: 'up' },
        transactions: { value: 156, change: 8.7, trend: 'up' },
        top_products: { value: 'Sugar 1kg', change: 0, trend: 'stable' },
        payment_methods: { value: 'Mobile Money 65%', change: 5.3, trend: 'up' },
        charts: {
          hourly_sales: [
            { hour: '8AM', sales: 250 },
            { hour: '10AM', sales: 420 },
            { hour: '12PM', sales: 680 },
            { hour: '2PM', sales: 890 },
            { hour: '4PM', sales: 1250 },
            { hour: '6PM', sales: 760 }
          ],
          payment_breakdown: [
            { method: 'Mobile Money', value: 65, color: '#10b981' },
            { method: 'Cash', value: 25, color: '#f59e0b' },
            { method: 'Card', value: 10, color: '#3b82f6' }
          ]
        }
      },
      inventory: {
        stock_levels: { value: '85%', change: -3.2, trend: 'down' },
        low_stock: { value: 12, change: 20.0, trend: 'up' },
        reorder_points: { value: 8, change: -12.5, trend: 'down' },
        turnover_rate: { value: '2.3x', change: 8.5, trend: 'up' },
        charts: {
          stock_movement: [
            { product: 'Rice 25kg', in: 100, out: 85, balance: 45 },
            { product: 'Sugar 1kg', in: 200, out: 180, balance: 25 },
            { product: 'Oil 1L', in: 150, out: 140, balance: 35 },
            { product: 'Soap', in: 80, out: 75, balance: 15 }
          ]
        }
      },
      agriculture: {
        crop_yield: { value: '4.2 tons/ha', change: 12.8, trend: 'up' },
        weather_impact: { value: 'Favorable', change: 0, trend: 'stable' },
        resource_efficiency: { value: '78%', change: 5.4, trend: 'up' },
        market_prices: { value: '$450/ton', change: 8.2, trend: 'up' },
        charts: {
          seasonal_yield: [
            { season: 'Q1', maize: 3.8, beans: 2.1, rice: 4.5 },
            { season: 'Q2', maize: 4.2, beans: 2.4, rice: 4.8 },
            { season: 'Q3', maize: 4.0, beans: 2.2, rice: 4.6 },
            { season: 'Q4', maize: 4.1, beans: 2.3, rice: 4.7 }
          ]
        }
      }
    };

    return baseData[system] || baseData.dashboard;
  };

  // Load dashboard data
  useEffect(() => {
    setIsLoading(true);
    
    // Simulate API call
    setTimeout(() => {
      const data = generateSampleData(currentSystem);
      setDashboardData(data);
      setActiveMetrics(systemConfigs[currentSystem]?.metrics || []);
      setIsLoading(false);
    }, 1000);
  }, [currentSystem]);

  // Real-time updates simulation
  useEffect(() => {
    if (!realtimeUpdates) return;

    const interval = setInterval(() => {
      setDashboardData(prev => {
        const updated = { ...prev };
        // Simulate small changes in metrics
        Object.keys(updated).forEach(key => {
          if (typeof updated[key] === 'object' && updated[key].value) {
            const randomChange = (Math.random() - 0.5) * 2; // -1 to 1
            updated[key] = {
              ...updated[key],
              change: updated[key].change + randomChange
            };
          }
        });
        return updated;
      });
    }, 30000); // Update every 30 seconds

    return () => clearInterval(interval);
  }, [realtimeUpdates]);

  const handleVoiceCommand = async (commandData) => {
    const { command, language, system } = commandData;
    
    // Process voice commands for dashboard
    if (command.toLowerCase().includes('show') || command.toLowerCase().includes('display')) {
      // Handle display commands
      return { response: `Displaying ${system} dashboard information` };
    }
    
    if (command.toLowerCase().includes('switch') || command.toLowerCase().includes('change')) {
      // Handle system switching
      return { response: `Switching to requested system` };
    }
    
    return { response: 'Command processed successfully' };
  };

  const MetricCard = ({ title, data, icon: Icon, color }) => (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-3">
          <div 
            className="p-2 rounded-lg"
            style={{ backgroundColor: color + '20' }}
          >
            <Icon size={20} style={{ color }} />
          </div>
          <h3 className="font-medium text-gray-900">{title}</h3>
        </div>
        
        {data?.trend && (
          <div className={`flex items-center space-x-1 ${
            data.trend === 'up' ? 'text-green-600' : 
            data.trend === 'down' ? 'text-red-600' : 'text-gray-600'
          }`}>
            {data.trend === 'up' ? <TrendingUp size={16} /> : 
             data.trend === 'down' ? <TrendingDown size={16} /> : <Activity size={16} />}
            <span className="text-sm font-medium">
              {data.change > 0 ? '+' : ''}{data.change?.toFixed(1)}%
            </span>
          </div>
        )}
      </div>
      
      <div className="text-2xl font-bold text-gray-900 mb-2">
        {data?.value || '---'}
      </div>
      
      <div className="text-sm text-gray-500">
        Compared to last period
      </div>
    </div>
  );

  const ChartContainer = ({ title, children, height = 300 }) => (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <h3 className="font-medium text-gray-900 mb-4">{title}</h3>
      <div style={{ height }}>
        {children}
      </div>
    </div>
  );

  if (isLoading) {
    return (
      <div className="p-6">
        <div className="animate-pulse">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="bg-gray-200 rounded-lg h-32"></div>
            ))}
          </div>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="bg-gray-200 rounded-lg h-64"></div>
            <div className="bg-gray-200 rounded-lg h-64"></div>
          </div>
        </div>
      </div>
    );
  }

  const config = systemConfigs[currentSystem];
  const data = dashboardData;

  return (
    <div className="p-4 md:p-6 space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between space-y-4 md:space-y-0">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">
            {config?.title || 'Dashboard'}
          </h1>
          <p className="text-gray-600">
            Real-time insights and analytics for your business
          </p>
        </div>
        
        <div className="flex items-center space-x-4">
          <button
            onClick={() => setRealtimeUpdates(!realtimeUpdates)}
            className={`flex items-center space-x-2 px-4 py-2 rounded-lg border transition-colors ${
              realtimeUpdates 
                ? 'bg-green-50 border-green-200 text-green-700' 
                : 'bg-gray-50 border-gray-200 text-gray-700'
            }`}
          >
            <Zap size={16} />
            <span className="text-sm font-medium">
              {realtimeUpdates ? 'Live Updates' : 'Static View'}
            </span>
          </button>
        </div>
      </div>

      {/* Voice Interface */}
      <div className="lg:hidden">
        <VoiceInterface
          onVoiceCommand={handleVoiceCommand}
          currentSystem={currentSystem}
          culturalContext={culturalContext}
        />
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6">
        {activeMetrics.map((metric, index) => {
          const metricData = data[metric];
          const icons = [DollarSign, Users, Package, TrendingUp];
          const Icon = icons[index % icons.length];
          
          return (
            <MetricCard
              key={metric}
              title={metric.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
              data={metricData}
              icon={Icon}
              color={config?.color || '#3b82f6'}
            />
          );
        })}
      </div>

      {/* Charts Section */}
      {data.charts && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Revenue/Sales Trend */}
          {(data.charts.revenue_trend || data.charts.hourly_sales) && (
            <ChartContainer title={currentSystem === 'pos' ? 'Hourly Sales' : 'Revenue Trend'}>
              <ResponsiveContainer width="100%" height="100%">
                {currentSystem === 'pos' ? (
                  <AreaChart data={data.charts.hourly_sales}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="hour" />
                    <YAxis />
                    <Tooltip formatter={(value) => [`$${value}`, 'Sales']} />
                    <Area 
                      type="monotone" 
                      dataKey="sales" 
                      stroke={config?.color} 
                      fill={config?.color + '20'} 
                    />
                  </AreaChart>
                ) : (
                  <LineChart data={data.charts.revenue_trend}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis />
                    <Tooltip formatter={(value) => [`$${value.toLocaleString()}`, '']} />
                    <Line 
                      type="monotone" 
                      dataKey="revenue" 
                      stroke="#10b981" 
                      strokeWidth={3}
                      name="Revenue"
                    />
                    <Line 
                      type="monotone" 
                      dataKey="expenses" 
                      stroke="#ef4444" 
                      strokeWidth={2}
                      name="Expenses"
                    />
                  </LineChart>
                )}
              </ResponsiveContainer>
            </ChartContainer>
          )}

          {/* Pie Charts */}
          {(data.charts.customer_segments || data.charts.payment_breakdown) && (
            <ChartContainer title={currentSystem === 'pos' ? 'Payment Methods' : 'Customer Segments'}>
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={data.charts.customer_segments || data.charts.payment_breakdown}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, value }) => `${name}: ${value}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {(data.charts.customer_segments || data.charts.payment_breakdown).map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </ChartContainer>
          )}

          {/* Inventory Stock Movement */}
          {data.charts.stock_movement && (
            <ChartContainer title="Stock Movement" height={400}>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={data.charts.stock_movement}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="product" angle={-45} textAnchor="end" height={80} />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="in" fill="#10b981" name="Stock In" />
                  <Bar dataKey="out" fill="#ef4444" name="Stock Out" />
                  <Bar dataKey="balance" fill="#3b82f6" name="Balance" />
                </BarChart>
              </ResponsiveContainer>
            </ChartContainer>
          )}

          {/* Agriculture Seasonal Yield */}
          {data.charts.seasonal_yield && (
            <ChartContainer title="Seasonal Crop Yield" height={400}>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={data.charts.seasonal_yield}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="season" />
                  <YAxis />
                  <Tooltip formatter={(value) => [`${value} tons/ha`, '']} />
                  <Bar dataKey="maize" fill="#f59e0b" name="Maize" />
                  <Bar dataKey="beans" fill="#10b981" name="Beans" />
                  <Bar dataKey="rice" fill="#3b82f6" name="Rice" />
                </BarChart>
              </ResponsiveContainer>
            </ChartContainer>
          )}
        </div>
      )}

      {/* Quick Actions */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="font-medium text-gray-900 mb-4">Quick Actions</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {currentSystem === 'pos' && (
            <>
              <button className="flex flex-col items-center p-4 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors">
                <Package size={24} className="text-blue-600 mb-2" />
                <span className="text-sm font-medium">New Sale</span>
              </button>
              <button className="flex flex-col items-center p-4 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors">
                <Users size={24} className="text-green-600 mb-2" />
                <span className="text-sm font-medium">Add Customer</span>
              </button>
            </>
          )}
          
          {currentSystem === 'inventory' && (
            <>
              <button className="flex flex-col items-center p-4 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors">
                <Package size={24} className="text-blue-600 mb-2" />
                <span className="text-sm font-medium">Add Stock</span>
              </button>
              <button className="flex flex-col items-center p-4 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors">
                <AlertTriangle size={24} className="text-orange-600 mb-2" />
                <span className="text-sm font-medium">Low Stock Alert</span>
              </button>
            </>
          )}
          
          <button className="flex flex-col items-center p-4 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors">
            <CheckCircle size={24} className="text-green-600 mb-2" />
            <span className="text-sm font-medium">Generate Report</span>
          </button>
          
          <button className="flex flex-col items-center p-4 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors">
            <Clock size={24} className="text-purple-600 mb-2" />
            <span className="text-sm font-medium">Schedule Task</span>
          </button>
        </div>
      </div>

      {/* Cultural Context Display */}
      {culturalContext.region && (
        <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg p-6 border border-purple-200">
          <h3 className="font-medium text-purple-900 mb-2">Cultural Context Active</h3>
          <p className="text-purple-700 text-sm">
            Dashboard optimized for {culturalContext.region} business practices and cultural preferences.
            Voice commands available in local languages.
          </p>
        </div>
      )}
    </div>
  );
};

export default SystemDashboard;

