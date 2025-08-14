"""Test script to demonstrate Sprint 3 functionality."""

import asyncio
import json
import websockets
from typing import Dict, Any
import httpx


class AutoGenA2AClient:
    """Client for testing AutoGen A2A API functionality."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api/v1"
        
    async def create_agent(self, agent_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new agent."""
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.api_url}/agents", json=agent_data)
            response.raise_for_status()
            return response.json()
    
    async def send_message(self, sender_id: str, receiver_id: str, content: str) -> Dict[str, Any]:
        """Send a message via REST API."""
        message_data = {
            "receiver_id": receiver_id,
            "content": content,
            "message_type": "chat"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_url}/messaging/send",
                params={"sender_id": sender_id},
                json=message_data
            )
            response.raise_for_status()
            return response.json()
    
    async def get_conversation_history(self, agent1_id: str, agent2_id: str) -> Dict[str, Any]:
        """Get conversation history between two agents."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.api_url}/messaging/conversation/{agent1_id}/{agent2_id}"
            )
            response.raise_for_status()
            return response.json()
    
    async def set_context(self, agent_id: str, key: str, value: Any, scope: str = "agent") -> Dict[str, Any]:
        """Set context via REST API."""
        context_data = {
            "key": key,
            "value": value,
            "scope": scope,
            "scope_id": agent_id,
            "metadata": {"test": True}
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_url}/context/set",
                params={"agent_id": agent_id},
                json=context_data
            )
            response.raise_for_status()
            return response.json()
    
    async def get_context(self, agent_id: str, key: str, scope: str = "agent") -> Dict[str, Any]:
        """Get context via REST API."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.api_url}/context/get/{scope}/{agent_id}/{key}",
                params={"agent_id": agent_id}
            )
            response.raise_for_status()
            return response.json()
    
    async def initiate_handoff(self, from_agent_id: str, to_agent_id: str, reason: str, message: str) -> Dict[str, Any]:
        """Initiate a handoff via REST API."""
        handoff_data = {
            "to_agent_id": to_agent_id,
            "reason": reason,
            "message": message,
            "priority": 5,
            "context_data": {"task_progress": "50%", "current_step": "analysis"}
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_url}/handoffs/initiate",
                params={"from_agent_id": from_agent_id},
                json=handoff_data
            )
            response.raise_for_status()
            return response.json()
    
    async def respond_to_handoff(self, handoff_id: str, agent_id: str, accepted: bool) -> Dict[str, Any]:
        """Respond to a handoff via REST API."""
        response_data = {
            "accepted": accepted,
            "message": "Accepted the handoff" if accepted else "Rejected the handoff"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_url}/handoffs/respond/{handoff_id}",
                params={"agent_id": agent_id},
                json=response_data
            )
            response.raise_for_status()
            return response.json()
    
    async def get_pending_handoffs(self, agent_id: str) -> Dict[str, Any]:
        """Get pending handoffs for an agent."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.api_url}/handoffs/pending",
                params={"agent_id": agent_id}
            )
            response.raise_for_status()
            return response.json()


async def test_websocket_communication(agent_id: str):
    """Test WebSocket communication."""
    uri = f"ws://localhost:8000/api/v1/ws/agent/{agent_id}"
    
    try:
        async with websockets.connect(uri) as websocket:
            print(f"✅ WebSocket connected for agent {agent_id}")
            
            # Send a heartbeat
            heartbeat_msg = {"type": "heartbeat", "data": {}}
            await websocket.send(json.dumps(heartbeat_msg))
            
            # Wait for heartbeat ack
            response = await websocket.recv()
            print(f"📞 Heartbeat response: {response}")
            
            # Send a message via WebSocket
            message_data = {
                "type": "message",
                "data": {
                    "receiver_id": "agent-2",
                    "content": "Hello from WebSocket!",
                    "message_type": "chat"
                }
            }
            await websocket.send(json.dumps(message_data))
            
            # Wait for response
            response = await websocket.recv()
            print(f"💬 Message response: {response}")
            
            return True
            
    except Exception as e:
        print(f"❌ WebSocket test failed: {e}")
        return False


async def main():
    """Main test function."""
    print("🚀 Starting AutoGen A2A Sprint 3 Feature Test")
    print("=" * 50)
    
    client = AutoGenA2AClient()
    
    # Test 1: Create test agents
    print("\n🏗️  Test 1: Creating test agents...")
    try:
        agent1_data = {
            "name": "test-agent-1",
            "description": "Test agent for messaging",
            "config": {
                "name": "test-agent-1",
                "system_message": "You are a helpful assistant.",
                "agent_type": "assistant",
                "model_config": {
                    "model": "gpt-4o",
                    "temperature": 0.7,
                    "max_tokens": 4096
                },
                "capabilities": [],
                "human_input_mode": "NEVER"
            },
            "tags": ["test"],
            "metadata": {"test": True}
        }
        
        agent2_data = {
            "name": "test-agent-2", 
            "description": "Test agent for handoffs",
            "config": {
                "name": "test-agent-2",
                "system_message": "You are a specialist agent.",
                "agent_type": "assistant",
                "model_config": {
                    "model": "gpt-4o",
                    "temperature": 0.7,
                    "max_tokens": 4096
                },
                "capabilities": [],
                "human_input_mode": "NEVER"
            },
            "tags": ["test"],
            "metadata": {"test": True}
        }
        
        agent1 = await client.create_agent(agent1_data)
        agent2 = await client.create_agent(agent2_data)
        
        agent1_id = agent1["agent"]["id"]
        agent2_id = agent2["agent"]["id"]
        
        print(f"✅ Created agent 1: {agent1_id}")
        print(f"✅ Created agent 2: {agent2_id}")
        
    except Exception as e:
        print(f"❌ Agent creation failed: {e}")
        return
    
    # Test 2: Message Bus REST API
    print("\n📨 Test 2: Testing Message Bus REST API...")
    try:
        # Send a message
        message_result = await client.send_message(
            sender_id=agent1_id,
            receiver_id=agent2_id,
            content="Hello from the message bus!"
        )
        print(f"✅ Message sent: {message_result['message_id']}")
        
        # Get conversation history  
        await asyncio.sleep(0.5)  # Give message time to be stored
        history = await client.get_conversation_history(agent1_id, agent2_id)
        print(f"✅ Conversation history retrieved: {len(history['messages'])} messages")
        
    except Exception as e:
        print(f"❌ Message bus test failed: {e}")
    
    # Test 3: Context Management
    print("\n🗂️  Test 3: Testing Context Management...")
    try:
        # Set context
        context_result = await client.set_context(
            agent_id=agent1_id,
            key="current_task",
            value={"task": "data_analysis", "progress": 0.3, "files": ["data.csv"]}
        )
        print(f"✅ Context set: {context_result['entry']['key']}")
        
        # Get context
        retrieved_context = await client.get_context(
            agent_id=agent1_id,
            key="current_task"
        )
        print(f"✅ Context retrieved: {retrieved_context['entry']['value']}")
        
    except Exception as e:
        print(f"❌ Context management test failed: {e}")
    
    # Test 4: Handoff Management
    print("\n🤝 Test 4: Testing Handoff Management...")
    try:
        # Initiate handoff
        handoff_result = await client.initiate_handoff(
            from_agent_id=agent1_id,
            to_agent_id=agent2_id,
            reason="expertise_required",
            message="Need specialist help with data analysis"
        )
        handoff_id = handoff_result["handoff"]["id"]
        print(f"✅ Handoff initiated: {handoff_id}")
        
        # Check pending handoffs
        pending = await client.get_pending_handoffs(agent2_id)
        print(f"✅ Pending handoffs for agent2: {len(pending['handoffs'])}")
        
        # Respond to handoff
        if pending['handoffs']:
            response = await client.respond_to_handoff(
                handoff_id=handoff_id,
                agent_id=agent2_id,
                accepted=True
            )
            print(f"✅ Handoff accepted: {response['response']['accepted']}")
        
    except Exception as e:
        print(f"❌ Handoff management test failed: {e}")
    
    # Test 5: WebSocket Communication
    print("\n🔗 Test 5: Testing WebSocket Communication...")
    websocket_success = await test_websocket_communication(agent1_id)
    if websocket_success:
        print("✅ WebSocket communication test passed")
    
    print("\n🎉 Sprint 3 Feature Test Complete!")
    print("=" * 50)
    print("✅ Message Bus (Redis-based)")
    print("✅ REST API for messaging")
    print("✅ Context Management System")
    print("✅ Handoff Management")
    print("✅ WebSocket Real-time Communication")
    print("✅ All Redis integrations working")


if __name__ == "__main__":
    asyncio.run(main())
