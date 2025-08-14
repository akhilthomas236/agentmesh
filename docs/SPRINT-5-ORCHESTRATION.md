# Sprint 5: Sequential & Round-Robin Orchestration

## Overview

Sprint 5 implements advanced orchestration patterns for the AutoGen Agent-to-Agent (A2A) Communication System, focusing on Sequential and Round-Robin workflow execution patterns.

## Completed Features

### 1. Orchestration Framework

#### Base Orchestration Classes
- **BaseOrchestrator**: Abstract base class for all orchestration patterns
- **OrchestrationPattern**: Enumeration of supported patterns (Sequential, Round-Robin, Graph, Swarm)
- **WorkflowConfig**: Configuration model for orchestration workflows
- **WorkflowStatus**: Workflow state management (Created, Running, Paused, Completed, Failed, Cancelled)
- **TaskResult**: Standardized result format for workflow execution
- **TerminationCondition**: Configurable workflow termination criteria

#### Sequential Orchestrator
- **SequentialOrchestrator**: Implements sequential agent execution pattern
- Agents process tasks in order, with each agent receiving the output from the previous one
- Built-in retry logic with configurable attempts
- Error handling and graceful failure management
- Progress tracking and execution metadata

#### Round-Robin Orchestrator  
- **RoundRobinOrchestrator**: Implements round-robin agent execution pattern
- Agents take turns processing the task across multiple rounds
- Configurable termination conditions (max rounds, max messages, timeout)
- Dynamic conversation flow with message accumulation
- Agent rotation and fair participation

### 2. Message Models

#### Core Message Types
- **BaseChatMessage**: Abstract base for all message types
- **TextMessage**: Plain text messages with sender information
- **SystemMessage**: System-level messages and notifications
- **ErrorMessage**: Error handling and reporting
- **MetadataMessage**: Workflow metadata and state information

#### Message Features
- Unique message IDs with timestamps
- Sender identification and routing
- Message validation and serialization
- Rich metadata support

### 3. Workflow Configuration System

#### Configuration Models
- **WorkflowConfigFile**: Complete workflow definition from YAML/JSON files
- **WorkflowAgentConfig**: Agent-specific configuration within workflows
- **WorkflowTerminationConfig**: Termination criteria configuration
- **WorkflowTemplate**: Reusable workflow templates with parameters

#### Configuration Manager
- **WorkflowConfigManager**: Central configuration management
- YAML and JSON configuration file support
- Configuration validation with detailed error reporting
- Template instantiation with parameter substitution
- Agent name to ID mapping resolution

### 4. Workflow Management

#### Workflow Manager
- **WorkflowManager**: Central workflow lifecycle management
- Workflow creation from configuration files or templates
- Execution management (start, pause, resume, cancel)
- Status monitoring and progress tracking
- Template management and instantiation

#### Workflow Execution
- **WorkflowExecution**: Wrapper for orchestrator delegation
- Execution metadata tracking (timing, status, progress)
- Result aggregation and reporting
- Error handling and recovery

### 5. REST API Endpoints

#### Workflow API Router (`/workflows`)
- **POST /workflows**: Create new workflows from configuration
- **GET /workflows**: List all workflows with optional status filtering
- **POST /workflows/{id}/execute**: Execute workflow with task and parameters
- **GET /workflows/{id}**: Get detailed workflow status and information
- **POST /workflows/{id}/pause**: Pause running workflow
- **POST /workflows/{id}/resume**: Resume paused workflow
- **DELETE /workflows/{id}**: Cancel and remove workflow
- **GET /workflows/templates**: List available workflow templates
- **POST /workflows/templates/{id}**: Create workflow from template

#### API Features
- Request/response models with Pydantic validation
- Comprehensive error handling and status codes
- Asynchronous execution support
- Progress monitoring capabilities

### 6. CLI Commands

#### Workflow CLI (`agentmesh workflow`)
- **create**: Create workflows from configuration files
- **list**: List workflows with filtering and formatting options
- **execute**: Execute workflows with tasks and parameters
- **get**: Get detailed workflow status and information
- **cancel**: Cancel running workflows
- **validate**: Validate workflow configuration files
- **templates**: List available workflow templates

#### CLI Features
- Rich terminal output with colors and tables
- JSON and table output formats
- Progress indicators for long-running operations
- Comprehensive help and examples

### 7. Example Configurations

#### Sequential Code Review Workflow
```yaml
name: "code-review-sequential"
pattern: "sequential"
agents:
  - name: "architect"
    type: "assistant"
    config:
      model: "gpt-3.5-turbo"
      system_message: "You are a software architect..."
  - name: "developer"
    type: "assistant"
  - name: "reviewer"
    type: "assistant"
```

#### Round-Robin Brainstorming Workflow
```yaml
name: "brainstorming-roundrobin"
pattern: "round-robin"
agents:
  - name: "creative"
  - name: "analytical"
  - name: "critic"
  - name: "facilitator"
termination:
  max_rounds: 5
  max_messages: 20
  timeout_seconds: 1800
```

## Architecture

### Orchestration Flow
1. **Configuration Loading**: YAML/JSON files parsed into configuration models
2. **Agent Resolution**: Agent names mapped to registered agent IDs
3. **Orchestrator Creation**: Appropriate orchestrator instantiated based on pattern
4. **Workflow Execution**: Tasks distributed according to orchestration pattern
5. **Result Aggregation**: Outputs collected and formatted
6. **Status Reporting**: Progress and completion status tracked

### Integration Points
- **Agent Manager**: Agent discovery and communication
- **Message Bus**: Inter-agent message routing
- **Context Manager**: Conversation context management
- **API Router**: REST endpoint registration
- **CLI Handler**: Command-line interface integration

## Testing

### Validation Testing
- Configuration file validation for all supported patterns
- Error detection for invalid configurations
- Agent mapping validation

### Workflow Creation Testing
- Workflow instantiation from configuration files
- Template-based workflow creation
- Agent ID resolution and mapping

### CLI Integration Testing
- Command-line argument parsing
- Output formatting (table and JSON)
- Error handling and user feedback

### API Integration Testing
- Workflow creation through REST endpoints
- Status monitoring and progress tracking
- Template listing and instantiation

## File Structure

```
src/autogen_a2a/
├── orchestration/
│   ├── __init__.py
│   ├── base.py              # Base orchestration classes
│   ├── sequential.py        # Sequential orchestrator
│   └── round_robin.py       # Round-robin orchestrator
├── workflows/
│   ├── __init__.py
│   ├── config.py           # Configuration management
│   └── manager.py          # Workflow lifecycle management
├── models/
│   ├── __init__.py
│   └── message.py          # Message models
├── api/routers/
│   └── workflows.py        # REST API endpoints
└── cli/commands/
    └── workflow.py         # CLI commands

examples/workflows/
├── sequential-code-review.yaml
└── roundrobin-brainstorming.yaml
```

## Usage Examples

### CLI Usage
```bash
# Validate configuration
agentmesh workflow validate examples/workflows/sequential-code-review.yaml

# Create workflow
agentmesh workflow create --config examples/workflows/sequential-code-review.yaml

# List workflows
agentmesh workflow list --status running

# Execute workflow
agentmesh workflow execute workflow-123 --task "Review this code"

# List templates
agentmesh workflow templates
```

### API Usage
```python
# Create workflow
POST /workflows
{
  "config": {...},
  "agent_mapping": {"architect": "agent-123"}
}

# Execute workflow
POST /workflows/{id}/execute
{
  "task": "Review this code",
  "parameters": {"timeout": 600}
}

# Get status
GET /workflows/{id}
```

## Next Steps

### Planned Enhancements
1. **Graph Orchestration**: Implement graph-based workflow patterns
2. **Swarm Orchestration**: Implement swarm intelligence patterns
3. **Real Agent Integration**: Connect with actual agent implementations
4. **Workflow Persistence**: Database storage for workflow state
5. **Advanced Templates**: Template library with categories and examples
6. **Monitoring & Metrics**: Performance monitoring and analytics
7. **Integration Testing**: End-to-end testing with real agents

### Technical Debt
1. **Agent Manager Integration**: Complete integration with agent registry
2. **Message Bus Integration**: Full message routing implementation
3. **Error Recovery**: Advanced error handling and recovery mechanisms
4. **Performance Optimization**: Optimize for large-scale workflows
5. **Security**: Authentication and authorization for API endpoints
