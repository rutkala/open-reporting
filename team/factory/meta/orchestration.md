# Factory Orchestration Meta-Layer

## Overview
The orchestrator is a meta-layer (not a workstation) that manages DAG execution.

## Responsibilities

### 1. DAG Reading
- Reads all DAG files from `team/factory/dag/`
- Distinguishes workstation DAGs from product DAGs
- Builds dependency graph

### 2. Topological Sort
- Determines execution order based on dependencies
- Identifies which steps can run in parallel
- Blocks on unresolved dependencies

### 3. Parallel Execution
- Runs independent workstations simultaneously
- Maximizes throughput while respecting dependencies
- Handles artifact passing between DAGs

### 4. Artifact Passing
- Outputs from one DAG become inputs to dependent DAGs
- Maintains artifact chain through the execution
- Handles missing artifacts gracefully

### 5. Metrics Collection
- Logs execution time per step
- Tracks tokens used
- Records iterations to pass
- Counts defects

### 6. Improvement Trigger
- Analyzes accumulated metrics
- Can improve instructions/standards based on patterns
- Reports bottlenecks

## Execution Flow

```
User Request
    ↓
DAG Loader (reads product DAG)
    ↓
Dependency Analyzer (topological sort)
    ↓
Executor (runs steps in order/parallel)
    ↓
Metrics Collector (logs performance)
    ↓
Result (product + metrics)
```

## DAG File Types

### Workstation DAG
- Defines internal steps for a workstation
- Each step has dev+test agents
- Produces reusable artifacts

### Product DAG
- Links workstation DAGs together
- Defines dependencies between workstations
- References parallel execution opportunities

## Current DAG Files

### Workstations (13)
- business-analysis.yaml
- architecture.yaml
- data-engineering.yaml
- ux-ui-design.yaml
- full-stack-development.yaml
- quality-assurance.yaml
- devops.yaml
- analytics.yaml
- business-domain.yaml
- content-creation.yaml
- infrastructure.yaml
- security.yaml
- research.yaml

### Products
- dashboard.yaml
- blog.yaml
- research-product.yaml