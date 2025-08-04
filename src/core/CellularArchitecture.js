/**
 * WebWaka Digital Operating System - Core Cellular Architecture
 * 
 * This module implements the foundational cellular architecture for WebWaka,
 * providing the base classes and interfaces for Cell, Tissue, and Organ components.
 * 
 * Architecture Philosophy:
 * - Cell: Smallest functional unit with specific capabilities
 * - Tissue: Collection of related cells working together
 * - Organ: Complex system of tissues providing major functionality
 * 
 * African Optimization:
 * - Ubuntu philosophy integration (community-centered design)
 * - Cultural intelligence and local adaptation
 * - Network-adaptive processing for varying infrastructure
 * - Mobile-first and offline-first capabilities
 */

import { EventEmitter } from 'events';

/**
 * Base Cell Class - Fundamental building block of WebWaka
 * 
 * Every component in WebWaka inherits from Cell, providing:
 * - Unique identification and lifecycle management
 * - Event-driven communication
 * - State management and persistence
 * - Cultural intelligence integration
 * - Performance monitoring and optimization
 */
export class Cell extends EventEmitter {
    constructor(config = {}) {
        super();
        
        // Core identification
        this.id = config.id || this.generateId();
        this.type = config.type || 'generic';
        this.name = config.name || `${this.type}-${this.id}`;
        
        // Lifecycle state
        this.state = 'initialized';
        this.created = new Date();
        this.lastUpdated = new Date();
        
        // Configuration and capabilities
        this.config = { ...this.getDefaultConfig(), ...config };
        this.capabilities = new Set(config.capabilities || []);
        
        // African optimization features
        this.culturalContext = config.culturalContext || 'default';
        this.language = config.language || 'en';
        this.networkCondition = config.networkCondition || 'auto';
        
        // Performance tracking
        this.metrics = {
            operations: 0,
            errors: 0,
            responseTime: [],
            lastActivity: new Date()
        };
        
        // Initialize cell
        this.initialize();
    }
    
    /**
     * Generate unique cell identifier
     */
    generateId() {
        return `cell_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }
    
    /**
     * Get default configuration for this cell type
     */
    getDefaultConfig() {
        return {
            autoStart: true,
            persistent: true,
            culturalIntelligence: true,
            offlineCapable: true,
            mobileOptimized: true,
            ubuntuPhilosophy: true
        };
    }
    
    /**
     * Initialize the cell
     */
    async initialize() {
        try {
            this.state = 'initializing';
            this.emit('initializing', { cell: this });
            
            // Setup cultural intelligence
            await this.setupCulturalIntelligence();
            
            // Setup network adaptation
            await this.setupNetworkAdaptation();
            
            // Setup offline capabilities
            await this.setupOfflineCapabilities();
            
            // Start the cell if auto-start is enabled
            if (this.config.autoStart) {
                await this.start();
            }
            
            this.state = 'ready';
            this.emit('ready', { cell: this });
            
        } catch (error) {
            this.state = 'error';
            this.handleError(error);
        }
    }
    
    /**
     * Setup cultural intelligence for African contexts
     */
    async setupCulturalIntelligence() {
        if (!this.config.culturalIntelligence) return;
        
        this.culturalIntelligence = {
            // Ubuntu philosophy: "I am because we are"
            ubuntu: {
                communityFirst: true,
                collectiveDecisionMaking: true,
                elderRespect: true,
                harmonyPreference: true
            },
            
            // Language and communication
            communication: {
                preferredLanguage: this.language,
                culturalNuances: true,
                respectfulTone: true,
                inclusiveLanguage: true
            },
            
            // Business practices
            business: {
                relationshipBased: true,
                trustBuilding: true,
                communityBenefit: true,
                sustainablePractices: true
            }
        };
    }
    
    /**
     * Setup network adaptation for African infrastructure
     */
    async setupNetworkAdaptation() {
        this.networkAdapter = {
            // Detect and adapt to network conditions
            detectCondition: () => {
                // Simulate network detection
                const conditions = ['2G', '3G', '4G', '5G', 'WiFi', 'offline'];
                return this.networkCondition === 'auto' 
                    ? conditions[Math.floor(Math.random() * conditions.length)]
                    : this.networkCondition;
            },
            
            // Optimize operations based on network
            optimize: (operation) => {
                const condition = this.networkAdapter.detectCondition();
                
                switch (condition) {
                    case '2G':
                        return { ...operation, compression: 'high', batch: true, timeout: 30000 };
                    case '3G':
                        return { ...operation, compression: 'medium', batch: true, timeout: 15000 };
                    case '4G':
                    case '5G':
                        return { ...operation, compression: 'low', batch: false, timeout: 5000 };
                    case 'WiFi':
                        return { ...operation, compression: 'none', batch: false, timeout: 3000 };
                    case 'offline':
                        return { ...operation, offline: true, queue: true };
                    default:
                        return operation;
                }
            }
        };
    }
    
    /**
     * Setup offline capabilities
     */
    async setupOfflineCapabilities() {
        if (!this.config.offlineCapable) return;
        
        this.offlineManager = {
            // Queue for offline operations
            operationQueue: [],
            
            // Add operation to queue
            queueOperation: (operation) => {
                this.offlineManager.operationQueue.push({
                    ...operation,
                    timestamp: new Date(),
                    cellId: this.id
                });
            },
            
            // Process queued operations when online
            processQueue: async () => {
                const queue = [...this.offlineManager.operationQueue];
                this.offlineManager.operationQueue = [];
                
                for (const operation of queue) {
                    try {
                        await this.execute(operation);
                    } catch (error) {
                        // Re-queue failed operations
                        this.offlineManager.queueOperation(operation);
                    }
                }
            },
            
            // Check if online
            isOnline: () => {
                return navigator.onLine !== false;
            }
        };
    }
    
    /**
     * Start the cell
     */
    async start() {
        if (this.state === 'running') return;
        
        try {
            this.state = 'starting';
            this.emit('starting', { cell: this });
            
            // Perform startup operations
            await this.onStart();
            
            this.state = 'running';
            this.emit('started', { cell: this });
            
        } catch (error) {
            this.state = 'error';
            this.handleError(error);
        }
    }
    
    /**
     * Stop the cell
     */
    async stop() {
        if (this.state === 'stopped') return;
        
        try {
            this.state = 'stopping';
            this.emit('stopping', { cell: this });
            
            // Perform shutdown operations
            await this.onStop();
            
            this.state = 'stopped';
            this.emit('stopped', { cell: this });
            
        } catch (error) {
            this.handleError(error);
        }
    }
    
    /**
     * Execute an operation with cultural and network optimization
     */
    async execute(operation) {
        const startTime = Date.now();
        
        try {
            // Increment operation counter
            this.metrics.operations++;
            this.metrics.lastActivity = new Date();
            
            // Apply network optimization
            const optimizedOperation = this.networkAdapter.optimize(operation);
            
            // Check if online for network operations
            if (optimizedOperation.requiresNetwork && !this.offlineManager.isOnline()) {
                this.offlineManager.queueOperation(operation);
                return { queued: true, reason: 'offline' };
            }
            
            // Apply cultural intelligence
            const culturallyAdaptedOperation = this.applyCulturalIntelligence(optimizedOperation);
            
            // Execute the operation
            const result = await this.performOperation(culturallyAdaptedOperation);
            
            // Track performance
            const responseTime = Date.now() - startTime;
            this.metrics.responseTime.push(responseTime);
            
            // Keep only last 100 response times
            if (this.metrics.responseTime.length > 100) {
                this.metrics.responseTime = this.metrics.responseTime.slice(-100);
            }
            
            this.emit('operation-completed', { operation, result, responseTime });
            
            return result;
            
        } catch (error) {
            this.metrics.errors++;
            this.handleError(error);
            throw error;
        }
    }
    
    /**
     * Apply cultural intelligence to operations
     */
    applyCulturalIntelligence(operation) {
        if (!this.config.culturalIntelligence) return operation;
        
        const adapted = { ...operation };
        
        // Apply Ubuntu philosophy
        if (this.culturalIntelligence.ubuntu.communityFirst) {
            adapted.priority = 'community';
            adapted.shareResults = true;
        }
        
        // Apply communication preferences
        if (this.culturalIntelligence.communication.respectfulTone) {
            adapted.tone = 'respectful';
            adapted.inclusive = true;
        }
        
        // Apply business practices
        if (this.culturalIntelligence.business.relationshipBased) {
            adapted.buildTrust = true;
            adapted.longTermFocus = true;
        }
        
        return adapted;
    }
    
    /**
     * Perform the actual operation (to be overridden by subclasses)
     */
    async performOperation(operation) {
        // Default implementation
        return { success: true, operation };
    }
    
    /**
     * Handle errors with cultural sensitivity
     */
    handleError(error) {
        this.emit('error', { cell: this, error });
        
        // Log error with cultural context
        console.error(`Cell ${this.name} error:`, {
            error: error.message,
            culturalContext: this.culturalContext,
            language: this.language,
            timestamp: new Date()
        });
    }
    
    /**
     * Get cell status and metrics
     */
    getStatus() {
        return {
            id: this.id,
            type: this.type,
            name: this.name,
            state: this.state,
            created: this.created,
            lastUpdated: this.lastUpdated,
            culturalContext: this.culturalContext,
            language: this.language,
            capabilities: Array.from(this.capabilities),
            metrics: {
                ...this.metrics,
                averageResponseTime: this.metrics.responseTime.length > 0
                    ? this.metrics.responseTime.reduce((a, b) => a + b, 0) / this.metrics.responseTime.length
                    : 0
            }
        };
    }
    
    /**
     * Update cell configuration
     */
    updateConfig(newConfig) {
        this.config = { ...this.config, ...newConfig };
        this.lastUpdated = new Date();
        this.emit('config-updated', { cell: this, config: this.config });
    }
    
    /**
     * Add capability to cell
     */
    addCapability(capability) {
        this.capabilities.add(capability);
        this.emit('capability-added', { cell: this, capability });
    }
    
    /**
     * Remove capability from cell
     */
    removeCapability(capability) {
        this.capabilities.delete(capability);
        this.emit('capability-removed', { cell: this, capability });
    }
    
    /**
     * Check if cell has capability
     */
    hasCapability(capability) {
        return this.capabilities.has(capability);
    }
    
    /**
     * Lifecycle hooks (to be overridden by subclasses)
     */
    async onStart() {
        // Override in subclasses
    }
    
    async onStop() {
        // Override in subclasses
    }
    
    /**
     * Serialize cell state for persistence
     */
    serialize() {
        return {
            id: this.id,
            type: this.type,
            name: this.name,
            config: this.config,
            culturalContext: this.culturalContext,
            language: this.language,
            capabilities: Array.from(this.capabilities),
            created: this.created,
            lastUpdated: this.lastUpdated
        };
    }
    
    /**
     * Deserialize cell state from persistence
     */
    static deserialize(data) {
        const cell = new this(data);
        cell.created = new Date(data.created);
        cell.lastUpdated = new Date(data.lastUpdated);
        return cell;
    }
}

/**
 * Tissue Class - Collection of related cells
 * 
 * Tissues coordinate multiple cells to provide higher-level functionality:
 * - Cell lifecycle management
 * - Inter-cell communication
 * - Load balancing and optimization
 * - Collective decision making (Ubuntu philosophy)
 */
export class Tissue extends Cell {
    constructor(config = {}) {
        super({ ...config, type: 'tissue' });
        
        this.cells = new Map();
        this.cellTypes = new Set();
        this.coordinationStrategy = config.coordinationStrategy || 'ubuntu';
        this.loadBalancer = config.loadBalancer || 'round-robin';
    }
    
    /**
     * Add cell to tissue
     */
    async addCell(cell) {
        if (!(cell instanceof Cell)) {
            throw new Error('Only Cell instances can be added to Tissue');
        }
        
        this.cells.set(cell.id, cell);
        this.cellTypes.add(cell.type);
        
        // Setup cell event listeners
        cell.on('error', (event) => this.handleCellError(event));
        cell.on('operation-completed', (event) => this.handleCellOperation(event));
        
        this.emit('cell-added', { tissue: this, cell });
        
        // Start cell if tissue is running
        if (this.state === 'running' && cell.state !== 'running') {
            await cell.start();
        }
    }
    
    /**
     * Remove cell from tissue
     */
    async removeCell(cellId) {
        const cell = this.cells.get(cellId);
        if (!cell) return;
        
        // Stop cell before removal
        if (cell.state === 'running') {
            await cell.stop();
        }
        
        this.cells.delete(cellId);
        this.emit('cell-removed', { tissue: this, cell });
    }
    
    /**
     * Get cells by type
     */
    getCellsByType(type) {
        return Array.from(this.cells.values()).filter(cell => cell.type === type);
    }
    
    /**
     * Get cells by capability
     */
    getCellsByCapability(capability) {
        return Array.from(this.cells.values()).filter(cell => cell.hasCapability(capability));
    }
    
    /**
     * Execute operation across tissue using Ubuntu coordination
     */
    async execute(operation) {
        const startTime = Date.now();
        
        try {
            // Apply Ubuntu philosophy for collective decision making
            if (this.coordinationStrategy === 'ubuntu') {
                return await this.executeWithUbuntu(operation);
            } else {
                return await this.executeWithLoadBalancing(operation);
            }
            
        } catch (error) {
            this.handleError(error);
            throw error;
        }
    }
    
    /**
     * Execute with Ubuntu philosophy (collective decision making)
     */
    async executeWithUbuntu(operation) {
        const availableCells = Array.from(this.cells.values())
            .filter(cell => cell.state === 'running');
        
        if (availableCells.length === 0) {
            throw new Error('No available cells in tissue');
        }
        
        // Ubuntu approach: seek consensus and collective benefit
        const proposals = await Promise.all(
            availableCells.map(async (cell) => {
                try {
                    // Each cell proposes how to handle the operation
                    return {
                        cell,
                        proposal: await cell.proposeOperation?.(operation) || { canHandle: true, priority: 1 }
                    };
                } catch (error) {
                    return { cell, proposal: { canHandle: false, error } };
                }
            })
        );
        
        // Find consensus (cells that can handle the operation)
        const capableCells = proposals.filter(p => p.proposal.canHandle);
        
        if (capableCells.length === 0) {
            throw new Error('No cells can handle this operation');
        }
        
        // Ubuntu decision: choose based on community benefit and harmony
        const selectedCell = this.selectCellUbuntu(capableCells, operation);
        
        // Execute with selected cell
        const result = await selectedCell.cell.execute(operation);
        
        // Share results with community (Ubuntu principle)
        this.shareResultsWithCommunity(operation, result, selectedCell.cell);
        
        return result;
    }
    
    /**
     * Select cell using Ubuntu principles
     */
    selectCellUbuntu(capableCells, operation) {
        // Ubuntu factors: community benefit, harmony, collective good
        return capableCells.reduce((best, current) => {
            const currentScore = this.calculateUbuntuScore(current, operation);
            const bestScore = this.calculateUbuntuScore(best, operation);
            
            return currentScore > bestScore ? current : best;
        });
    }
    
    /**
     * Calculate Ubuntu score for cell selection
     */
    calculateUbuntuScore(cellProposal, operation) {
        const { cell, proposal } = cellProposal;
        let score = 0;
        
        // Community benefit (how much this helps the collective)
        score += proposal.communityBenefit || 0;
        
        // Harmony (least disruptive to other cells)
        score += proposal.harmony || 0;
        
        // Capability match
        score += proposal.priority || 1;
        
        // Load balancing (give opportunity to less busy cells)
        const avgResponseTime = cell.metrics.responseTime.length > 0
            ? cell.metrics.responseTime.reduce((a, b) => a + b, 0) / cell.metrics.responseTime.length
            : 0;
        score += avgResponseTime < 1000 ? 2 : avgResponseTime < 5000 ? 1 : 0;
        
        // Recent activity (Ubuntu: share the work)
        const timeSinceLastActivity = Date.now() - cell.metrics.lastActivity.getTime();
        score += timeSinceLastActivity > 60000 ? 2 : timeSinceLastActivity > 30000 ? 1 : 0;
        
        return score;
    }
    
    /**
     * Share results with community (Ubuntu principle)
     */
    shareResultsWithCommunity(operation, result, executingCell) {
        // Notify all cells about the operation and result
        this.cells.forEach(cell => {
            if (cell !== executingCell) {
                cell.emit('community-operation', {
                    operation,
                    result,
                    executingCell: executingCell.id,
                    timestamp: new Date()
                });
            }
        });
    }
    
    /**
     * Execute with traditional load balancing
     */
    async executeWithLoadBalancing(operation) {
        const availableCells = Array.from(this.cells.values())
            .filter(cell => cell.state === 'running');
        
        if (availableCells.length === 0) {
            throw new Error('No available cells in tissue');
        }
        
        let selectedCell;
        
        switch (this.loadBalancer) {
            case 'round-robin':
                selectedCell = this.selectRoundRobin(availableCells);
                break;
            case 'least-loaded':
                selectedCell = this.selectLeastLoaded(availableCells);
                break;
            case 'random':
                selectedCell = availableCells[Math.floor(Math.random() * availableCells.length)];
                break;
            default:
                selectedCell = availableCells[0];
        }
        
        return await selectedCell.execute(operation);
    }
    
    /**
     * Handle cell errors with Ubuntu support
     */
    handleCellError(event) {
        const { cell, error } = event;
        
        // Ubuntu approach: community support for struggling members
        this.emit('cell-needs-support', { tissue: this, cell, error });
        
        // Try to redistribute cell's work to other cells
        this.redistributeWork(cell);
    }
    
    /**
     * Redistribute work from struggling cell (Ubuntu mutual support)
     */
    redistributeWork(strugglingCell) {
        // Find healthy cells that can help
        const healthyCells = Array.from(this.cells.values())
            .filter(cell => 
                cell !== strugglingCell && 
                cell.state === 'running' && 
                cell.metrics.errors < 5
            );
        
        if (healthyCells.length > 0) {
            this.emit('work-redistributed', {
                from: strugglingCell.id,
                to: healthyCells.map(c => c.id)
            });
        }
    }
    
    /**
     * Start all cells in tissue
     */
    async onStart() {
        const startPromises = Array.from(this.cells.values()).map(cell => cell.start());
        await Promise.all(startPromises);
    }
    
    /**
     * Stop all cells in tissue
     */
    async onStop() {
        const stopPromises = Array.from(this.cells.values()).map(cell => cell.stop());
        await Promise.all(stopPromises);
    }
    
    /**
     * Get tissue status including all cells
     */
    getStatus() {
        const baseStatus = super.getStatus();
        
        return {
            ...baseStatus,
            cellCount: this.cells.size,
            cellTypes: Array.from(this.cellTypes),
            coordinationStrategy: this.coordinationStrategy,
            cells: Array.from(this.cells.values()).map(cell => cell.getStatus())
        };
    }
}

/**
 * Organ Class - Complex system of tissues
 * 
 * Organs provide major functionality by coordinating multiple tissues:
 * - High-level business logic
 * - Cross-tissue communication
 * - System-wide optimization
 * - Cultural intelligence coordination
 */
export class Organ extends Tissue {
    constructor(config = {}) {
        super({ ...config, type: 'organ' });
        
        this.tissues = new Map();
        this.businessLogic = config.businessLogic || {};
        this.culturalCoordinator = config.culturalCoordinator || true;
    }
    
    /**
     * Add tissue to organ
     */
    async addTissue(tissue) {
        if (!(tissue instanceof Tissue)) {
            throw new Error('Only Tissue instances can be added to Organ');
        }
        
        this.tissues.set(tissue.id, tissue);
        
        // Setup tissue event listeners
        tissue.on('error', (event) => this.handleTissueError(event));
        tissue.on('cell-needs-support', (event) => this.coordinateSupport(event));
        
        this.emit('tissue-added', { organ: this, tissue });
        
        // Start tissue if organ is running
        if (this.state === 'running' && tissue.state !== 'running') {
            await tissue.start();
        }
    }
    
    /**
     * Execute complex operations across multiple tissues
     */
    async execute(operation) {
        // Apply cultural coordination if enabled
        if (this.culturalCoordinator) {
            return await this.executeWithCulturalCoordination(operation);
        } else {
            return await super.execute(operation);
        }
    }
    
    /**
     * Execute with cultural coordination across tissues
     */
    async executeWithCulturalCoordination(operation) {
        // Ubuntu principle: ensure all tissues work in harmony
        const availableTissues = Array.from(this.tissues.values())
            .filter(tissue => tissue.state === 'running');
        
        if (availableTissues.length === 0) {
            // Fall back to direct cell execution
            return await super.execute(operation);
        }
        
        // Coordinate across tissues with cultural intelligence
        const coordinatedOperation = this.applyCulturalCoordination(operation, availableTissues);
        
        // Execute coordinated operation
        return await this.executeCoordinatedOperation(coordinatedOperation);
    }
    
    /**
     * Apply cultural coordination to operation
     */
    applyCulturalCoordination(operation, tissues) {
        return {
            ...operation,
            coordination: {
                ubuntu: true,
                harmony: true,
                collectiveDecision: true,
                culturalSensitivity: true
            },
            tissues: tissues.map(t => t.id),
            culturalContext: this.culturalContext
        };
    }
    
    /**
     * Execute coordinated operation across tissues
     */
    async executeCoordinatedOperation(operation) {
        const { tissues: tissueIds } = operation;
        const tissues = tissueIds.map(id => this.tissues.get(id)).filter(Boolean);
        
        // Ubuntu approach: seek consensus from all tissues
        const proposals = await Promise.all(
            tissues.map(async (tissue) => {
                try {
                    return {
                        tissue,
                        proposal: await tissue.proposeOperation?.(operation) || { canHandle: true, priority: 1 }
                    };
                } catch (error) {
                    return { tissue, proposal: { canHandle: false, error } };
                }
            })
        );
        
        // Find tissues that can contribute
        const capableTissues = proposals.filter(p => p.proposal.canHandle);
        
        if (capableTissues.length === 0) {
            throw new Error('No tissues can handle this operation');
        }
        
        // Execute with cultural harmony
        if (capableTissues.length === 1) {
            return await capableTissues[0].tissue.execute(operation);
        } else {
            return await this.executeCollaboratively(operation, capableTissues);
        }
    }
    
    /**
     * Execute collaboratively across multiple tissues (Ubuntu style)
     */
    async executeCollaboratively(operation, capableTissues) {
        // Ubuntu: work together for collective benefit
        const results = await Promise.all(
            capableTissues.map(async ({ tissue }) => {
                try {
                    return {
                        tissue: tissue.id,
                        result: await tissue.execute(operation),
                        success: true
                    };
                } catch (error) {
                    return {
                        tissue: tissue.id,
                        error: error.message,
                        success: false
                    };
                }
            })
        );
        
        // Combine results harmoniously
        const successfulResults = results.filter(r => r.success);
        const failedResults = results.filter(r => !r.success);
        
        return {
            success: successfulResults.length > 0,
            results: successfulResults,
            failures: failedResults,
            collaboration: true,
            ubuntu: true
        };
    }
    
    /**
     * Coordinate support across tissues (Ubuntu mutual aid)
     */
    coordinateSupport(event) {
        const { tissue: needyTissue, cell, error } = event;
        
        // Find tissues that can provide support
        const supportingTissues = Array.from(this.tissues.values())
            .filter(tissue => 
                tissue !== needyTissue && 
                tissue.state === 'running' &&
                tissue.cells.size > 0
            );
        
        if (supportingTissues.length > 0) {
            this.emit('cross-tissue-support', {
                needyTissue: needyTissue.id,
                supportingTissues: supportingTissues.map(t => t.id),
                cell: cell.id,
                error
            });
        }
    }
    
    /**
     * Start all tissues in organ
     */
    async onStart() {
        // Start tissues first
        const tissueStartPromises = Array.from(this.tissues.values()).map(tissue => tissue.start());
        await Promise.all(tissueStartPromises);
        
        // Then start any direct cells
        await super.onStart();
    }
    
    /**
     * Stop all tissues in organ
     */
    async onStop() {
        // Stop direct cells first
        await super.onStop();
        
        // Then stop tissues
        const tissueStopPromises = Array.from(this.tissues.values()).map(tissue => tissue.stop());
        await Promise.all(tissueStopPromises);
    }
    
    /**
     * Get organ status including all tissues
     */
    getStatus() {
        const baseStatus = super.getStatus();
        
        return {
            ...baseStatus,
            tissueCount: this.tissues.size,
            businessLogic: Object.keys(this.businessLogic),
            culturalCoordinator: this.culturalCoordinator,
            tissues: Array.from(this.tissues.values()).map(tissue => tissue.getStatus())
        };
    }
}

/**
 * CellularSystem - Top-level system coordinator
 * 
 * Manages the entire cellular ecosystem:
 * - System-wide coordination
 * - Cultural intelligence orchestration
 * - Performance optimization
 * - African business logic integration
 */
export class CellularSystem extends Organ {
    constructor(config = {}) {
        super({ ...config, type: 'system' });
        
        this.organs = new Map();
        this.systemMetrics = {
            totalCells: 0,
            totalTissues: 0,
            totalOrgans: 0,
            systemHealth: 100,
            culturalAlignment: 100,
            ubuntuScore: 100
        };
    }
    
    /**
     * Add organ to system
     */
    async addOrgan(organ) {
        if (!(organ instanceof Organ)) {
            throw new Error('Only Organ instances can be added to CellularSystem');
        }
        
        this.organs.set(organ.id, organ);
        this.updateSystemMetrics();
        
        this.emit('organ-added', { system: this, organ });
        
        if (this.state === 'running' && organ.state !== 'running') {
            await organ.start();
        }
    }
    
    /**
     * Update system-wide metrics
     */
    updateSystemMetrics() {
        let totalCells = this.cells.size;
        let totalTissues = this.tissues.size;
        let totalOrgans = this.organs.size;
        
        // Count cells and tissues in organs
        this.organs.forEach(organ => {
            totalCells += organ.cells.size;
            totalTissues += organ.tissues.size;
            
            organ.tissues.forEach(tissue => {
                totalCells += tissue.cells.size;
            });
        });
        
        this.systemMetrics = {
            ...this.systemMetrics,
            totalCells,
            totalTissues,
            totalOrgans,
            lastUpdated: new Date()
        };
    }
    
    /**
     * Get comprehensive system status
     */
    getSystemStatus() {
        this.updateSystemMetrics();
        
        return {
            ...this.getStatus(),
            systemMetrics: this.systemMetrics,
            organs: Array.from(this.organs.values()).map(organ => organ.getStatus()),
            ubuntu: {
                philosophy: 'I am because we are',
                implementation: 'Community-centered cellular architecture',
                culturalIntelligence: true,
                collectiveDecisionMaking: true
            }
        };
    }
}

// Export all classes
export default {
    Cell,
    Tissue,
    Organ,
    CellularSystem
};

