# WebWaka.com.ng - Netlify Deployment Guide

## 🚀 Complete Production Deployment Instructions

### Step 1: Netlify Project Setup

1. **Login to Netlify**
   - Go to [netlify.com](https://netlify.com)
   - Login to your account

2. **Create New Project**
   - Click **"Projects"** → **"Add new project"**
   - Select **"Import an existing project"**
   - Choose **"Deploy with GitHub"**

3. **Repository Selection**
   - Select **WebWaka** organization
   - Choose **"webwaka-digital-operating-system"** repository
   - Click **"Deploy site"**

### Step 2: Build Configuration

**Netlify will auto-detect the settings, but verify these:**

```
Base directory: .
Build command: cd frontend && npm install && npm run build && cd ../backend && cp -r src/static/* ../frontend/dist/ 2>/dev/null || true
Publish directory: frontend/dist
Functions directory: netlify/functions
```

### Step 3: Domain Configuration

1. **Add Custom Domain**
   - Go to **Project settings** → **"Domain management"**
   - Click **"Add custom domain"**
   - Enter: **webwaka.com.ng**
   - Click **"Verify"**

2. **DNS Configuration**
   Configure these DNS records with your domain provider:

   ```
   Type: CNAME
   Name: www
   Value: [your-netlify-subdomain].netlify.app

   Type: A
   Name: @
   Value: 75.2.60.5

   Type: AAAA (if IPv6 supported)
   Name: @
   Value: 2600:1f14:e22:d200::1
   ```

### Step 4: Environment Variables

In **Project settings** → **"Environment variables"**, add:

```
NODE_VERSION = 18
NPM_VERSION = 9
NODE_ENV = production
REACT_APP_API_URL = https://webwaka.com.ng
REACT_APP_ENVIRONMENT = production
REACT_APP_VERSION = 1.0.0
```

### Step 5: GitHub Secrets Configuration

In your GitHub repository settings → **"Secrets and variables"** → **"Actions"**, add:

1. **NETLIFY_AUTH_TOKEN**
   - Go to Netlify → User settings → Applications → Personal access tokens
   - Generate new token with full access
   - Copy and add to GitHub secrets

2. **NETLIFY_SITE_ID**
   - In Netlify project → Site settings → General → Site details
   - Copy "Site ID"
   - Add to GitHub secrets

### Step 6: SSL Certificate

Netlify will automatically provision SSL certificates for webwaka.com.ng once DNS is configured.

### Step 7: Deployment Verification

Once deployed, verify these endpoints:

- **Main Site:** https://webwaka.com.ng
- **API Health:** https://webwaka.com.ng/api/health
- **API Status:** https://webwaka.com.ng/api/status
- **Sectors:** https://webwaka.com.ng/api/sectors
- **AI Status:** https://webwaka.com.ng/api/ai/status
- **Partners:** https://webwaka.com.ng/api/partners

### Step 8: Performance Optimization

The following are automatically configured:

- ✅ **CDN:** Global content delivery network
- ✅ **Compression:** Gzip/Brotli compression enabled
- ✅ **Caching:** Optimized cache headers
- ✅ **Security:** Security headers and CSP
- ✅ **PWA:** Service worker for offline capabilities
- ✅ **Performance:** Lighthouse score optimization

### Step 9: Monitoring Setup

1. **Netlify Analytics**
   - Enable in Project settings → Analytics
   - Monitor traffic and performance

2. **GitHub Actions**
   - Automated deployment on every push
   - Performance testing with Lighthouse
   - Security scanning

### Troubleshooting

**Common Issues:**

1. **Build Fails**
   - Check Node.js version (should be 18)
   - Verify npm dependencies install correctly
   - Check build logs in Netlify dashboard

2. **Domain Not Working**
   - Verify DNS records are correct
   - Wait 24-48 hours for DNS propagation
   - Check domain registrar settings

3. **API Endpoints Not Working**
   - Verify serverless functions are deployed
   - Check function logs in Netlify dashboard
   - Ensure CORS is properly configured

4. **SSL Certificate Issues**
   - Ensure DNS is properly configured
   - Wait for automatic certificate provisioning
   - Contact Netlify support if needed

### Success Indicators

✅ **Deployment Successful When:**
- Main site loads at https://webwaka.com.ng
- All API endpoints return valid JSON responses
- SSL certificate is active (green lock icon)
- GitHub Actions workflow completes successfully
- Lighthouse performance score > 90

### Support

- **GitHub Repository:** https://github.com/WebWaka/webwaka-digital-operating-system
- **Netlify Documentation:** https://docs.netlify.com
- **WebWaka Support:** Available through GitHub issues

---

**🌍 WebWaka Digital Operating System - Africa's Premier AI-Powered Platform**

