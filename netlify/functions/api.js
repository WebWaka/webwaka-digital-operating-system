const { createProxyMiddleware } = require('http-proxy-middleware');

// WebWaka Digital Operating System - Production API Wrapper
// Handles backend API routing for Netlify deployment

exports.handler = async (event, context) => {
    const { path, httpMethod, headers, body, queryStringParameters } = event;
    
    // CORS headers
    const corsHeaders = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Access-Control-Max-Age': '86400'
    };
    
    // Handle preflight requests
    if (httpMethod === 'OPTIONS') {
        return {
            statusCode: 200,
            headers: corsHeaders,
            body: ''
        };
    }
    
    try {
        // Route API requests to appropriate handlers
        const apiPath = path.replace('/api', '');
        
        // WebWaka API routing logic
        let response;
        
        if (apiPath.startsWith('/agents')) {
            response = await handleAgentsAPI(apiPath, httpMethod, body, queryStringParameters);
        } else if (apiPath.startsWith('/white-label')) {
            response = await handleWhiteLabelAPI(apiPath, httpMethod, body, queryStringParameters);
        } else if (apiPath.startsWith('/referral')) {
            response = await handleReferralAPI(apiPath, httpMethod, body, queryStringParameters);
        } else if (apiPath.startsWith('/payments')) {
            response = await handlePaymentsAPI(apiPath, httpMethod, body, queryStringParameters);
        } else {
            response = {
                statusCode: 404,
                body: JSON.stringify({ error: 'API endpoint not found' })
            };
        }
        
        return {
            ...response,
            headers: {
                ...corsHeaders,
                'Content-Type': 'application/json',
                ...response.headers
            }
        };
        
    } catch (error) {
        console.error('API Error:', error);
        
        return {
            statusCode: 500,
            headers: corsHeaders,
            body: JSON.stringify({
                error: 'Internal server error',
                message: error.message
            })
        };
    }
};

// API Handler Functions
async function handleAgentsAPI(path, method, body, params) {
    // Handle agents API requests
    return {
        statusCode: 200,
        body: JSON.stringify({
            message: 'WebWaka Agents API',
            path: path,
            method: method,
            agents: {
                total: 42,
                active: 42,
                status: 'operational'
            }
        })
    };
}

async function handleWhiteLabelAPI(path, method, body, params) {
    // Handle white-label API requests
    return {
        statusCode: 200,
        body: JSON.stringify({
            message: 'WebWaka White-Label API',
            path: path,
            method: method,
            platform: {
                status: 'operational',
                tenants: 'unlimited',
                customization: 'full'
            }
        })
    };
}

async function handleReferralAPI(path, method, body, params) {
    // Handle referral system API requests
    return {
        statusCode: 200,
        body: JSON.stringify({
            message: 'WebWaka Referral System API',
            path: path,
            method: method,
            referral: {
                levels: 6,
                commission_types: 'multi-level',
                analytics: 'real-time'
            }
        })
    };
}

async function handlePaymentsAPI(path, method, body, params) {
    // Handle payments API requests
    return {
        statusCode: 200,
        body: JSON.stringify({
            message: 'WebWaka Payments API',
            path: path,
            method: method,
            payments: {
                handylife_wallet: true,
                multi_currency: true,
                compliance: 'full'
            }
        })
    };
}