# Swarm Coordination Documentation

## Overview

Swarm coordination provides autonomous agent collaboration in the AutoGen A2A system, enabling:

- **Autonomous Handoffs**: Agents autonomously decide when and to whom to hand off tasks
- **Self-Organization**: Dynamic adaptation to task requirements and agent capabilities  
- **Emergent Behavior**: Complex problem-solving through agent interaction
- **Real-Time Monitoring**: Comprehensive metrics and analytics for swarm behavior
- **Parameter Tuning**: Dynamic adjustment of swarm behavior during execution

## Key Concepts

### Swarm Participants
Each agent in the swarm is defined as a participant with:
- **Specializations**: Areas of expertise for autonomous routing
- **Handoff Targets**: Preferred agents for task handoffs
- **Participation Weight**: Influence on selection probability
- **Consecutive Turn Limits**: Maximum consecutive actions before handoff

### Handoff Types
- **Autonomous**: Agent decides to handoff based on task analysis
- **Broadcast**: Message sent to all swarm participants
- **Targeted**: Specific agent selection based on specialization
- **Random**: Random selection for load balancing

### Termination Conditions
- **Max Messages**: Stop after a certain number of messages
- **Consensus**: Stop when agents reach agreement
- **Timeout**: Stop after specified time duration
- **Task Completion**: Stop when task is marked as complete

## Configuration Structure

### Basic Swarm Configuration

```yaml
name: "Research Analysis Swarm"
pattern: "swarm"

agents:
  - name: "data_collector"
    type: "assistant"
    system_message: "You specialize in collecting and gathering research data"
  - name: "analyst"
    type: "assistant" 
    system_message: "You analyze data and identify patterns and insights"
  - name: "statistician"
    type: "assistant"
    system_message: "You perform statistical analysis and validation"
  - name: "report_generator"
    type: "assistant"
    system_message: "You create comprehensive research reports"

swarm:
  participants:
    - agent: "data_collector"
      specializations: ["data_collection", "web_scraping", "api_integration"]
      handoff_targets: ["analyst", "statistician"]
      participation_weight: 1.2
      max_consecutive_turns: 3
    
    - agent: "analyst"
      specializations: ["data_analysis", "pattern_recognition", "insights"]
      handoff_targets: ["statistician", "report_generator"]
      participation_weight: 1.0
      max_consecutive_turns: 4
    
    - agent: "statistician"
      specializations: ["statistics", "validation", "hypothesis_testing"]
      handoff_targets: ["analyst", "report_generator"]
      participation_weight: 0.8
      max_consecutive_turns: 2
    
    - agent: "report_generator"
      specializations: ["writing", "reporting", "documentation"]
      handoff_targets: ["analyst"]
      participation_weight: 1.0
      max_consecutive_turns: 3

  termination:
    type: "max_messages"
    value: 25
    fallback_timeout: 1800  # 30 minutes

  handoff_config:
    autonomous_threshold: 0.7
    broadcast_threshold: 0.3
    random_selection_probability: 0.1
```

### Advanced Swarm Configuration

```yaml
name: "Product Development Swarm"
pattern: "swarm"

agents:
  - name: "product_manager"
    type: "assistant"
    system_message: "You manage product requirements and roadmap"
  - name: "tech_lead"
    type: "assistant"
    system_message: "You provide technical leadership and architecture guidance"
  - name: "developer"
    type: "assistant"
    system_message: "You implement features and write code"
  - name: "qa_engineer"
    type: "assistant"
    system_message: "You ensure quality through testing and validation"
  - name: "ui_designer"
    type: "assistant"
    system_message: "You design user interfaces and user experience"

swarm:
  participants:
    - agent: "product_manager"
      specializations: ["requirements", "roadmap", "stakeholder_management"]
      handoff_targets: ["tech_lead", "ui_designer"]
      participation_weight: 1.5
      max_consecutive_turns: 5
      priority_keywords: ["requirements", "roadmap", "business"]
    
    - agent: "tech_lead"
      specializations: ["architecture", "technical_design", "code_review"]
      handoff_targets: ["developer", "qa_engineer"]
      participation_weight: 1.3
      max_consecutive_turns: 4
      priority_keywords: ["architecture", "design", "technical"]
    
    - agent: "developer"
      specializations: ["implementation", "coding", "debugging"]
      handoff_targets: ["tech_lead", "qa_engineer"]
      participation_weight: 1.0
      max_consecutive_turns: 6
      priority_keywords: ["code", "implement", "develop"]
    
    - agent: "qa_engineer"
      specializations: ["testing", "quality_assurance", "validation"]
      handoff_targets: ["developer", "tech_lead"]
      participation_weight: 1.1
      max_consecutive_turns: 3
      priority_keywords: ["test", "quality", "bug", "validation"]
    
    - agent: "ui_designer"
      specializations: ["design", "user_experience", "prototyping"]
      handoff_targets: ["product_manager", "developer"]
      participation_weight: 0.9
      max_consecutive_turns: 4
      priority_keywords: ["design", "ui", "ux", "user"]

  termination:
    type: "consensus"
    consensus_threshold: 0.8
    required_agents: ["product_manager", "tech_lead"]
    max_messages: 50
    timeout: 3600  # 1 hour

  handoff_config:
    autonomous_threshold: 0.6
    keyword_boost: 0.3
    specialization_boost: 0.4
    recent_activity_penalty: 0.2
    load_balancing: true
```

## Participant Configuration

### Agent Specializations
Define what each agent excels at:

```yaml
participants:
  - agent: "research_specialist"
    specializations: 
      - "academic_research"
      - "literature_review" 
      - "citation_analysis"
      - "methodology_design"
```

### Handoff Targets
Specify preferred handoff partners:

```yaml
participants:
  - agent: "frontend_dev"
    handoff_targets: ["backend_dev", "ui_designer", "qa_engineer"]
    handoff_preferences:
      "backend_dev": 0.7    # High preference for API work
      "ui_designer": 0.5    # Medium preference for design work
      "qa_engineer": 0.3    # Lower preference for testing
```

### Participation Weights
Control agent selection probability:

```yaml
participants:
  - agent: "senior_architect"
    participation_weight: 2.0    # 2x more likely to be selected
  - agent: "junior_developer"
    participation_weight: 0.5    # 0.5x less likely to be selected
```

### Turn Limits
Prevent any single agent from dominating:

```yaml
participants:
  - agent: "creative_writer"
    max_consecutive_turns: 3     # Hand off after 3 consecutive messages
    cooldown_period: 2           # Wait 2 turns before re-entering
```

## Termination Conditions

### Message-Based Termination
```yaml
termination:
  type: "max_messages"
  value: 30
  per_agent_limit: 10          # Max 10 messages per agent
```

### Consensus-Based Termination
```yaml
termination:
  type: "consensus"
  consensus_threshold: 0.75     # 75% agreement required
  required_agents: ["lead", "manager"]  # These agents must agree
  consensus_keywords: ["approved", "ready", "complete"]
```

### Time-Based Termination
```yaml
termination:
  type: "timeout"
  value: 1800                   # 30 minutes in seconds
  soft_timeout: 1200           # Warning at 20 minutes
```

### Task Completion Detection
```yaml
termination:
  type: "task_completion"
  completion_indicators:
    - "task completed"
    - "deliverable ready"
    - "requirements met"
  validation_agent: "project_manager"
```

## CLI Commands

### Create Swarm
```bash
# Basic swarm creation
agentmesh swarm create --config research-swarm.yaml

# With agent mapping
agentmesh swarm create --config swarm.yaml --agent-mapping '{"analyst": "agent-456"}'
```

### Monitor Swarm
```bash
# Monitor all metrics
agentmesh swarm monitor --id swarm-123

# Monitor specific metrics
agentmesh swarm monitor --id swarm-123 --metrics participation

# Monitor with custom refresh rate
agentmesh swarm monitor --id swarm-123 --refresh 3
```

### Tune Parameters
```bash
# Adjust participation balance
agentmesh swarm tune --id swarm-123 --parameter participation_balance --value 0.8

# Modify handoff frequency  
agentmesh swarm tune --id swarm-123 --parameter handoff_frequency --value 0.6

# Update convergence threshold
agentmesh swarm tune --id swarm-123 --parameter convergence_threshold --value 0.9

# Get current parameter value
agentmesh swarm tune --id swarm-123 --parameter participation_balance
```

### Analytics
```bash
# Console analytics
agentmesh swarm analytics --id swarm-123

# JSON output for processing
agentmesh swarm analytics --id swarm-123 --output json

# CSV export for analysis
agentmesh swarm analytics --id swarm-123 --output csv > swarm_metrics.csv
```

## API Endpoints

### Get Swarm Metrics
```http
GET /api/v1/workflows/{execution_id}/swarm/metrics

Response:
{
  "execution_id": "swarm-123",
  "agent_participation_rates": {
    "data_collector": 0.25,
    "analyst": 0.35,
    "statistician": 0.20,
    "report_generator": 0.20
  },
  "total_handoffs": 12,
  "autonomous_handoffs": 8,
  "avg_response_time": 2.3,
  "total_messages": 18,
  "active_agents": ["analyst", "statistician"],
  "convergence_score": 0.73
}
```

### Get Swarm Analytics
```http
GET /api/v1/workflows/{execution_id}/swarm/analytics

Response:
{
  "execution_id": "swarm-123",
  "performance_metrics": {
    "total_messages": 18,
    "total_handoffs": 12,
    "autonomous_handoffs": 8,
    "avg_response_time": 2.3,
    "convergence_score": 0.73
  },
  "handoff_patterns": {
    "direct_handoffs": {
      "data_collector": {"analyst": 3, "statistician": 1},
      "analyst": {"statistician": 2, "report_generator": 3}
    }
  },
  "agent_statistics": {
    "participation_rates": {...},
    "active_agents": [...],
    "agent_count": 4
  },
  "efficiency_scores": {
    "messages_per_handoff": 1.5,
    "participation_balance": 0.85
  }
}
```

### Tune Parameters
```http
POST /api/v1/workflows/{execution_id}/swarm/tune
Content-Type: application/json

{
  "parameter": "participation_balance",
  "value": 0.8
}

Response:
{
  "success": true,
  "parameter": "participation_balance",
  "new_value": 0.8,
  "execution_id": "swarm-123"
}
```

### Get Handoff Graph
```http
GET /api/v1/workflows/{execution_id}/swarm/handoff-graph

Response:
{
  "execution_id": "swarm-123",
  "nodes": {
    "data_collector": {
      "id": "data_collector",
      "name": "Data Collector",
      "specializations": ["data_collection", "web_scraping"],
      "participation_rate": 0.25,
      "is_active": false
    }
  },
  "edges": {
    "edge_1": {
      "id": "edge_1",
      "source": "data_collector",
      "target": "analyst",
      "weight": 3,
      "type": "handoff"
    }
  },
  "metadata": {
    "total_participants": 4,
    "total_handoffs": 12,
    "last_updated": "2025-08-14T10:30:00Z"
  }
}
```

## Monitoring and Analytics

### Real-Time Metrics

**Participation Rates**: How often each agent contributes
```
Agent Participation:
  data_collector: 25.0%
  analyst: 35.0%  
  statistician: 20.0%
  report_generator: 20.0%
```

**Handoff Statistics**: Collaboration patterns
```
Handoff Statistics:
  Total Handoffs: 12
  Autonomous Handoffs: 8 (67%)
  Average Response Time: 2.3s
```

**Performance Indicators**: System efficiency
```
Performance:
  Messages Processed: 18
  Active Agents: 2
  Convergence Score: 0.73
```

### Analytics Dashboard

Key performance indicators for swarm optimization:

1. **Efficiency Metrics**
   - Messages per handoff ratio
   - Participation balance score
   - Response time trends
   - Task completion rate

2. **Collaboration Patterns**
   - Handoff frequency matrix
   - Agent interaction network
   - Specialization utilization
   - Load distribution

3. **Quality Indicators**
   - Consensus achievement rate
   - Task completion accuracy
   - Error and retry rates
   - User satisfaction scores

## Best Practices

### 1. Agent Design
- **Clear Specializations**: Define distinct areas of expertise
- **Complementary Skills**: Ensure agents have overlapping capabilities
- **Balanced Participation**: Avoid single points of failure
- **Appropriate Turn Limits**: Prevent monopolization

### 2. Configuration Optimization
- **Start Small**: Begin with 3-4 agents, scale up gradually
- **Monitor Metrics**: Track participation and handoff patterns
- **Tune Parameters**: Adjust based on observed behavior
- **Set Appropriate Limits**: Balance autonomy with control

### 3. Termination Strategy
- **Multiple Conditions**: Use fallback termination conditions
- **Reasonable Timeouts**: Prevent infinite loops
- **Quality Gates**: Ensure task completion validation
- **Graceful Degradation**: Handle edge cases smoothly

### 4. Performance Tuning

#### Participation Balance
```bash
# Increase balance (more equal participation)
agentmesh swarm tune --id swarm-123 --parameter participation_balance --value 0.9

# Decrease balance (allow specialization)
agentmesh swarm tune --id swarm-123 --parameter participation_balance --value 0.6
```

#### Handoff Frequency
```bash
# Increase handoffs (more collaboration)
agentmesh swarm tune --id swarm-123 --parameter handoff_frequency --value 0.8

# Decrease handoffs (longer agent turns)
agentmesh swarm tune --id swarm-123 --parameter handoff_frequency --value 0.4
```

## Common Patterns

### Research and Analysis
```yaml
# Agents: researcher → analyst → validator → reporter
participants:
  - agent: "researcher"
    specializations: ["research", "data_gathering"]
    handoff_targets: ["analyst"]
  - agent: "analyst" 
    specializations: ["analysis", "insights"]
    handoff_targets: ["validator", "reporter"]
  - agent: "validator"
    specializations: ["validation", "quality_check"]
    handoff_targets: ["analyst", "reporter"]
  - agent: "reporter"
    specializations: ["writing", "presentation"]
    handoff_targets: ["validator"]
```

### Code Development
```yaml
# Agents: architect → developer → reviewer → tester
participants:
  - agent: "architect"
    specializations: ["design", "architecture"]
    handoff_targets: ["developer"]
  - agent: "developer"
    specializations: ["coding", "implementation"]
    handoff_targets: ["reviewer", "tester"]
  - agent: "reviewer"
    specializations: ["code_review", "best_practices"]
    handoff_targets: ["developer", "tester"]
  - agent: "tester"
    specializations: ["testing", "quality_assurance"]
    handoff_targets: ["developer", "reviewer"]
```

### Content Creation
```yaml
# Agents: strategist → writer → editor → designer
participants:
  - agent: "strategist"
    specializations: ["strategy", "planning"]
    handoff_targets: ["writer", "designer"]
  - agent: "writer"
    specializations: ["writing", "content_creation"]
    handoff_targets: ["editor"]
  - agent: "editor"
    specializations: ["editing", "proofreading"]
    handoff_targets: ["writer", "designer"]
  - agent: "designer"
    specializations: ["design", "layout"]
    handoff_targets: ["editor"]
```

## Troubleshooting

### Common Issues

1. **Infinite Loops**
   - **Symptoms**: Agents continuously hand off without progress
   - **Solution**: Implement max consecutive turns and cooldown periods
   - **Prevention**: Clear termination conditions and task completion detection

2. **Agent Monopolization**
   - **Symptoms**: One agent dominates all interactions
   - **Solution**: Adjust participation weights and turn limits
   - **Prevention**: Monitor participation rates and tune balance

3. **Poor Handoff Decisions**
   - **Symptoms**: Inappropriate agent selection for tasks
   - **Solution**: Refine specializations and handoff targets
   - **Prevention**: Use keyword-based routing and priority systems

4. **Slow Convergence**
   - **Symptoms**: Swarm takes too long to complete tasks
   - **Solution**: Increase handoff frequency and adjust thresholds
   - **Prevention**: Set appropriate timeouts and fallback mechanisms

### Debug Commands

```bash
# Monitor real-time behavior
agentmesh swarm monitor --id swarm-123 --metrics all --refresh 1

# Analyze handoff patterns
agentmesh swarm analytics --id swarm-123 --output json | jq '.handoff_patterns'

# Check participation balance
agentmesh swarm analytics --id swarm-123 --output json | jq '.efficiency_scores.participation_balance'

# Tune problematic parameters
agentmesh swarm tune --id swarm-123 --parameter handoff_frequency --value 0.7
```

## Examples

### Basic Research Swarm
See `examples/workflows/swarm-research-analysis.yaml` for a complete research analysis swarm with data collection, analysis, and reporting agents.

### Advanced Product Development Swarm
See `examples/workflows/swarm-product-development.yaml` for a comprehensive product development swarm with multiple specialized roles and complex handoff patterns.

### Content Creation Swarm
See `examples/workflows/swarm-content-creation.yaml` for a content creation pipeline with strategy, writing, editing, and design agents.

Each example demonstrates different aspects of swarm coordination and can be used as templates for your own swarm implementations.
