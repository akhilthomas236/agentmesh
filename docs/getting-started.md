# Getting Started with AutoGen A2A

This guide will help you get started with the AutoGen Agent-to-Agent Communication System.

## Installation

### Prerequisites

- Python 3.11 or higher
- Poetry (recommended) or pip
- Docker and Docker Compose (for development environment)

### Option 1: Local Installation with Poetry

```bash
# Clone the repository
git clone <repository-url>
cd autogen-agent

# Install dependencies
poetry install

# Activate the virtual environment
poetry shell
```

### Option 2: Local Installation with pip

```bash
# Clone the repository
git clone <repository-url>
cd autogen-agent

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
pip install -e .
```

### Option 3: Docker Development Environment

```bash
# Clone the repository
git clone <repository-url>
cd autogen-agent

# Start all services
docker-compose up -d

# The API will be available at http://localhost:8000
```

## Quick Start

### 1. CLI Interface

The AutoGen A2A system provides a comprehensive CLI for managing agents and workflows.

#### Basic Commands

```bash
# Show help
agentmesh --help

# Create an agent
agentmesh agent create --name "architect" --type "assistant" --model "gpt-4o"

# List agents
agentmesh agent list

# Create a workflow
agentmesh workflow create --name "code-review" --pattern "sequential"

# List workflows
agentmesh workflow list

# Start the API server
agentmesh server start --port 8000
```

#### Agent Management

```bash
# Create different types of agents
agentmesh agent create --name "architect" --type "assistant" --system-message "You are a software architect"
agentmesh agent create --name "developer" --type "assistant" --system-message "You write clean, efficient code"
agentmesh agent create --name "reviewer" --type "assistant" --system-message "You review code for quality and bugs"

# List all agents
agentmesh agent list

# Get agent details
agentmesh agent get architect

# Start an agent
agentmesh agent start architect

# Stop an agent
agentmesh agent stop architect
```

#### Workflow Management

```bash
# Create a workflow from configuration
agentmesh workflow create --config examples/code-review-workflow.yaml

# Run a workflow
agentmesh workflow run --task "Build a REST API for user management"

# Check workflow status
agentmesh workflow status workflow-123
```

### 2. API Interface

Start the API server:

```bash
agentmesh server start --port 8000
```

The API will be available at `http://localhost:8000` with interactive documentation at `http://localhost:8000/docs`.

#### Basic API Usage

```bash
# Health check
curl http://localhost:8000/health

# Create an agent
curl -X POST "http://localhost:8000/api/v1/agents" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "architect",
    "type": "assistant",
    "model": "gpt-4o",
    "system_message": "You are a software architect"
  }'

# List agents
curl http://localhost:8000/api/v1/agents

# Get agent details
curl http://localhost:8000/api/v1/agents/agent-001
```

### 3. Configuration Files

You can create agents and workflows using YAML configuration files.

#### Agent Configuration

```yaml
# agent-config.yaml
name: "architect"
type: "assistant"
model: "gpt-4o"
system_message: "You are a software architect with 10 years of experience"
config:
  temperature: 0.7
  max_tokens: 1000
```

#### Workflow Configuration

```yaml
# workflow-config.yaml
name: "Code Review Workflow"
pattern: "sequential"
agents:
  - name: "coder"
    type: "assistant"
    config:
      model: "gpt-4o"
      system_message: "You write Python code following best practices"
  - name: "reviewer"
    type: "assistant"
    config:
      model: "gpt-4o"
      system_message: "You review code for quality, bugs, and best practices"
steps:
  - agent: "coder"
    task: "Write the initial code"
  - agent: "reviewer"
    task: "Review the code and suggest improvements"
```

Use the configuration:

```bash
agentmesh agent create --config agent-config.yaml
agentmesh workflow create --config workflow-config.yaml
```

## Development Setup

### Running Tests

```bash
# Install test dependencies
poetry install

# Run tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=autogen_a2a
```

### Code Quality

```bash
# Format code
poetry run black src tests

# Check linting
poetry run flake8 src tests

# Type checking
poetry run mypy src
```

### Development Server

```bash
# Start with auto-reload
agentmesh server start --reload --port 8000

# Or with Docker
docker-compose up agentmesh
```

## Monitoring and Observability

When using the Docker development environment, you get:

- **Prometheus**: Metrics collection at http://localhost:9090
- **Grafana**: Dashboards at http://localhost:3000 (admin/admin)
- **API Documentation**: Interactive docs at http://localhost:8000/docs

## Next Steps

1. **Explore Examples**: Check the `examples/` directory for sample workflows
2. **Read the Documentation**: See `docs/` for detailed guides
3. **Try the API**: Use the interactive documentation at `/docs`
4. **Create Custom Workflows**: Build your own agent workflows
5. **Contribute**: See the contributing guidelines in the main README

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure you've installed all dependencies with `poetry install`
2. **Port Conflicts**: Use different ports with `--port` if 8000 is taken
3. **Docker Issues**: Run `docker-compose down -v` to reset volumes

### Getting Help

- Check the [documentation](../docs/)
- Look at [examples](../examples/)
- Review the [sprint planning](../SPRINT-PLANNING.md) for current features
- Open an issue for bugs or feature requests

## What's Next?

This system is under active development. Check the [Sprint Planning Document](../SPRINT-PLANNING.md) to see what features are being implemented next and track progress.
