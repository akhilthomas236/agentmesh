"""Test the core AgentManager functionality."""

import pytest
import asyncio
from datetime import datetime

from agentmesh.core.agent_manager import AgentManager
from agentmesh.models.agent import AgentConfig, AgentType, AgentStatus


class TestAgentManager:
    """Test cases for AgentManager."""

    @pytest.fixture
    def agent_manager(self):
        """Create a fresh AgentManager instance for each test."""
        return AgentManager()

    @pytest.fixture
    def sample_config(self):
        """Create a sample agent configuration."""
        return AgentConfig(
            name="test-agent",
            type=AgentType.ASSISTANT,
            system_message="You are a test agent",
        )

    @pytest.mark.asyncio
    async def test_create_agent(self, agent_manager, sample_config):
        """Test agent creation."""
        agent_id = await agent_manager.create_agent(sample_config)

        assert agent_id is not None
        assert agent_id.startswith("agent-")

        # Verify agent was created
        agents = await agent_manager.list_agents()
        assert len(agents) == 1
        assert agents[0].name == sample_config.name
        assert agents[0].type == sample_config.type

    @pytest.mark.asyncio
    async def test_duplicate_agent_name(self, agent_manager, sample_config):
        """Test that duplicate agent names are rejected."""
        await agent_manager.create_agent(sample_config)

        # Try to create another agent with the same name
        with pytest.raises(ValueError, match="Agent with name .* already exists"):
            await agent_manager.create_agent(sample_config)

    @pytest.mark.asyncio
    async def test_agent_lifecycle(self, agent_manager, sample_config):
        """Test complete agent lifecycle."""
        # Create agent
        agent_id = await agent_manager.create_agent(sample_config)
        agent = await agent_manager.get_agent(agent_id)
        assert agent.status == AgentStatus.CREATED

        # Start agent
        success = await agent_manager.start_agent(agent_id)
        assert success is True

        agent = await agent_manager.get_agent(agent_id)
        assert agent.status == AgentStatus.ACTIVE
        assert agent.last_active is not None

        # Stop agent
        success = await agent_manager.stop_agent(agent_id)
        assert success is True

        agent = await agent_manager.get_agent(agent_id)
        assert agent.status == AgentStatus.STOPPED

        # Delete agent
        success = await agent_manager.delete_agent(agent_id)
        assert success is True

        # Verify agent is gone
        agents = await agent_manager.list_agents()
        assert len(agents) == 0

    @pytest.mark.asyncio
    async def test_get_agent_by_name(self, agent_manager, sample_config):
        """Test getting agent by name."""
        agent_id = await agent_manager.create_agent(sample_config)

        agent = await agent_manager.get_agent_by_name(sample_config.name)
        assert agent is not None
        assert agent.id == agent_id
        assert agent.name == sample_config.name

        # Test non-existent agent
        agent = await agent_manager.get_agent_by_name("non-existent")
        assert agent is None

    @pytest.mark.asyncio
    async def test_list_agents_with_status_filter(self, agent_manager):
        """Test listing agents with status filter."""
        # Create multiple agents
        config1 = AgentConfig(name="agent1", type=AgentType.ASSISTANT)
        config2 = AgentConfig(name="agent2", type=AgentType.ASSISTANT)

        agent1_id = await agent_manager.create_agent(config1)
        agent2_id = await agent_manager.create_agent(config2)

        # Start one agent
        await agent_manager.start_agent(agent1_id)

        # Test filtering
        all_agents = await agent_manager.list_agents()
        assert len(all_agents) == 2

        active_agents = await agent_manager.list_agents(status=AgentStatus.ACTIVE)
        assert len(active_agents) == 1
        assert active_agents[0].id == agent1_id

        created_agents = await agent_manager.list_agents(status=AgentStatus.CREATED)
        assert len(created_agents) == 1
        assert created_agents[0].id == agent2_id

    @pytest.mark.asyncio
    async def test_agent_not_found_errors(self, agent_manager):
        """Test error handling for non-existent agents."""
        non_existent_id = "agent-nonexistent"

        with pytest.raises(ValueError, match="Agent .* not found"):
            await agent_manager.get_agent(non_existent_id)

        with pytest.raises(ValueError, match="Agent .* not found"):
            await agent_manager.start_agent(non_existent_id)

        with pytest.raises(ValueError, match="Agent .* not found"):
            await agent_manager.stop_agent(non_existent_id)

        with pytest.raises(ValueError, match="Agent .* not found"):
            await agent_manager.delete_agent(non_existent_id)

    @pytest.mark.asyncio
    async def test_health_check(self, agent_manager):
        """Test health check functionality."""
        health = await agent_manager.health_check()

        assert "status" in health
        assert "total_agents" in health
        assert "active_agents" in health
        assert "error_agents" in health
        assert "autogen_available" in health
        assert "timestamp" in health

        # Initially should be healthy with no agents
        assert health["status"] == "healthy"
        assert health["total_agents"] == 0
        assert health["active_agents"] == 0
        assert health["error_agents"] == 0

    @pytest.mark.asyncio
    async def test_agent_metrics(self, agent_manager, sample_config):
        """Test agent metrics functionality."""
        agent_id = await agent_manager.create_agent(sample_config)

        metrics = await agent_manager.get_agent_metrics(agent_id)
        assert metrics.agent_id == agent_id
        assert metrics.messages_processed == 0
        assert metrics.conversations_handled == 0
        assert metrics.success_rate == 1.0


def test_agent_config_validation():
    """Test agent configuration validation."""
    # Valid configuration
    config = AgentConfig(
        name="test",
        type=AgentType.ASSISTANT,
        temperature=0.5,
        max_tokens=1000,
    )
    assert config.name == "test"
    assert config.temperature == 0.5

    # Test default values
    assert config.model == "gpt-4o"
    assert config.config == {}


def test_imports():
    """Test that all necessary imports work."""
    from agentmesh.core import AgentManager
    from agentmesh.models import AgentConfig, AgentType, AgentStatus

    assert AgentManager is not None
    assert AgentConfig is not None
    assert AgentType is not None
    assert AgentStatus is not None
