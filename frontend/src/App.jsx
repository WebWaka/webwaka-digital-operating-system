import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Globe, Cpu, Users, Zap, Shield, Smartphone } from 'lucide-react'
import './App.css'

function App() {
  const [apiStatus, setApiStatus] = useState(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Fetch API status from backend
    const fetchApiStatus = async () => {
      try {
        const response = await fetch('/api/status')
        const data = await response.json()
        setApiStatus(data)
      } catch (error) {
        console.error('Failed to fetch API status:', error)
        setApiStatus({ error: 'API connection failed' })
      } finally {
        setIsLoading(false)
      }
    }

    fetchApiStatus()
  }, [])

  const features = [
    {
      icon: <Cpu className="h-8 w-8 text-blue-600" />,
      title: "AI SuperAgent",
      description: "13+ AI platforms integrated with Hugging Face ecosystem for cutting-edge capabilities"
    },
    {
      icon: <Users className="h-8 w-8 text-green-600" />,
      title: "Partner Ecosystem",
      description: "6-level referral system with white-label solutions for continental growth"
    },
    {
      icon: <Globe className="h-8 w-8 text-purple-600" />,
      title: "42 Sectors",
      description: "Complete coverage of African economic sectors with cellular-level modularity"
    },
    {
      icon: <Shield className="h-8 w-8 text-red-600" />,
      title: "Bank-Grade Security",
      description: "Biometric identity verification with world-class security framework"
    },
    {
      icon: <Smartphone className="h-8 w-8 text-orange-600" />,
      title: "Mobile-First",
      description: "Offline-first PWA optimized for African infrastructure and devices"
    },
    {
      icon: <Zap className="h-8 w-8 text-yellow-600" />,
      title: "Cultural Intelligence",
      description: "50+ African languages with Ubuntu philosophy and cultural adaptation"
    }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                <Globe className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">WebWaka</h1>
                <p className="text-sm text-gray-600">Digital Operating System</p>
              </div>
            </div>
            <Badge variant="outline" className="bg-green-50 text-green-700 border-green-200">
              {isLoading ? 'Connecting...' : apiStatus?.webwaka?.status || 'Offline'}
            </Badge>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center">
          <h2 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
            Africa's Premier
            <span className="block text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600">
              AI-Powered Digital Operating System
            </span>
          </h2>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Empowering every African with world-class AI-powered digital tools that respect cultural intelligence, 
            promote economic inclusion, and accelerate continental transformation.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" className="bg-blue-600 hover:bg-blue-700">
              Get Started
            </Button>
            <Button size="lg" variant="outline">
              Learn More
            </Button>
          </div>
        </div>
      </section>

      {/* System Status */}
      {apiStatus?.webwaka && (
        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Card className="bg-white/80 backdrop-blur-sm">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Cpu className="h-5 w-5" />
                System Status
              </CardTitle>
              <CardDescription>Real-time WebWaka infrastructure status</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600">{apiStatus.webwaka.sectors}</div>
                  <div className="text-sm text-gray-600">Sectors</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-600">{apiStatus.webwaka.subsectors}</div>
                  <div className="text-sm text-gray-600">Subsectors</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-purple-600">{apiStatus.webwaka.cellular_modules}</div>
                  <div className="text-sm text-gray-600">Cellular Modules</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-orange-600">
                    {apiStatus.webwaka.cellular_architecture === 'active' ? 'Active' : 'Inactive'}
                  </div>
                  <div className="text-sm text-gray-600">Architecture</div>
                </div>
              </div>
            </CardContent>
          </Card>
        </section>
      )}

      {/* Features Grid */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-12">
          <h3 className="text-3xl font-bold text-gray-900 mb-4">
            Comprehensive Digital Transformation
          </h3>
          <p className="text-lg text-gray-600">
            Built with cellular-level modularity for maximum scalability and African optimization
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <Card key={index} className="bg-white/80 backdrop-blur-sm hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="flex items-center gap-3">
                  {feature.icon}
                  <CardTitle className="text-lg">{feature.title}</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-gray-600">
                  {feature.description}
                </CardDescription>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center">
            <div className="flex items-center justify-center space-x-3 mb-4">
              <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                <Globe className="h-5 w-5 text-white" />
              </div>
              <h4 className="text-xl font-bold">WebWaka</h4>
            </div>
            <p className="text-gray-400 mb-4">
              Serving 1 billion Africans across 54 countries with culturally intelligent AI technology
            </p>
            <p className="text-sm text-gray-500">
              © 2025 WebWaka Digital Operating System. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App
