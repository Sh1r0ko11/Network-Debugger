class OperationNomenclature {
    static OPERATIONS = {
        CPU: {
            FETCH: 'InstructionCacheFetch',
            DECODE: 'MicrooperationDecode',
            EXECUTE: 'ArithmeticLogicExecution',
            WRITEBACK: 'RegisterWriteBack',
            SIMD: 'VectorizedSIMDExecution',
            FPU: 'FloatingPointCoprocessor',
            MMX: 'MultiMediaExtensions',
            SSE: 'StreamingSIMDExtensions',
            AVX: 'AdvancedVectorExtensions'
        },
        MEMORY: {
            READ: 'MemoryPageTableAccess',
            WRITE: 'MemorySegmentWrite',
            SWAP: 'VirtualMemoryPageSwap',
            ALLOC: 'HeapSegmentAllocation',
            TLB: 'TranslationLookaside',
            PREFETCH: 'CachePrefetchQueue',
            WRITEBACK: 'CacheWriteBack',
            COHERENCY: 'CacheCoherencyProtocol'
        },
        PIPELINE: {
            STALL: 'PipelineHazardStall',
            FLUSH: 'BranchMispredictionFlush',
            RETIRE: 'InstructionRetirement'
        }
    };

    static getFullOperationName(category, operation, address) {
        return `${this.OPERATIONS[category][operation]}@0x${address.toString(16)} [${performance.now().toFixed(6)}μs]`;
    }

    static getExtendedOperationName(category, operation, address) {
        const timestamp = performance.now().toFixed(9);
        const cpuCycle = Math.floor(timestamp * 3.6e9 % 0xFFFFFFFF);
        return `${this.OPERATIONS[category][operation]}@0x${address.toString(16)} ` +
               `[TSC:${cpuCycle.toString(16)}] [${timestamp}ns]`;
    }
}
