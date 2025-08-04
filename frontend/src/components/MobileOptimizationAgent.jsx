/**
 * WebWaka Mobile Optimization Agent (Agent 6)
 * Mobile-First Design and Touch Optimization
 * 
 * This agent provides comprehensive mobile optimization with:
 * - Responsive design for all screen sizes
 * - Touch-friendly interfaces optimized for African mobile usage
 * - Performance optimization for 2G/3G/4G networks
 * - Offline-first mobile experience
 * - Cultural adaptation for African mobile behaviors
 */

import React, { useState, useEffect, useCallback, useRef } from 'react';
import { debounce } from 'lodash';

// Mobile device detection and capabilities
class MobileDeviceDetector {
  constructor() {
    this.deviceInfo = this.detectDevice();
    this.networkInfo = this.detectNetwork();
    this.touchCapabilities = this.detectTouchCapabilities();
  }

  detectDevice() {
    const userAgent = navigator.userAgent;
    const isAndroid = /Android/i.test(userAgent);
    const isIOS = /iPhone|iPad|iPod/i.test(userAgent);
    const isWindowsPhone = /Windows Phone/i.test(userAgent);
    const isKaiOS = /KaiOS/i.test(userAgent);
    
    // Common African mobile devices
    const isFeaturePhone = /Nokia|TECNO|Infinix|itel|Gionee/i.test(userAgent);
    
    return {
      type: this.getDeviceType(),
      os: isAndroid ? 'Android' : isIOS ? 'iOS' : isWindowsPhone ? 'Windows' : isKaiOS ? 'KaiOS' : 'Unknown',
      isSmartphone: isAndroid || isIOS,
      isFeaturePhone: isFeaturePhone || isKaiOS,
      screenSize: this.getScreenSize(),
      orientation: this.getOrientation(),
      pixelRatio: window.devicePixelRatio || 1
    };
  }

  detectNetwork() {
    const connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
    
    return {
      type: connection?.effectiveType || 'unknown',
      downlink: connection?.downlink || 0,
      rtt: connection?.rtt || 0,
      saveData: connection?.saveData || false,
      isSlowConnection: this.isSlowConnection(connection)
    };
  }

  detectTouchCapabilities() {
    return {
      hasTouch: 'ontouchstart' in window || navigator.maxTouchPoints > 0,
      maxTouchPoints: navigator.maxTouchPoints || 1,
      hasHover: window.matchMedia('(hover: hover)').matches,
      hasPointer: window.matchMedia('(pointer: fine)').matches
    };
  }

  getDeviceType() {
    const width = window.innerWidth;
    if (width < 480) return 'mobile';
    if (width < 768) return 'phablet';
    if (width < 1024) return 'tablet';
    return 'desktop';
  }

  getScreenSize() {
    return {
      width: window.innerWidth,
      height: window.innerHeight,
      availWidth: window.screen.availWidth,
      availHeight: window.screen.availHeight
    };
  }

  getOrientation() {
    return window.innerHeight > window.innerWidth ? 'portrait' : 'landscape';
  }

  isSlowConnection(connection) {
    if (!connection) return false;
    return connection.effectiveType === '2g' || 
           connection.effectiveType === 'slow-2g' ||
           (connection.downlink && connection.downlink < 1.5);
  }
}

// Touch gesture handler for African mobile usage patterns
class TouchGestureHandler {
  constructor(element, options = {}) {
    this.element = element;
    this.options = {
      swipeThreshold: 50,
      tapTimeout: 300,
      doubleTapTimeout: 300,
      longPressTimeout: 500,
      ...options
    };
    
    this.touchStart = null;
    this.touchEnd = null;
    this.lastTap = 0;
    this.longPressTimer = null;
    
    this.bindEvents();
  }

  bindEvents() {
    if (!this.element) return;

    this.element.addEventListener('touchstart', this.handleTouchStart.bind(this), { passive: false });
    this.element.addEventListener('touchmove', this.handleTouchMove.bind(this), { passive: false });
    this.element.addEventListener('touchend', this.handleTouchEnd.bind(this), { passive: false });
    this.element.addEventListener('touchcancel', this.handleTouchCancel.bind(this));
  }

  handleTouchStart(e) {
    this.touchStart = {
      x: e.touches[0].clientX,
      y: e.touches[0].clientY,
      time: Date.now()
    };

    // Start long press timer
    this.longPressTimer = setTimeout(() => {
      this.onLongPress && this.onLongPress(e);
    }, this.options.longPressTimeout);
  }

  handleTouchMove(e) {
    if (!this.touchStart) return;

    // Clear long press timer on move
    if (this.longPressTimer) {
      clearTimeout(this.longPressTimer);
      this.longPressTimer = null;
    }

    const currentTouch = {
      x: e.touches[0].clientX,
      y: e.touches[0].clientY
    };

    const deltaX = currentTouch.x - this.touchStart.x;
    const deltaY = currentTouch.y - this.touchStart.y;

    // Prevent scrolling for horizontal swipes (common in African mobile usage)
    if (Math.abs(deltaX) > Math.abs(deltaY) && Math.abs(deltaX) > 10) {
      e.preventDefault();
    }

    this.onMove && this.onMove(e, { deltaX, deltaY });
  }

  handleTouchEnd(e) {
    if (!this.touchStart) return;

    // Clear long press timer
    if (this.longPressTimer) {
      clearTimeout(this.longPressTimer);
      this.longPressTimer = null;
    }

    this.touchEnd = {
      x: e.changedTouches[0].clientX,
      y: e.changedTouches[0].clientY,
      time: Date.now()
    };

    const deltaX = this.touchEnd.x - this.touchStart.x;
    const deltaY = this.touchEnd.y - this.touchStart.y;
    const deltaTime = this.touchEnd.time - this.touchStart.time;

    // Detect swipe gestures
    if (Math.abs(deltaX) > this.options.swipeThreshold || Math.abs(deltaY) > this.options.swipeThreshold) {
      const direction = this.getSwipeDirection(deltaX, deltaY);
      this.onSwipe && this.onSwipe(e, direction, { deltaX, deltaY, deltaTime });
    }
    // Detect tap gestures
    else if (deltaTime < this.options.tapTimeout) {
      const now = Date.now();
      const timeSinceLastTap = now - this.lastTap;

      if (timeSinceLastTap < this.options.doubleTapTimeout) {
        this.onDoubleTap && this.onDoubleTap(e);
      } else {
        this.onTap && this.onTap(e);
      }

      this.lastTap = now;
    }

    this.touchStart = null;
    this.touchEnd = null;
  }

  handleTouchCancel(e) {
    if (this.longPressTimer) {
      clearTimeout(this.longPressTimer);
      this.longPressTimer = null;
    }
    this.touchStart = null;
    this.touchEnd = null;
  }

  getSwipeDirection(deltaX, deltaY) {
    if (Math.abs(deltaX) > Math.abs(deltaY)) {
      return deltaX > 0 ? 'right' : 'left';
    } else {
      return deltaY > 0 ? 'down' : 'up';
    }
  }
}

// Mobile performance optimizer for African networks
class MobilePerformanceOptimizer {
  constructor() {
    this.deviceDetector = new MobileDeviceDetector();
    this.optimizationLevel = this.determineOptimizationLevel();
    this.imageQuality = this.determineImageQuality();
    this.animationLevel = this.determineAnimationLevel();
  }

  determineOptimizationLevel() {
    const { networkInfo, deviceInfo } = this.deviceDetector;
    
    if (networkInfo.isSlowConnection || deviceInfo.isFeaturePhone) {
      return 'aggressive';
    } else if (networkInfo.type === '3g' || deviceInfo.type === 'mobile') {
      return 'moderate';
    } else {
      return 'minimal';
    }
  }

  determineImageQuality() {
    switch (this.optimizationLevel) {
      case 'aggressive': return 'low';
      case 'moderate': return 'medium';
      default: return 'high';
    }
  }

  determineAnimationLevel() {
    switch (this.optimizationLevel) {
      case 'aggressive': return 'none';
      case 'moderate': return 'reduced';
      default: return 'full';
    }
  }

  optimizeImageSrc(src, width = 300) {
    if (!src) return src;
    
    const quality = this.imageQuality === 'low' ? 60 : this.imageQuality === 'medium' ? 80 : 90;
    const format = this.deviceDetector.deviceInfo.isFeaturePhone ? 'jpg' : 'webp';
    
    // In a real implementation, this would use a CDN service
    return `${src}?w=${width}&q=${quality}&f=${format}`;
  }

  shouldPreloadImages() {
    return this.optimizationLevel !== 'aggressive';
  }

  shouldUseAnimations() {
    return this.animationLevel !== 'none';
  }

  getOptimalChunkSize() {
    switch (this.optimizationLevel) {
      case 'aggressive': return 10;
      case 'moderate': return 25;
      default: return 50;
    }
  }
}

// African mobile UI patterns and cultural adaptations
const AfricanMobileUIPatterns = {
  // Common African mobile interaction patterns
  patterns: {
    bottomNavigation: true, // Easier thumb access
    largeButtons: true, // Better for various hand sizes
    highContrast: true, // Better visibility in bright sunlight
    voiceFirst: true, // Voice commands preferred
    gestureNavigation: true, // Swipe-based navigation
    offlineFirst: true, // Assume poor connectivity
  },

  // Cultural color preferences
  colors: {
    primary: '#2E7D32', // Green - prosperity, growth
    secondary: '#FF6F00', // Orange - energy, warmth
    accent: '#1976D2', // Blue - trust, stability
    warning: '#F57C00', // Amber - caution
    success: '#388E3C', // Green - success
    error: '#D32F2F', // Red - danger
  },

  // Typography optimized for African languages
  typography: {
    fontFamily: 'Roboto, "Noto Sans", Arial, sans-serif',
    baseFontSize: '16px', // Larger for better readability
    lineHeight: 1.6, // Better for African language scripts
    fontWeight: {
      light: 300,
      regular: 400,
      medium: 500,
      bold: 700
    }
  },

  // Spacing optimized for touch
  spacing: {
    touchTarget: '48px', // Minimum touch target size
    padding: '16px',
    margin: '8px',
    borderRadius: '8px'
  }
};

// Main Mobile Optimization Agent Component
const MobileOptimizationAgent = ({ children, className = '' }) => {
  const [deviceInfo, setDeviceInfo] = useState(null);
  const [performanceOptimizer, setPerformanceOptimizer] = useState(null);
  const [orientation, setOrientation] = useState('portrait');
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  const containerRef = useRef(null);

  // Initialize mobile optimization
  useEffect(() => {
    const detector = new MobileDeviceDetector();
    const optimizer = new MobilePerformanceOptimizer();
    
    setDeviceInfo(detector.deviceInfo);
    setPerformanceOptimizer(optimizer);
    setOrientation(detector.getOrientation());

    // Listen for orientation changes
    const handleOrientationChange = debounce(() => {
      setOrientation(detector.getOrientation());
    }, 100);

    // Listen for network changes
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('resize', handleOrientationChange);
    window.addEventListener('orientationchange', handleOrientationChange);
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('resize', handleOrientationChange);
      window.removeEventListener('orientationchange', handleOrientationChange);
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  // Setup touch gestures
  useEffect(() => {
    if (!containerRef.current) return;

    const gestureHandler = new TouchGestureHandler(containerRef.current);
    
    gestureHandler.onSwipe = (e, direction, details) => {
      console.log('Swipe detected:', direction, details);
      // Handle swipe gestures for navigation
    };

    gestureHandler.onTap = (e) => {
      console.log('Tap detected');
      // Handle tap interactions
    };

    gestureHandler.onDoubleTap = (e) => {
      console.log('Double tap detected');
      // Handle double tap (e.g., zoom)
    };

    gestureHandler.onLongPress = (e) => {
      console.log('Long press detected');
      // Handle long press (e.g., context menu)
    };

    return () => {
      // Cleanup gesture handler
    };
  }, []);

  // Generate mobile-optimized styles
  const getMobileStyles = useCallback(() => {
    if (!deviceInfo || !performanceOptimizer) return {};

    const baseStyles = {
      fontFamily: AfricanMobileUIPatterns.typography.fontFamily,
      fontSize: AfricanMobileUIPatterns.typography.baseFontSize,
      lineHeight: AfricanMobileUIPatterns.typography.lineHeight,
      minHeight: '100vh',
      display: 'flex',
      flexDirection: 'column',
      backgroundColor: '#f5f5f5',
      color: '#333',
      touchAction: 'manipulation', // Optimize touch interactions
      userSelect: 'none', // Prevent text selection on touch
      WebkitTapHighlightColor: 'transparent', // Remove tap highlight
    };

    // Device-specific optimizations
    if (deviceInfo.type === 'mobile') {
      baseStyles.padding = '8px';
      baseStyles.fontSize = '14px';
    } else if (deviceInfo.type === 'phablet') {
      baseStyles.padding = '12px';
      baseStyles.fontSize = '15px';
    }

    // Network-specific optimizations
    if (performanceOptimizer.optimizationLevel === 'aggressive') {
      baseStyles.animation = 'none';
      baseStyles.transition = 'none';
    }

    return baseStyles;
  }, [deviceInfo, performanceOptimizer]);

  // Render mobile-optimized UI
  const renderMobileOptimizedContent = () => {
    if (!deviceInfo) {
      return <div>Loading mobile optimization...</div>;
    }

    return (
      <div className="mobile-optimization-wrapper" style={getMobileStyles()}>
        {/* Network status indicator */}
        <NetworkStatusIndicator isOnline={isOnline} />
        
        {/* Device info display (for development) */}
        {process.env.NODE_ENV === 'development' && (
          <DeviceInfoDisplay deviceInfo={deviceInfo} />
        )}
        
        {/* Main content with mobile optimizations */}
        <div className="mobile-content" style={{ flex: 1 }}>
          {children}
        </div>
        
        {/* Mobile navigation */}
        <MobileBottomNavigation />
      </div>
    );
  };

  return (
    <div 
      ref={containerRef}
      className={`mobile-optimization-agent ${className}`}
      data-device-type={deviceInfo?.type}
      data-orientation={orientation}
      data-online={isOnline}
    >
      {renderMobileOptimizedContent()}
    </div>
  );
};

// Network status indicator component
const NetworkStatusIndicator = ({ isOnline }) => {
  const [networkInfo, setNetworkInfo] = useState(null);

  useEffect(() => {
    const connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
    if (connection) {
      const updateNetworkInfo = () => {
        setNetworkInfo({
          type: connection.effectiveType,
          downlink: connection.downlink,
          rtt: connection.rtt,
          saveData: connection.saveData
        });
      };

      updateNetworkInfo();
      connection.addEventListener('change', updateNetworkInfo);

      return () => {
        connection.removeEventListener('change', updateNetworkInfo);
      };
    }
  }, []);

  if (!isOnline) {
    return (
      <div style={{
        backgroundColor: '#f44336',
        color: 'white',
        padding: '8px',
        textAlign: 'center',
        fontSize: '14px'
      }}>
        📱 Offline Mode - Some features may be limited
      </div>
    );
  }

  if (networkInfo && (networkInfo.type === '2g' || networkInfo.type === 'slow-2g')) {
    return (
      <div style={{
        backgroundColor: '#ff9800',
        color: 'white',
        padding: '8px',
        textAlign: 'center',
        fontSize: '14px'
      }}>
        🐌 Slow Connection - Optimizing for your network
      </div>
    );
  }

  return null;
};

// Device info display for development
const DeviceInfoDisplay = ({ deviceInfo }) => (
  <div style={{
    backgroundColor: '#e3f2fd',
    padding: '8px',
    fontSize: '12px',
    borderBottom: '1px solid #ddd'
  }}>
    <strong>Device:</strong> {deviceInfo.type} | <strong>OS:</strong> {deviceInfo.os} | 
    <strong>Screen:</strong> {deviceInfo.screenSize.width}x{deviceInfo.screenSize.height}
  </div>
);

// Mobile bottom navigation component
const MobileBottomNavigation = () => {
  const navItems = [
    { icon: '🏠', label: 'Home', path: '/' },
    { icon: '📊', label: 'Sales', path: '/sales' },
    { icon: '📦', label: 'Inventory', path: '/inventory' },
    { icon: '👥', label: 'Customers', path: '/customers' },
    { icon: '⚙️', label: 'Settings', path: '/settings' }
  ];

  return (
    <nav style={{
      display: 'flex',
      justifyContent: 'space-around',
      alignItems: 'center',
      backgroundColor: 'white',
      borderTop: '1px solid #ddd',
      padding: '8px 0',
      position: 'sticky',
      bottom: 0,
      zIndex: 1000
    }}>
      {navItems.map((item, index) => (
        <button
          key={index}
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            background: 'none',
            border: 'none',
            padding: '8px',
            minWidth: AfricanMobileUIPatterns.spacing.touchTarget,
            minHeight: AfricanMobileUIPatterns.spacing.touchTarget,
            fontSize: '12px',
            color: '#666',
            cursor: 'pointer'
          }}
          onClick={() => console.log(`Navigate to ${item.path}`)}
        >
          <span style={{ fontSize: '20px', marginBottom: '4px' }}>{item.icon}</span>
          <span>{item.label}</span>
        </button>
      ))}
    </nav>
  );
};

// Touch-optimized button component
export const TouchOptimizedButton = ({ 
  children, 
  onClick, 
  variant = 'primary', 
  size = 'medium',
  disabled = false,
  ...props 
}) => {
  const getButtonStyles = () => {
    const baseStyles = {
      minWidth: AfricanMobileUIPatterns.spacing.touchTarget,
      minHeight: AfricanMobileUIPatterns.spacing.touchTarget,
      padding: '12px 24px',
      border: 'none',
      borderRadius: AfricanMobileUIPatterns.spacing.borderRadius,
      fontSize: size === 'large' ? '18px' : size === 'small' ? '14px' : '16px',
      fontWeight: AfricanMobileUIPatterns.typography.fontWeight.medium,
      cursor: disabled ? 'not-allowed' : 'pointer',
      transition: 'all 0.2s ease',
      touchAction: 'manipulation',
      userSelect: 'none',
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      gap: '8px'
    };

    const variantStyles = {
      primary: {
        backgroundColor: disabled ? '#ccc' : AfricanMobileUIPatterns.colors.primary,
        color: 'white'
      },
      secondary: {
        backgroundColor: disabled ? '#f5f5f5' : 'white',
        color: disabled ? '#999' : AfricanMobileUIPatterns.colors.primary,
        border: `2px solid ${disabled ? '#ccc' : AfricanMobileUIPatterns.colors.primary}`
      },
      accent: {
        backgroundColor: disabled ? '#ccc' : AfricanMobileUIPatterns.colors.accent,
        color: 'white'
      }
    };

    return { ...baseStyles, ...variantStyles[variant] };
  };

  return (
    <button
      style={getButtonStyles()}
      onClick={disabled ? undefined : onClick}
      disabled={disabled}
      {...props}
    >
      {children}
    </button>
  );
};

// Touch-optimized input component
export const TouchOptimizedInput = ({ 
  label, 
  type = 'text', 
  placeholder, 
  value, 
  onChange,
  error,
  ...props 
}) => {
  const inputStyles = {
    width: '100%',
    minHeight: AfricanMobileUIPatterns.spacing.touchTarget,
    padding: '12px 16px',
    fontSize: '16px', // Prevents zoom on iOS
    border: `2px solid ${error ? AfricanMobileUIPatterns.colors.error : '#ddd'}`,
    borderRadius: AfricanMobileUIPatterns.spacing.borderRadius,
    backgroundColor: 'white',
    color: '#333',
    outline: 'none',
    transition: 'border-color 0.2s ease'
  };

  const labelStyles = {
    display: 'block',
    marginBottom: '8px',
    fontSize: '14px',
    fontWeight: AfricanMobileUIPatterns.typography.fontWeight.medium,
    color: '#333'
  };

  const errorStyles = {
    color: AfricanMobileUIPatterns.colors.error,
    fontSize: '12px',
    marginTop: '4px'
  };

  return (
    <div style={{ marginBottom: '16px' }}>
      {label && <label style={labelStyles}>{label}</label>}
      <input
        type={type}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        style={inputStyles}
        {...props}
      />
      {error && <div style={errorStyles}>{error}</div>}
    </div>
  );
};

export default MobileOptimizationAgent;
export { 
  MobileDeviceDetector, 
  TouchGestureHandler, 
  MobilePerformanceOptimizer,
  AfricanMobileUIPatterns 
};

