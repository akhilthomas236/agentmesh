# Graph Workflow Documentation

## Overview

Graph workflows provide the most flexible orchestration pattern in the AutoGen A2A system, supporting:

- **Conditional Branching**: Route execution based on agent responses or conditions
- **Parallel Execution**: Run multiple agents simultaneously for efficiency  
- **Synchronization Points**: Wait for multiple parallel paths to complete
- **Complex Dependencies**: Model sophisticated workflows with arbitrary connections
- **Dynamic Routing**: Modify workflow paths during execution
- **Quality Gates**: Implement approval and validation checkpoints

## Configuration Structure

### Basic Graph Workflow

```yaml
name: "My Graph Workflow"
pattern: "graph"

agents:
  - name: "agent1"
    type: "chat"
  - name: "agent2" 
    type: "chat"
  - name: "agent3"
    type: "chat"

graph:
  nodes:
    - id: "start"
      agent: "agent1"
      description: "Starting node"
    - id: "process"
      agent: "agent2"
      description: "Processing node"
    - id: "finish"
      agent: "agent3"
      description: "Final node"
  
  edges:
    - id: "start_to_process"
      source: "start"
      target: "process"
      type: "sequential"
    - id: "process_to_finish"
      source: "process"
      target: "finish"
      type: "conditional"
      condition: "approval"
  
  conditions:
    approval:
      type: "evaluation"
      criteria: ["quality_check"]
```

## Node Configuration

Each node represents an agent execution step:

```yaml
nodes:
  - id: "unique_node_id"          # Required: Unique identifier
    agent: "agent_name"           # Required: Agent to execute
    description: "Node purpose"   # Optional: Human readable description
    max_retries: 3               # Optional: Retry attempts (default: 3)
    timeout: 600                 # Optional: Timeout in seconds
    input_schema:                # Optional: Expected input structure
      type: "object"
      properties:
        data: {"type": "string"}
    output_schema:               # Optional: Expected output structure
      type: "object"
      properties:
        result: {"type": "string"}
```

## Edge Types

### Sequential Edges
Simple one-after-another execution:

```yaml
edges:
  - id: "seq_edge"
    source: "node1"
    target: "node2"
    type: "sequential"
```

### Parallel Edges
Trigger multiple nodes simultaneously:

```yaml
edges:
  - id: "parallel1"
    source: "start"
    target: "worker1" 
    type: "parallel"
  - id: "parallel2"
    source: "start"
    target: "worker2"
    type: "parallel"
```

### Conditional Edges
Execute based on conditions:

```yaml
edges:
  - id: "conditional_edge"
    source: "decision_node"
    target: "target_node"
    type: "conditional"
    condition: "approval_check"
```

### Synchronization Edges
Wait for multiple paths to complete:

```yaml
edges:
  - id: "sync1"
    source: "worker1"
    target: "merger"
    type: "synchronize"
  - id: "sync2"
    source: "worker2"
    target: "merger"
    type: "synchronize"
```

## Parallel Execution

Define parallel branches that execute simultaneously:

```yaml
parallel_branches:
  - id: "research_phase"
    nodes: ["market_research", "tech_research", "user_research"]
    synchronization_node: "synthesis"
  
  - id: "development_phase"
    nodes: ["frontend_dev", "backend_dev", "database_setup"]
    synchronization_node: "integration"
```

## Conditional Logic

### Evaluation Conditions
Check multiple criteria:

```yaml
conditions:
  quality_gate:
    type: "evaluation"
    criteria: ["code_quality", "test_coverage", "performance"]
    timeout: 300
```

### Approval Conditions
Require specific agent approval:

```yaml
conditions:
  manager_approval:
    type: "approval"
    required_approval: "project_manager"
    timeout: 600
```

### Consensus Conditions
Require agreement from multiple agents:

```yaml
conditions:
  team_consensus:
    type: "consensus"
    required_agents: ["tech_lead", "product_manager", "qa_lead"]
    timeout: 900
```

## Advanced Features

### Feedback Loops
Create revision cycles:

```yaml
edges:
  - id: "review_feedback"
    source: "reviewer"
    target: "developer"
    type: "conditional"
    condition: "needs_revision"
```

### Quality Gates
Implement checkpoints:

```yaml
nodes:
  - id: "quality_checkpoint"
    agent: "qa_agent"
    description: "Quality gate - must pass to continue"

conditions:
  quality_pass:
    type: "evaluation"
    criteria: ["test_results", "code_review", "performance_check"]
```

### Dynamic Routing
Route based on runtime conditions:

```yaml
conditions:
  complexity_routing:
    type: "evaluation"
    criteria: ["task_complexity_high"]
    # Routes to expert agent if complexity is high
```

## CLI Commands

### Create Graph Workflow
```bash
agentmesh workflow create --config graph-workflow.yaml
```

### Visualize Graph Structure
```bash
# ASCII visualization
agentmesh workflow visualize workflow-123 --format ascii

# Mermaid diagram
agentmesh workflow visualize workflow-123 --format mermaid > workflow.md

# JSON structure
agentmesh workflow visualize workflow-123 --format json
```

### Monitor Execution
```bash
# Get detailed status
agentmesh workflow get workflow-123

# Real-time monitoring
agentmesh workflow get workflow-123 --watch
```

### Control Execution
```bash
# Pause workflow
agentmesh workflow pause workflow-123

# Resume workflow
agentmesh workflow resume workflow-123

# Cancel workflow
agentmesh workflow cancel workflow-123
```

## API Endpoints

### Get Graph Structure
```http
GET /api/v1/workflows/{workflow_id}/graph
```

Returns graph nodes, edges, and current execution state.

### Get Execution History
```http
GET /api/v1/workflows/{workflow_id}/history
```

Returns detailed execution timeline and message flow.

### Validate Configuration
```http
POST /api/v1/workflows/validate
Content-Type: application/json

{
  "name": "test-workflow",
  "pattern": "graph",
  "agents": [...],
  "graph": {...}
}
```

### Control Workflow
```http
POST /api/v1/workflows/{workflow_id}/pause
POST /api/v1/workflows/{workflow_id}/resume
POST /api/v1/workflows/{workflow_id}/cancel
```

## Best Practices

### 1. Design Principles
- **Start Simple**: Begin with linear flows, add complexity gradually
- **Clear Dependencies**: Make node dependencies explicit
- **Error Handling**: Plan for failure scenarios and recovery paths
- **Timeouts**: Set appropriate timeouts for all nodes
- **Documentation**: Use descriptive names and descriptions

### 2. Performance Optimization
- **Parallel Execution**: Use parallel branches for independent tasks
- **Resource Management**: Consider agent capacity and resource limits
- **Batch Operations**: Group related operations where possible
- **Caching**: Cache intermediate results when appropriate

### 3. Monitoring and Debugging
- **Visualization**: Use graph visualization to understand flow
- **Logging**: Enable detailed logging for debugging
- **Checkpoints**: Add validation nodes at critical points
- **Metrics**: Monitor execution time and success rates

### 4. Common Patterns

#### Approval Workflow
```yaml
# Review -> Approval -> Action pattern
edges:
  - id: "review_to_approval"
    source: "content_review"
    target: "manager_approval"
    type: "sequential"
  - id: "approval_to_publish"
    source: "manager_approval"
    target: "publish_content"
    type: "conditional"
    condition: "approved"
```

#### Parallel Processing with Merge
```yaml
# Fork -> Process -> Merge pattern
parallel_branches:
  - id: "processing_branch"
    nodes: ["process_a", "process_b", "process_c"]
    synchronization_node: "merge_results"
```

#### Quality Gate Pattern
```yaml
# Development -> Test -> Quality Gate -> Deploy
conditions:
  quality_gate:
    type: "evaluation"
    criteria: ["tests_pass", "coverage_ok", "security_clear"]
```

## Troubleshooting

### Common Issues

1. **Circular Dependencies**
   - Check for loops in your edge definitions
   - Use visualization to identify cycles
   - Break cycles with conditional logic

2. **Deadlocks**
   - Ensure synchronization nodes can be reached
   - Check parallel branch configurations
   - Verify condition logic

3. **Performance Issues**
   - Check for inefficient sequential chains
   - Optimize parallel execution
   - Adjust timeouts and retry counts

4. **Failed Conditions**
   - Verify condition logic and criteria
   - Check agent response formats
   - Review timeout settings

### Debug Commands

```bash
# Validate configuration
agentmesh workflow validate config.yaml

# Check workflow status
agentmesh workflow get workflow-123 --format json

# View execution history
agentmesh workflow history workflow-123

# Visualize current state
agentmesh workflow visualize workflow-123 --include-state
```

## Examples

See the `examples/workflows/` directory for complete examples:

- `graph-code-review.yaml` - Simple code review workflow
- `graph-product-development.yaml` - Complex product development pipeline
- `graph-advanced-product-development.yaml` - Advanced multi-stage development
- `graph-content-creation-pipeline.yaml` - Content creation with quality gates

Each example demonstrates different aspects of graph workflow capabilities and can be used as templates for your own workflows.
