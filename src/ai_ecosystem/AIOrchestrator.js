/**
 * WebWaka AI Ecosystem Orchestrator
 * 
 * Unified orchestration layer for all AI providers:
 * - Eden AI (Primary aggregator)
 * - Hugging Face (African language models)
 * - OpenRouter (LLM diversity)
 * 
 * Features:
 * - Cost optimization across providers
 * - Intelligent provider selection
 * - African language optimization
 * - Cultural intelligence integration
 * - Offline-first capabilities
 */

import { Cell } from '../core/CellularArchitecture.js';

export class AIOrchestrator extends Cell {
    constructor(config = {}) {
        super({
            ...config,
            type: 'ai-orchestrator',
            capabilities: ['ai-coordination', 'cost-optimization', 'cultural-intelligence']
        });
        
        this.providers = new Map();
        this.costTracker = new CostTracker();
        this.culturalIntelligence = new CulturalIntelligenceEngine();
        this.requestQueue = [];
        this.isProcessing = false;
    }
    
    /**
     * Initialize AI providers
     */
    async initialize() {
        await super.initialize();
        
        // Initialize Eden AI
        this.providers.set('eden', new EdenAIProvider({
            apiKey: process.env.EDEN_AI_API_KEY,
            culturalContext: this.culturalContext
        }));
        
        // Initialize Hugging Face
        this.providers.set('huggingface', new HuggingFaceProvider({
            apiKey: process.env.HUGGINGFACE_API_KEY,
            africanLanguages: true
        }));
        
        // Initialize OpenRouter
        this.providers.set('openrouter', new OpenRouterProvider({
            apiKey: process.env.OPENROUTER_API_KEY,
            diversityMode: true
        }));
        
        // Start all providers
        for (const [name, provider] of this.providers) {
            try {
                await provider.initialize();
                this.emit('provider-ready', { name, provider });
            } catch (error) {
                this.emit('provider-error', { name, error });
            }
        }
    }
    
    /**
     * Execute AI operation with optimal provider selection
     */
    async execute(operation) {
        const optimizedOperation = await this.optimizeOperation(operation);
        const selectedProvider = await this.selectOptimalProvider(optimizedOperation);
        
        return await this.executeWithProvider(selectedProvider, optimizedOperation);
    }
    
    /**
     * Optimize operation for African contexts
     */
    async optimizeOperation(operation) {
        const optimized = { ...operation };
        
        // Apply cultural intelligence
        if (this.culturalIntelligence) {
            optimized.culturalContext = await this.culturalIntelligence.analyze(operation);
        }
        
        // Optimize for network conditions
        optimized.networkOptimization = this.networkAdapter.optimize(operation);
        
        // Add cost constraints
        optimized.costConstraints = this.costTracker.getConstraints();
        
        return optimized;
    }
    
    /**
     * Select optimal provider based on operation requirements
     */
    async selectOptimalProvider(operation) {
        const scores = new Map();
        
        for (const [name, provider] of this.providers) {
            if (!provider.isAvailable()) continue;
            
            const score = await this.calculateProviderScore(provider, operation);
            scores.set(name, score);
        }
        
        // Select provider with highest score
        const bestProvider = Array.from(scores.entries())
            .sort(([,a], [,b]) => b - a)[0];
        
        return bestProvider ? bestProvider[0] : 'eden'; // Default to Eden AI
    }
    
    /**
     * Calculate provider score for operation
     */
    async calculateProviderScore(provider, operation) {
        let score = 0;
        
        // Capability match
        score += provider.hasCapability(operation.type) ? 50 : 0;
        
        // Cost efficiency
        const estimatedCost = await provider.estimateCost(operation);
        score += Math.max(0, 30 - estimatedCost * 10);
        
        // Performance history
        score += provider.getPerformanceScore();
        
        // Cultural appropriateness
        if (operation.culturalContext && provider.supportsCulturalContext) {
            score += 20;
        }
        
        // African language support
        if (operation.language && provider.supportsAfricanLanguages) {
            score += 15;
        }
        
        return score;
    }
    
    /**
     * Execute operation with selected provider
     */
    async executeWithProvider(providerName, operation) {
        const provider = this.providers.get(providerName);
        if (!provider) {
            throw new Error(`Provider ${providerName} not available`);
        }
        
        const startTime = Date.now();
        
        try {
            // Track cost before execution
            const estimatedCost = await provider.estimateCost(operation);
            this.costTracker.trackEstimate(providerName, estimatedCost);
            
            // Execute operation
            const result = await provider.execute(operation);
            
            // Track actual cost and performance
            const actualCost = result.cost || estimatedCost;
            const responseTime = Date.now() - startTime;
            
            this.costTracker.trackActual(providerName, actualCost);
            provider.updatePerformance(responseTime, true);
            
            this.emit('operation-completed', {
                provider: providerName,
                operation,
                result,
                cost: actualCost,
                responseTime
            });
            
            return result;
            
        } catch (error) {
            provider.updatePerformance(Date.now() - startTime, false);
            this.emit('operation-failed', {
                provider: providerName,
                operation,
                error
            });
            throw error;
        }
    }
}

/**
 * Cost Tracker for AI operations
 */
class CostTracker {
    constructor() {
        this.dailyBudget = 10.00; // $10 daily budget
        this.monthlyBudget = 200.00; // $200 monthly budget
        this.costs = {
            daily: 0,
            monthly: 0,
            byProvider: new Map()
        };
        this.lastReset = new Date();
    }
    
    /**
     * Track estimated cost
     */
    trackEstimate(provider, cost) {
        this.updateCosts(provider, cost, 'estimated');
    }
    
    /**
     * Track actual cost
     */
    trackActual(provider, cost) {
        this.updateCosts(provider, cost, 'actual');
    }
    
    /**
     * Update cost tracking
     */
    updateCosts(provider, cost, type) {
        // Reset daily costs if needed
        this.checkDailyReset();
        
        this.costs.daily += cost;
        this.costs.monthly += cost;
        
        if (!this.costs.byProvider.has(provider)) {
            this.costs.byProvider.set(provider, { daily: 0, monthly: 0 });
        }
        
        const providerCosts = this.costs.byProvider.get(provider);
        providerCosts.daily += cost;
        providerCosts.monthly += cost;
    }
    
    /**
     * Check if daily reset is needed
     */
    checkDailyReset() {
        const now = new Date();
        const daysDiff = Math.floor((now - this.lastReset) / (1000 * 60 * 60 * 24));
        
        if (daysDiff >= 1) {
            this.costs.daily = 0;
            this.costs.byProvider.forEach(costs => costs.daily = 0);
            this.lastReset = now;
        }
    }
    
    /**
     * Get cost constraints for operations
     */
    getConstraints() {
        return {
            dailyRemaining: Math.max(0, this.dailyBudget - this.costs.daily),
            monthlyRemaining: Math.max(0, this.monthlyBudget - this.costs.monthly),
            canProceed: this.costs.daily < this.dailyBudget && this.costs.monthly < this.monthlyBudget
        };
    }
    
    /**
     * Get cost summary
     */
    getSummary() {
        return {
            daily: {
                spent: this.costs.daily,
                budget: this.dailyBudget,
                remaining: this.dailyBudget - this.costs.daily,
                percentage: (this.costs.daily / this.dailyBudget) * 100
            },
            monthly: {
                spent: this.costs.monthly,
                budget: this.monthlyBudget,
                remaining: this.monthlyBudget - this.costs.monthly,
                percentage: (this.costs.monthly / this.monthlyBudget) * 100
            },
            byProvider: Object.fromEntries(this.costs.byProvider)
        };
    }
}

/**
 * Cultural Intelligence Engine for African contexts
 */
class CulturalIntelligenceEngine {
    constructor() {
        this.culturalProfiles = new Map();
        this.initializeAfricanProfiles();
    }
    
    /**
     * Initialize African cultural profiles
     */
    initializeAfricanProfiles() {
        // Ubuntu philosophy profile
        this.culturalProfiles.set('ubuntu', {
            values: ['community', 'harmony', 'respect', 'sharing'],
            communication: 'respectful and inclusive',
            decisionMaking: 'collective',
            businessApproach: 'relationship-based'
        });
        
        // West African profile
        this.culturalProfiles.set('west-africa', {
            values: ['hospitality', 'storytelling', 'music', 'family'],
            communication: 'expressive and warm',
            decisionMaking: 'elder-guided',
            businessApproach: 'trust-building'
        });
        
        // East African profile
        this.culturalProfiles.set('east-africa', {
            values: ['resilience', 'innovation', 'trade', 'diversity'],
            communication: 'direct but respectful',
            decisionMaking: 'pragmatic',
            businessApproach: 'opportunity-focused'
        });
        
        // Southern African profile
        this.culturalProfiles.set('southern-africa', {
            values: ['ubuntu', 'mining heritage', 'struggle history', 'rainbow nation'],
            communication: 'multilingual and adaptive',
            decisionMaking: 'consensus-seeking',
            businessApproach: 'transformation-minded'
        });
    }
    
    /**
     * Analyze operation for cultural context
     */
    async analyze(operation) {
        const context = {
            region: operation.region || 'general',
            language: operation.language || 'en',
            businessType: operation.businessType || 'general',
            userProfile: operation.userProfile || {}
        };
        
        // Determine cultural profile
        const profile = this.selectCulturalProfile(context);
        
        // Apply cultural adaptations
        return {
            profile: profile.name,
            adaptations: {
                communication: profile.communication,
                values: profile.values,
                businessApproach: profile.businessApproach,
                decisionMaking: profile.decisionMaking
            },
            recommendations: this.generateRecommendations(context, profile)
        };
    }
    
    /**
     * Select appropriate cultural profile
     */
    selectCulturalProfile(context) {
        // Default to Ubuntu philosophy
        let selectedProfile = this.culturalProfiles.get('ubuntu');
        
        // Regional selection
        if (context.region) {
            const regionalProfile = this.culturalProfiles.get(context.region);
            if (regionalProfile) {
                selectedProfile = regionalProfile;
            }
        }
        
        return {
            name: context.region || 'ubuntu',
            ...selectedProfile
        };
    }
    
    /**
     * Generate cultural recommendations
     */
    generateRecommendations(context, profile) {
        const recommendations = [];
        
        // Communication recommendations
        recommendations.push({
            type: 'communication',
            suggestion: `Use ${profile.communication} tone`,
            reason: 'Aligns with cultural communication preferences'
        });
        
        // Business approach recommendations
        recommendations.push({
            type: 'business',
            suggestion: `Adopt ${profile.businessApproach} approach`,
            reason: 'Matches cultural business practices'
        });
        
        // Decision making recommendations
        recommendations.push({
            type: 'decision-making',
            suggestion: `Use ${profile.decisionMaking} process`,
            reason: 'Respects cultural decision-making norms'
        });
        
        return recommendations;
    }
}

/**
 * Base AI Provider class
 */
class AIProvider extends Cell {
    constructor(config = {}) {
        super({
            ...config,
            type: 'ai-provider'
        });
        
        this.apiKey = config.apiKey;
        this.baseUrl = config.baseUrl;
        this.capabilities = new Set(config.capabilities || []);
        this.performance = {
            averageResponseTime: 0,
            successRate: 100,
            totalRequests: 0,
            successfulRequests: 0
        };
    }
    
    /**
     * Check if provider is available
     */
    isAvailable() {
        return this.state === 'running' && this.apiKey;
    }
    
    /**
     * Check if provider has capability
     */
    hasCapability(capability) {
        return this.capabilities.has(capability);
    }
    
    /**
     * Estimate cost for operation
     */
    async estimateCost(operation) {
        // Override in subclasses
        return 0.01; // Default estimate
    }
    
    /**
     * Execute operation
     */
    async execute(operation) {
        // Override in subclasses
        throw new Error('Execute method must be implemented by subclass');
    }
    
    /**
     * Update performance metrics
     */
    updatePerformance(responseTime, success) {
        this.performance.totalRequests++;
        
        if (success) {
            this.performance.successfulRequests++;
        }
        
        this.performance.successRate = 
            (this.performance.successfulRequests / this.performance.totalRequests) * 100;
        
        // Update average response time
        const currentAvg = this.performance.averageResponseTime;
        const totalRequests = this.performance.totalRequests;
        this.performance.averageResponseTime = 
            ((currentAvg * (totalRequests - 1)) + responseTime) / totalRequests;
    }
    
    /**
     * Get performance score
     */
    getPerformanceScore() {
        const responseTimeScore = Math.max(0, 20 - (this.performance.averageResponseTime / 1000));
        const successRateScore = this.performance.successRate * 0.3;
        
        return responseTimeScore + successRateScore;
    }
}

/**
 * Eden AI Provider
 */
class EdenAIProvider extends AIProvider {
    constructor(config = {}) {
        super({
            ...config,
            baseUrl: 'https://api.edenai.run/v2',
            capabilities: [
                'text-generation', 'translation', 'sentiment-analysis',
                'image-generation', 'speech-to-text', 'text-to-speech',
                'document-parsing', 'face-recognition'
            ]
        });
    }
    
    async execute(operation) {
        const endpoint = this.getEndpoint(operation.type);
        const payload = this.buildPayload(operation);
        
        const response = await fetch(`${this.baseUrl}/${endpoint}`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${this.apiKey}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
        
        if (!response.ok) {
            throw new Error(`Eden AI error: ${response.statusText}`);
        }
        
        return await response.json();
    }
    
    getEndpoint(operationType) {
        const endpoints = {
            'text-generation': 'text/generation',
            'translation': 'translation/automatic_translation',
            'sentiment-analysis': 'text/sentiment_analysis',
            'image-generation': 'image/generation',
            'speech-to-text': 'audio/speech_to_text_async',
            'text-to-speech': 'audio/text_to_speech'
        };
        
        return endpoints[operationType] || 'text/generation';
    }
    
    buildPayload(operation) {
        const basePayload = {
            providers: 'openai',
            text: operation.text || operation.prompt,
            language: operation.language || 'en'
        };
        
        // Add operation-specific parameters
        switch (operation.type) {
            case 'text-generation':
                return {
                    ...basePayload,
                    max_tokens: operation.maxTokens || 150,
                    temperature: operation.temperature || 0.7
                };
            case 'translation':
                return {
                    ...basePayload,
                    target_language: operation.targetLanguage || 'en',
                    source_language: operation.sourceLanguage || 'auto'
                };
            default:
                return basePayload;
        }
    }
    
    async estimateCost(operation) {
        // Eden AI pricing estimation
        const baseCost = 0.002; // $0.002 per request
        const tokenMultiplier = (operation.maxTokens || 150) / 1000;
        
        return baseCost * tokenMultiplier;
    }
}

/**
 * Hugging Face Provider
 */
class HuggingFaceProvider extends AIProvider {
    constructor(config = {}) {
        super({
            ...config,
            baseUrl: 'https://api-inference.huggingface.co/models',
            capabilities: [
                'text-generation', 'translation', 'sentiment-analysis',
                'question-answering', 'summarization', 'african-languages'
            ]
        });
        
        this.africanModels = new Map([
            ['sw', 'Helsinki-NLP/opus-mt-en-sw'], // Swahili
            ['yo', 'Helsinki-NLP/opus-mt-en-yo'], // Yoruba
            ['ig', 'Helsinki-NLP/opus-mt-en-ig'], // Igbo
            ['ha', 'Helsinki-NLP/opus-mt-en-ha'], // Hausa
            ['zu', 'Helsinki-NLP/opus-mt-en-zu'], // Zulu
            ['xh', 'Helsinki-NLP/opus-mt-en-xh'], // Xhosa
            ['af', 'Helsinki-NLP/opus-mt-en-af']  // Afrikaans
        ]);
    }
    
    async execute(operation) {
        const model = this.selectModel(operation);
        const payload = this.buildPayload(operation);
        
        const response = await fetch(`${this.baseUrl}/${model}`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${this.apiKey}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
        
        if (!response.ok) {
            throw new Error(`Hugging Face error: ${response.statusText}`);
        }
        
        return await response.json();
    }
    
    selectModel(operation) {
        // Select African language model if available
        if (operation.language && this.africanModels.has(operation.language)) {
            return this.africanModels.get(operation.language);
        }
        
        // Default models by operation type
        const defaultModels = {
            'text-generation': 'gpt2',
            'translation': 'Helsinki-NLP/opus-mt-en-mul',
            'sentiment-analysis': 'cardiffnlp/twitter-roberta-base-sentiment-latest',
            'question-answering': 'deepset/roberta-base-squad2',
            'summarization': 'facebook/bart-large-cnn'
        };
        
        return defaultModels[operation.type] || 'gpt2';
    }
    
    buildPayload(operation) {
        return {
            inputs: operation.text || operation.prompt,
            parameters: {
                max_length: operation.maxTokens || 150,
                temperature: operation.temperature || 0.7,
                do_sample: true
            }
        };
    }
    
    async estimateCost(operation) {
        // Hugging Face is free for inference API
        return 0;
    }
}

/**
 * OpenRouter Provider
 */
class OpenRouterProvider extends AIProvider {
    constructor(config = {}) {
        super({
            ...config,
            baseUrl: 'https://openrouter.ai/api/v1',
            capabilities: [
                'text-generation', 'chat-completion', 'code-generation',
                'reasoning', 'creative-writing'
            ]
        });
    }
    
    async execute(operation) {
        const model = this.selectModel(operation);
        const payload = this.buildPayload(operation, model);
        
        const response = await fetch(`${this.baseUrl}/chat/completions`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${this.apiKey}`,
                'Content-Type': 'application/json',
                'HTTP-Referer': 'https://webwaka.com',
                'X-Title': 'WebWaka Digital Operating System'
            },
            body: JSON.stringify(payload)
        });
        
        if (!response.ok) {
            throw new Error(`OpenRouter error: ${response.statusText}`);
        }
        
        return await response.json();
    }
    
    selectModel(operation) {
        // Select model based on operation requirements and cost
        const models = {
            'creative': 'anthropic/claude-3-haiku',
            'reasoning': 'openai/gpt-4o-mini',
            'code': 'deepseek/deepseek-coder',
            'general': 'meta-llama/llama-3.1-8b-instruct:free',
            'budget': 'google/gemma-2-9b-it:free'
        };
        
        // Use free models when possible
        if (operation.budget === 'free' || operation.cost === 'minimal') {
            return models.budget;
        }
        
        return models[operation.category] || models.general;
    }
    
    buildPayload(operation, model) {
        return {
            model: model,
            messages: [
                {
                    role: 'system',
                    content: this.buildSystemPrompt(operation)
                },
                {
                    role: 'user',
                    content: operation.text || operation.prompt
                }
            ],
            max_tokens: operation.maxTokens || 150,
            temperature: operation.temperature || 0.7
        };
    }
    
    buildSystemPrompt(operation) {
        let systemPrompt = 'You are a helpful AI assistant for WebWaka, a Digital Operating System for African businesses.';
        
        if (operation.culturalContext) {
            systemPrompt += ` Please be culturally sensitive and incorporate ${operation.culturalContext.profile} values.`;
        }
        
        if (operation.language && operation.language !== 'en') {
            systemPrompt += ` Please respond in ${operation.language} when appropriate.`;
        }
        
        return systemPrompt;
    }
    
    async estimateCost(operation) {
        // OpenRouter pricing varies by model
        const model = this.selectModel(operation);
        
        if (model.includes(':free')) {
            return 0;
        }
        
        // Estimate based on tokens and model pricing
        const tokens = (operation.text || operation.prompt || '').length / 4; // Rough token estimate
        const costPerToken = 0.000001; // $0.000001 per token (varies by model)
        
        return tokens * costPerToken;
    }
}

export {
    AIOrchestrator,
    CostTracker,
    CulturalIntelligenceEngine,
    EdenAIProvider,
    HuggingFaceProvider,
    OpenRouterProvider
};

