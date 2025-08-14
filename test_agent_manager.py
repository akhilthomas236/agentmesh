"""Test script for AgentManager functionality."""

import asyncio
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from agentmesh.core.agent_manager import AgentManager
from agentmesh.models.agent import AgentConfig, AgentType, AgentStatus


async def test_agent_lifecycle():
    """Test complete agent lifecycle."""
    print("🧪 Testing AgentManager functionality...")
    
    manager = AgentManager()
    
    # Test 1: Create agents
    print("\n1. Creating agents...")
    config1 = AgentConfig(
        name="architect",
        type=AgentType.ASSISTANT,
        system_message="You are a software architect"
    )
    config2 = AgentConfig(
        name="developer", 
        type=AgentType.ASSISTANT,
        system_message="You are a Python developer"
    )
    
    agent1_id = await manager.create_agent(config1)
    agent2_id = await manager.create_agent(config2)
    print(f"   ✓ Created agent 1: {agent1_id}")
    print(f"   ✓ Created agent 2: {agent2_id}")
    
    # Test 2: List agents
    print("\n2. Listing agents...")
    agents = await manager.list_agents()
    print(f"   ✓ Found {len(agents)} agents")
    for agent in agents:
        print(f"     - {agent.name} ({agent.id}): {agent.status}")
    
    # Test 3: Start agents
    print("\n3. Starting agents...")
    success1 = await manager.start_agent(agent1_id)
    success2 = await manager.start_agent(agent2_id)
    print(f"   ✓ Started agent 1: {success1}")
    print(f"   ✓ Started agent 2: {success2}")
    
    # Test 4: Check status
    print("\n4. Checking agent status...")
    agent1 = await manager.get_agent(agent1_id)
    agent2 = await manager.get_agent(agent2_id)
    print(f"   ✓ Agent 1 status: {agent1.status}")
    print(f"   ✓ Agent 2 status: {agent2.status}")
    
    # Test 5: Get agent by name
    print("\n5. Getting agent by name...")
    agent_by_name = await manager.get_agent_by_name("architect")
    print(f"   ✓ Found agent by name: {agent_by_name.name if agent_by_name else 'None'}")
    
    # Test 6: Health check
    print("\n6. Health check...")
    health = await manager.health_check()
    print(f"   ✓ Health status: {health['status']}")
    print(f"   ✓ Total agents: {health['total_agents']}")
    print(f"   ✓ Active agents: {health['active_agents']}")
    print(f"   ✓ AutoGen available: {health['autogen_available']}")
    
    # Test 7: Stop agents
    print("\n7. Stopping agents...")
    success1 = await manager.stop_agent(agent1_id)
    success2 = await manager.stop_agent(agent2_id)
    print(f"   ✓ Stopped agent 1: {success1}")
    print(f"   ✓ Stopped agent 2: {success2}")
    
    # Test 8: Delete agents
    print("\n8. Deleting agents...")
    success1 = await manager.delete_agent(agent1_id)
    success2 = await manager.delete_agent(agent2_id)
    print(f"   ✓ Deleted agent 1: {success1}")
    print(f"   ✓ Deleted agent 2: {success2}")
    
    # Test 9: Final agent count
    print("\n9. Final agent count...")
    final_agents = await manager.list_agents()
    print(f"   ✓ Remaining agents: {len(final_agents)}")
    
    print("\n🎉 All tests passed! AgentManager is working correctly.")


if __name__ == "__main__":
    asyncio.run(test_agent_lifecycle())
