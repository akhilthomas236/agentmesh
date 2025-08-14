#!/usr/bin/env python3
"""Test script for registering test agents and testing handoff functionality."""

import asyncio
import json
import sys
from typing import List, Dict, Any

import httpx


BASE_URL = "http://localhost:8889"


async def register_test_agents() -> Dict[str, str]:
    """Register test agents in the system or use existing ones."""
    print("🤖 Checking for existing test agents...")
    
    registered_agents = {}
    async with httpx.AsyncClient() as client:
        # First check if agents already exist
        try:
            response = await client.get(f"{BASE_URL}/api/v1/agents")
            if response.status_code == 200:
                agents_data = response.json()
                for agent in agents_data.get("agents", []):
                    if agent["name"] in ["assistant_alice", "assistant_bob", "user_proxy_charlie"]:
                        registered_agents[agent["name"]] = agent["id"]
                        print(f"✅ Found existing agent: {agent['name']} (ID: {agent['id']})")
        except Exception as e:
            print(f"❌ Error checking existing agents: {e}")
    
    # Only register missing agents
    agents_config = [
        {
            "name": "assistant_alice",
            "description": "A helpful assistant agent for testing",
            "config": {
                "name": "assistant_alice",
                "system_message": "You are Alice, a helpful assistant agent for testing handoffs.",
                "agent_type": "assistant",
                "model_config": {
                    "model": "gpt-3.5-turbo",
                    "max_tokens": 1000,
                    "temperature": 0.7
                },
                "capabilities": ["function_calling"],
                "extra_config": {}
            },
            "tags": ["test", "assistant"],
            "metadata": {"purpose": "testing"}
        },
        {
            "name": "assistant_bob",
            "description": "Another assistant agent for testing",
            "config": {
                "name": "assistant_bob",
                "system_message": "You are Bob, a helpful assistant agent specialized in handoff testing.",
                "agent_type": "assistant",
                "model_config": {
                    "model": "gpt-3.5-turbo",
                    "max_tokens": 1000,
                    "temperature": 0.5
                },
                "capabilities": ["function_calling"],
                "extra_config": {}
            },
            "tags": ["test", "assistant"],
            "metadata": {"purpose": "testing"}
        },
        {
            "name": "user_proxy_charlie",
            "description": "A user proxy agent for testing",
            "config": {
                "name": "user_proxy_charlie",
                "system_message": "You are Charlie, a user proxy agent for testing handoffs.",
                "agent_type": "user_proxy",
                "model_config": {
                    "model": "gpt-3.5-turbo",
                    "max_tokens": 1000,
                    "temperature": 0.3
                },
                "capabilities": ["termination"],
                "extra_config": {}
            },
            "tags": ["test", "proxy"],
            "metadata": {"purpose": "testing"}
        }
    ]
    
    async with httpx.AsyncClient() as client:
        for agent_config in agents_config:
            agent_name = agent_config["name"]
            if agent_name not in registered_agents:
                try:
                    response = await client.post(
                        f"{BASE_URL}/api/v1/agents",
                        json=agent_config,
                        timeout=30.0
                    )
                    
                    if response.status_code == 201:
                        agent_data = response.json()
                        agent_id = agent_data["agent"]["id"]
                        registered_agents[agent_name] = agent_id
                        print(f"✅ Registered new agent: {agent_name} (ID: {agent_id})")
                    else:
                        print(f"❌ Failed to register agent {agent_name}: {response.status_code}")
                        print(f"   Response: {response.text}")
                        
                except Exception as e:
                    print(f"❌ Error registering agent {agent_name}: {e}")
    
    return registered_agents


async def test_handoff_endpoints(agents: Dict[str, str]) -> None:
    """Test handoff manager endpoints with registered agents."""
    print("\n🔄 Testing handoff endpoints...")
    
    if not agents:
        print("❌ No agents registered, skipping handoff tests")
        return
    
    agent_names = list(agents.keys())
    agent_ids = list(agents.values())
    
    async with httpx.AsyncClient() as client:
        # Test 1: Get handoff reasons
        print("\n1️⃣ Testing handoff reasons...")
        try:
            response = await client.get(f"{BASE_URL}/api/v1/handoffs/reasons")
            if response.status_code == 200:
                reasons = response.json()
                print(f"✅ Handoff reasons: {reasons}")
            else:
                print(f"❌ Failed to get handoff reasons: {response.status_code}")
        except Exception as e:
            print(f"❌ Error getting handoff reasons: {e}")
        
        # Test 2: Get pending handoffs for first agent
        print("\n2️⃣ Testing pending handoffs...")
        try:
            first_agent = agent_names[0]
            response = await client.get(
                f"{BASE_URL}/api/v1/handoffs/pending",
                params={"agent_id": agents[first_agent]}
            )
            if response.status_code == 200:
                pending = response.json()
                print(f"✅ Pending handoffs for {first_agent}: {pending}")
            else:
                print(f"❌ Failed to get pending handoffs: {response.status_code}")
                print(f"   Response: {response.text}")
        except Exception as e:
            print(f"❌ Error getting pending handoffs: {e}")
        
        # Test 3: Get handoff history for first agent
        print("\n3️⃣ Testing handoff history...")
        try:
            first_agent = agent_names[0]
            response = await client.get(
                f"{BASE_URL}/api/v1/handoffs/history",
                params={"agent_id": agents[first_agent]}
            )
            if response.status_code == 200:
                history = response.json()
                print(f"✅ Handoff history for {first_agent}: {history}")
            else:
                print(f"❌ Failed to get handoff history: {response.status_code}")
                print(f"   Response: {response.text}")
        except Exception as e:
            print(f"❌ Error getting handoff history: {e}")
        
        # Test 4: Initiate a handoff (if we have at least 2 agents)
        if len(agents) >= 2:
            print("\n4️⃣ Testing handoff initiation...")
            try:
                from_agent = agent_names[0]
                to_agent = agent_names[1]
                
                handoff_request = {
                    "to_agent_id": agents[to_agent],
                    "reason": "expertise_required",
                    "message": "Handing off to specialist for testing purposes",
                    "conversation_id": "test-conversation-123",
                    "context_data": {
                        "message": "Testing handoff functionality",
                        "metadata": {"test": True}
                    },
                    "metadata": {"purpose": "testing"},
                    "priority": 1,
                    "expires_in_minutes": 30
                }
                
                response = await client.post(
                    f"{BASE_URL}/api/v1/handoffs/initiate",
                    params={"from_agent_id": agents[from_agent]},
                    json=handoff_request
                )
                
                if response.status_code == 200:
                    handoff_data = response.json()
                    handoff_id = handoff_data.get("handoff", {}).get("id")
                    print(f"✅ Initiated handoff from {from_agent} to {to_agent}")
                    print(f"   Handoff ID: {handoff_id}")
                    
                    # Test 5: Try to get pending handoffs to see if the handoff shows up
                    if handoff_id:
                        print("\n5️⃣ Testing pending handoffs after creation...")
                        try:
                            response = await client.get(
                                f"{BASE_URL}/api/v1/handoffs/pending",
                                params={"agent_id": agents[to_agent]}
                            )
                            if response.status_code == 200:
                                pending = response.json()
                                print(f"✅ Pending handoffs for {to_agent}: {pending}")
                            else:
                                print(f"❌ Failed to get pending handoffs: {response.status_code}")
                        except Exception as e:
                            print(f"❌ Error getting pending handoffs: {e}")
                        
                        # Test 6: Accept the handoff
                        print("\n6️⃣ Testing handoff acceptance...")
                        try:
                            accept_request = {
                                "accepted": True,
                                "message": "Accepting handoff for testing"
                            }
                            response = await client.post(
                                f"{BASE_URL}/api/v1/handoffs/respond/{handoff_id}",
                                params={"agent_id": agents[to_agent]},
                                json=accept_request
                            )
                            if response.status_code == 200:
                                print(f"✅ Handoff accepted successfully")
                            else:
                                print(f"❌ Failed to accept handoff: {response.status_code}")
                                print(f"   Response: {response.text}")
                        except Exception as e:
                            print(f"❌ Error accepting handoff: {e}")
                        
                        # Test 7: Get audit trail
                        print("\n7️⃣ Testing audit trail...")
                        try:
                            response = await client.get(
                                f"{BASE_URL}/api/v1/handoffs/audit/{handoff_id}",
                                params={"agent_id": agents[from_agent]}
                            )
                            if response.status_code == 200:
                                audit = response.json()
                                print(f"✅ Audit trail: {json.dumps(audit, indent=2)}")
                            else:
                                print(f"❌ Failed to get audit trail: {response.status_code}")
                        except Exception as e:
                            print(f"❌ Error getting audit trail: {e}")
                
                else:
                    print(f"❌ Failed to initiate handoff: {response.status_code}")
                    print(f"   Response: {response.text}")
                    
            except Exception as e:
                print(f"❌ Error initiating handoff: {e}")
        
        # Test 8: Test cancellation of a new handoff
        # Test 8: Test cancellation of a new handoff
        if len(agents) >= 2:
            print("\n8️⃣ Testing handoff cancellation...")
            try:
                from_agent = agent_names[0]
                to_agent = agent_names[1]
                
                # Create another handoff to cancel
                handoff_request = {
                    "to_agent_id": agents[to_agent],
                    "reason": "manual",
                    "message": "Another handoff for cancellation testing",
                    "conversation_id": "test-conversation-456",
                    "priority": 0,
                    "expires_in_minutes": 60
                }
                
                response = await client.post(
                    f"{BASE_URL}/api/v1/handoffs/initiate",
                    params={"from_agent_id": agents[from_agent]},
                    json=handoff_request
                )
                
                if response.status_code == 200:
                    handoff_data = response.json()
                    cancel_handoff_id = handoff_data.get("handoff", {}).get("id")
                    print(f"✅ Created handoff for cancellation: {cancel_handoff_id}")
                    
                    # Now cancel it
                    if cancel_handoff_id:
                        response = await client.post(
                            f"{BASE_URL}/api/v1/handoffs/cancel/{cancel_handoff_id}",
                            params={
                                "agent_id": agents[from_agent],
                                "reason": "Testing cancellation functionality"
                            }
                        )
                        
                        if response.status_code == 200:
                            cancel_data = response.json()
                            print(f"✅ Handoff cancelled: {cancel_data}")
                        else:
                            print(f"❌ Failed to cancel handoff: {response.status_code}")
                            print(f"   Response: {response.text}")
                else:
                    print(f"❌ Failed to create handoff for cancellation: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Error testing cancellation: {e}")
        
        # Test 9: List all agents to verify they're registered
        print("\n9️⃣ Listing all registered agents...")
        try:
            response = await client.get(f"{BASE_URL}/api/v1/agents")
            if response.status_code == 200:
                agents_list = response.json()
                print(f"✅ Total agents: {agents_list.get('total', 0)}")
                for agent in agents_list.get('agents', []):
                    print(f"   - {agent['name']} (ID: {agent['id']}, Status: {agent['status']})")
            else:
                print(f"❌ Failed to list agents: {response.status_code}")
        except Exception as e:
            print(f"❌ Error listing agents: {e}")


async def cleanup_test_agents(agents: Dict[str, str]) -> None:
    """Clean up test agents."""
    print("\n🧹 Cleaning up test agents...")
    
    async with httpx.AsyncClient() as client:
        for agent_name, agent_id in agents.items():
            try:
                response = await client.delete(f"{BASE_URL}/api/v1/agents/{agent_id}")
                if response.status_code in [200, 204, 404]:
                    print(f"✅ Cleaned up agent: {agent_name}")
                else:
                    print(f"❌ Failed to clean up agent {agent_name}: {response.status_code}")
            except Exception as e:
                print(f"❌ Error cleaning up agent {agent_name}: {e}")


async def main():
    """Main test function."""
    print("🚀 Starting agent registration and handoff testing...")
    
    try:
        # Register test agents
        agents = await register_test_agents()
        
        if agents:
            # Test handoff endpoints
            await test_handoff_endpoints(agents)
            
            # Clean up (optional - comment out if you want to keep agents for further testing)
            cleanup = input("\n🤔 Clean up test agents? (y/N): ").strip().lower()
            if cleanup == 'y':
                await cleanup_test_agents(agents)
            else:
                print("📝 Test agents left in system for further testing.")
                print("   Agent IDs:")
                for name, agent_id in agents.items():
                    print(f"   - {name}: {agent_id}")
        else:
            print("❌ No agents were registered successfully")
            
    except KeyboardInterrupt:
        print("\n⛔ Testing interrupted by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
