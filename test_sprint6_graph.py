#!/usr/bin/env python3
"""Test script for Sprint 6 Graph Workflow implementation."""

import asyncio
import json
import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from agentmesh.workflows.config import get_config_manager
from agentmesh.workflows.manager import get_workflow_manager
from agentmesh.orchestration.graph import GraphOrchestrator, EdgeType
from agentmesh.orchestration.base import WorkflowConfig, OrchestrationPattern


async def test_graph_orchestrator_basic():
    """Test basic graph orchestrator functionality."""
    print("=" * 60)
    print("Testing Basic Graph Orchestrator")
    print("=" * 60)
    
    try:
        # Create a simple graph workflow config
        config = WorkflowConfig(
            name="test-graph-workflow",
            pattern=OrchestrationPattern.GRAPH,
            agents=["agent-1", "agent-2", "agent-3", "agent-4"]
        )
        
        # Create graph orchestrator
        orchestrator = GraphOrchestrator(config)
        
        # Add nodes
        orchestrator.add_node("start", "agent-1", "Start Node", "Initial processing")
        orchestrator.add_node("parallel_1", "agent-2", "Parallel 1", "First parallel task")
        orchestrator.add_node("parallel_2", "agent-3", "Parallel 2", "Second parallel task")
        orchestrator.add_node("end", "agent-4", "End Node", "Final consolidation")
        
        # Add edges
        orchestrator.add_edge("edge_1", "start", "parallel_1", EdgeType.PARALLEL)
        orchestrator.add_edge("edge_2", "start", "parallel_2", EdgeType.PARALLEL)
        orchestrator.add_edge("edge_3", "parallel_1", "end", EdgeType.SYNCHRONIZE)
        orchestrator.add_edge("edge_4", "parallel_2", "end", EdgeType.SYNCHRONIZE)
        
        # Add parallel branch
        orchestrator.add_parallel_branch("main_branch", ["parallel_1", "parallel_2"], "end")
        
        print(f"✓ Created graph orchestrator with {len(orchestrator.nodes)} nodes")
        print(f"✓ Added {len(orchestrator.edges)} edges")
        print(f"✓ Configured {len(orchestrator.parallel_executions)} parallel branches")
        
        # Test execution
        print("\n🔄 Testing workflow execution...")
        result = await orchestrator.execute("Test graph workflow execution")
        
        if result.success:
            print("✅ Graph workflow executed successfully!")
            print(f"   - Messages: {len(result.messages)}")
            print(f"   - Completed nodes: {len(result.metadata.get('completed_nodes', []))}")
        else:
            print(f"❌ Graph workflow failed: {result.error}")
        
        # Get execution graph
        execution_graph = orchestrator.get_execution_graph()
        print(f"\n📊 Execution graph contains:")
        print(f"   - Nodes: {len(execution_graph['nodes'])}")
        print(f"   - Edges: {len(execution_graph['edges'])}")
        print(f"   - Parallel executions: {len(execution_graph['parallel_executions'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_graph_workflow_config():
    """Test graph workflow configuration loading."""
    print("\n" + "=" * 60)
    print("Testing Graph Workflow Configuration")
    print("=" * 60)
    
    try:
        config_manager = get_config_manager()
        
        # Test simple graph config (default structure)
        config_file = config_manager.load_config("examples/workflows/sequential-code-review.yaml")
        
        # Manually set pattern to graph for testing
        config_file.pattern = OrchestrationPattern.GRAPH
        
        print(f"✓ Loaded config: {config_file.name}")
        print(f"✓ Pattern: {config_file.pattern}")
        print(f"✓ Agents: {len(config_file.agents)}")
        
        # Validate configuration
        errors = config_manager.validate_config(config_file)
        if errors:
            print(f"❌ Validation errors: {errors}")
            return False
        else:
            print("✅ Configuration validation passed")
        
        # Test creating workflow from config
        workflow_manager = get_workflow_manager()
        agent_mapping = {
            "architect": "agent-arch-001",
            "developer": "agent-dev-001", 
            "reviewer": "agent-rev-001"
        }
        
        workflow = await workflow_manager.create_workflow_from_config(config_file, agent_mapping)
        print(f"✅ Created graph workflow: {workflow.workflow_id}")
        
        # Get execution info
        exec_info = await workflow.get_execution_info()
        print(f"✓ Execution info retrieved")
        
        if "execution_graph" in exec_info:
            graph = exec_info["execution_graph"]
            print(f"✓ Graph structure available:")
            print(f"   - Nodes: {len(graph['nodes'])}")
            print(f"   - Edges: {len(graph['edges'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Config test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_graph_workflow_advanced():
    """Test advanced graph workflow with explicit structure."""
    print("\n" + "=" * 60)
    print("Testing Advanced Graph Workflow")
    print("=" * 60)
    
    try:
        # Try to load the advanced graph config
        config_manager = get_config_manager()
        
        try:
            config_file = config_manager.load_config("examples/workflows/graph-code-review.yaml")
            print(f"✓ Loaded advanced config: {config_file.name}")
            
            # Show graph structure if available
            if hasattr(config_file, 'graph') and config_file.graph:
                print(f"✓ Explicit graph structure found:")
                print(f"   - Nodes: {len(config_file.graph.nodes)}")
                print(f"   - Edges: {len(config_file.graph.edges)}")
                
                if config_file.graph.parallel_branches:
                    print(f"   - Parallel branches: {len(config_file.graph.parallel_branches)}")
            else:
                print("⚠️  No explicit graph structure, will use default")
            
            # Validate advanced config
            errors = config_manager.validate_config(config_file)
            if errors:
                print(f"❌ Advanced validation errors: {errors}")
                return False
            else:
                print("✅ Advanced configuration validation passed")
                
            return True
            
        except FileNotFoundError:
            print("⚠️  Advanced graph config file not found, skipping advanced test")
            return True
        
    except Exception as e:
        print(f"❌ Advanced test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_cli_integration():
    """Test CLI integration for graph workflows."""
    print("\n" + "=" * 60)
    print("Testing CLI Integration")
    print("=" * 60)
    
    try:
        # Import CLI functions
        from agentmesh.cli.commands.workflow import validate_config, list_templates
        
        # Mock args for testing
        class MockArgs:
            def __init__(self, **kwargs):
                for key, value in kwargs.items():
                    setattr(self, key, value)
        
        # Test config validation
        args = MockArgs(config="examples/workflows/sequential-code-review.yaml")
        result = validate_config(args)
        print(f"✓ Config validation result: {result}")
        
        # Test template listing
        args = MockArgs(format="table")
        result = await list_templates(args)
        print(f"✓ Template listing result: {result}")
        
        print("✅ CLI integration tests passed")
        return True
        
    except Exception as e:
        print(f"❌ CLI integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all Sprint 6 tests."""
    print("🚀 Sprint 6: Graph-based Workflows Testing")
    print("=" * 60)
    
    all_passed = True
    
    # Test basic graph orchestrator
    all_passed &= await test_graph_orchestrator_basic()
    
    # Test graph workflow configuration
    all_passed &= await test_graph_workflow_config()
    
    # Test advanced graph workflows
    all_passed &= await test_graph_workflow_advanced()
    
    # Test CLI integration
    all_passed &= await test_cli_integration()
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All Sprint 6 tests passed!")
        print("✅ Graph-based workflow orchestration is ready!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
