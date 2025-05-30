class OperationVisualizer {
    static generateOperationDescription(opType, details) {
        let description = 'OPERATION ANALYSIS:\n';
        description += '━━━━━━━━━━━━━━━━━━\n';
        
        const impacts = {
            CPU: 'Performance impact on CPU execution cycles',
            MEMORY: 'Memory access patterns and cache behavior',
            IO: 'Impact on system I/O operations',
            SECURITY: 'Potential security implications'
        };

        for (const [aspect, impact] of Object.entries(impacts)) {
            description += `${aspect}: ${this.analyzeImpact(opType, aspect)}\n`;
            description += `├─ ${impact}\n`;
            description += `└─ Severity: ${this.calculateSeverity(opType, aspect)}\n\n`;
        }

        return description;
    }

    static analyzeImpact(opType, aspect) {
        // Simulate impact analysis
        const impacts = ['MINIMAL', 'MODERATE', 'SIGNIFICANT', 'CRITICAL'];
        return impacts[Math.floor(Math.random() * impacts.length)];
    }

    static calculateSeverity(opType, aspect) {
        return Math.floor(Math.random() * 100);
    }
}
