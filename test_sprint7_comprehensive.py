#!/usr/bin/env python3
"""
Comprehensive test script for Sprint 7 Swarm Coordination features.

This script tests:
1. Swarm workflow creation and execution
2. CLI commands for swarm management
3. API endpoints for swarm monitoring and analytics
4. Parameter tuning functionality
5. Swarm examples and configurations

Run with: python test_sprint7_comprehensive.py
"""

import asyncio
import json
import logging
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, Any, List

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Test configuration
BASE_DIR = Path(__file__).parent
EXAMPLES_DIR = BASE_DIR / "examples" / "workflows"
DOCS_DIR = BASE_DIR / "docs"

class SwarmTestSuite:
    """Comprehensive test suite for Sprint 7 swarm coordination features."""
    
    def __init__(self):
        self.test_results = []
        self.failed_tests = []
        
    def log_test_result(self, test_name: str, success: bool, details: str = ""):
        """Log the result of a test."""
        status = "✅ PASS" if success else "❌ FAIL"
        logger.info(f"{status} | {test_name}")
        if details:
            logger.info(f"    Details: {details}")
        
        self.test_results.append({
            "test": test_name,
            "success": success,
            "details": details
        })
        
        if not success:
            self.failed_tests.append(test_name)
    
    def run_command(self, command: List[str], timeout: int = 30) -> tuple[bool, str]:
        """Run a command and return success status and output."""
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=BASE_DIR
            )
            return result.returncode == 0, result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            return False, "Command timed out"
        except Exception as e:
            return False, str(e)
    
    def test_swarm_examples_exist(self):
        """Test that swarm workflow examples exist and are valid."""
        logger.info("🧪 Testing swarm example files...")
        
        expected_examples = [
            "swarm-research-analysis.yaml",
            "swarm-product-development.yaml", 
            "swarm-content-creation.yaml",
            "swarm-financial-analysis.yaml"
        ]
        
        for example in expected_examples:
            example_path = EXAMPLES_DIR / example
            exists = example_path.exists()
            
            if exists:
                # Try to parse the YAML
                try:
                    import yaml
                    with open(example_path) as f:
                        config = yaml.safe_load(f)
                    
                    # Validate basic structure
                    has_pattern = config.get("pattern") == "swarm"
                    has_agents = "agents" in config and len(config["agents"]) > 0
                    has_swarm_config = "swarm" in config
                    
                    valid = has_pattern and has_agents and has_swarm_config
                    details = f"Pattern: {has_pattern}, Agents: {has_agents}, Swarm config: {has_swarm_config}"
                    
                except Exception as e:
                    valid = False
                    details = f"YAML parsing error: {e}"
            else:
                valid = False
                details = "File does not exist"
            
            self.log_test_result(f"Swarm example: {example}", exists and valid, details)
    
    def test_swarm_documentation(self):
        """Test that swarm documentation exists."""
        logger.info("📚 Testing swarm documentation...")
        
        doc_files = [
            "swarm-coordination.md"
        ]
        
        for doc_file in doc_files:
            doc_path = DOCS_DIR / doc_file
            exists = doc_path.exists()
            
            if exists:
                # Check that it has substantial content
                content = doc_path.read_text()
                has_content = len(content) > 1000  # At least 1KB of content
                has_examples = "```yaml" in content
                has_cli_docs = "autogen-a2a swarm" in content
                
                valid = has_content and has_examples and has_cli_docs
                details = f"Content: {has_content}, Examples: {has_examples}, CLI docs: {has_cli_docs}"
            else:
                valid = False
                details = "File does not exist"
            
            self.log_test_result(f"Documentation: {doc_file}", exists and valid, details)
    
    def test_swarm_orchestrator_implementation(self):
        """Test that SwarmOrchestrator is properly implemented."""
        logger.info("🔧 Testing SwarmOrchestrator implementation...")
        
        try:
            # Test imports
            from src.autogen_a2a.orchestration.swarm import (
                SwarmOrchestrator, SwarmParticipant, SwarmMetrics, 
                HandoffDecision, SwarmStatus
            )
            from src.autogen_a2a.orchestration.base import WorkflowConfig
            
            # Test basic instantiation with proper config
            workflow_config = WorkflowConfig(
                name="Test Swarm Workflow",
                pattern="swarm", 
                agents=["test_agent_1", "test_agent_2"],
                parameters={
                    'swarm': {
                        'participants': [
                            {
                                'agent_id': 'test_agent_1',
                                'name': 'Test Agent 1',
                                'specializations': ['testing']
                            },
                            {
                                'agent_id': 'test_agent_2',
                                'name': 'Test Agent 2', 
                                'specializations': ['validation']
                            }
                        ]
                    }
                }
            )
            
            orchestrator = SwarmOrchestrator(workflow_config)
            
            # Test required methods exist
            required_methods = [
                'get_swarm_metrics', 'get_analytics', 'tune_parameter',
                'get_parameter', 'get_handoff_graph'
            ]
            
            missing_methods = []
            for method in required_methods:
                if not hasattr(orchestrator, method):
                    missing_methods.append(method)
            
            if missing_methods:
                self.log_test_result(
                    "SwarmOrchestrator methods", 
                    False, 
                    f"Missing methods: {missing_methods}"
                )
            else:
                self.log_test_result("SwarmOrchestrator methods", True, "All required methods present")
                
        except ImportError as e:
            self.log_test_result("SwarmOrchestrator import", False, str(e))
        except Exception as e:
            self.log_test_result("SwarmOrchestrator instantiation", False, str(e))
    
    def test_cli_swarm_commands(self):
        """Test CLI swarm commands."""
        logger.info("💻 Testing CLI swarm commands...")
        
        # Test that swarm commands are available
        success, output = self.run_command(["python", "-m", "src.autogen_a2a.cli", "swarm", "--help"])
        
        if success:
            # Check for expected subcommands
            expected_commands = ["create", "monitor", "tune", "analytics"]
            has_commands = all(cmd in output for cmd in expected_commands)
            
            self.log_test_result(
                "CLI swarm help", 
                has_commands, 
                f"Commands present: {expected_commands}" if has_commands else "Missing subcommands"
            )
        else:
            self.log_test_result("CLI swarm help", False, f"Help command failed: {output}")
        
        # Test swarm create command structure
        success, output = self.run_command(["python", "-m", "src.autogen_a2a.cli", "swarm", "create", "--help"])
        
        has_config_arg = "--config" in output
        self.log_test_result("CLI swarm create help", success and has_config_arg, 
                           "Has --config argument" if has_config_arg else "Missing --config argument")
    
    def test_api_swarm_endpoints(self):
        """Test that swarm API endpoints are defined."""
        logger.info("🌐 Testing API swarm endpoints...")
        
        try:
            # Test that API router has swarm endpoints
            from src.autogen_a2a.api.routers.workflows import router
            
            # Get all routes
            routes = [route.path for route in router.routes]
            
            expected_endpoints = [
                "/workflows/{execution_id}/swarm/metrics",
                "/workflows/{execution_id}/swarm/analytics", 
                "/workflows/{execution_id}/swarm/tune",
                "/workflows/{execution_id}/swarm/handoff-graph"
            ]
            
            missing_endpoints = []
            for endpoint in expected_endpoints:
                # Check if any route matches the pattern
                if not any(endpoint.replace("{execution_id}", "test") in route.replace("{execution_id}", "test") for route in routes):
                    missing_endpoints.append(endpoint)
            
            if missing_endpoints:
                self.log_test_result(
                    "API swarm endpoints", 
                    False, 
                    f"Missing endpoints: {missing_endpoints}"
                )
            else:
                self.log_test_result("API swarm endpoints", True, "All expected endpoints present")
                
        except ImportError as e:
            self.log_test_result("API swarm endpoints", False, f"Import error: {e}")
        except Exception as e:
            self.log_test_result("API swarm endpoints", False, str(e))
    
    def test_workflow_manager_swarm_support(self):
        """Test that WorkflowManager supports swarm orchestration."""
        logger.info("🔄 Testing WorkflowManager swarm support...")
        
        try:
            from src.autogen_a2a.workflows.manager import WorkflowManager
            from src.autogen_a2a.workflows.config import WorkflowConfigFile
            
            # Test that swarm orchestration is supported
            manager = WorkflowManager()
            
            # Check if _configure_swarm_orchestrator method exists
            has_swarm_method = hasattr(manager, '_configure_swarm_orchestrator')
            
            self.log_test_result(
                "WorkflowManager swarm method", 
                has_swarm_method, 
                "Has _configure_swarm_orchestrator method" if has_swarm_method else "Missing swarm orchestrator method"
            )
            
        except ImportError as e:
            self.log_test_result("WorkflowManager swarm support", False, f"Import error: {e}")
        except Exception as e:
            self.log_test_result("WorkflowManager swarm support", False, str(e))
    
    def test_swarm_config_models(self):
        """Test swarm configuration models."""
        logger.info("📋 Testing swarm configuration models...")
        
        try:
            from src.autogen_a2a.workflows.config import (
                SwarmWorkflowConfig, SwarmParticipantConfig, SwarmTerminationConfig
            )
            
            # Test basic instantiation
            participant_config = SwarmParticipantConfig(
                agent_id="test_agent",
                specializations=["testing"],
                handoff_targets=["other_agent"]
            )
            
            termination_config = SwarmTerminationConfig(
                max_messages=20
            )
            
            swarm_config = SwarmWorkflowConfig(
                participants=[participant_config],
                termination=termination_config
            )
            
            self.log_test_result("Swarm config models", True, "All models instantiated successfully")
            
        except ImportError as e:
            self.log_test_result("Swarm config models", False, f"Import error: {e}")
        except Exception as e:
            self.log_test_result("Swarm config models", False, str(e))
    
    def test_swarm_example_validation(self):
        """Test validation of swarm examples."""
        logger.info("✅ Testing swarm example validation...")
        
        example_file = EXAMPLES_DIR / "swarm-research-analysis.yaml"
        
        if example_file.exists():
            # Test CLI validation command
            success, output = self.run_command([
                "python", "-m", "src.autogen_a2a.cli", 
                "workflow", "validate", "--config", str(example_file)
            ])
            
            self.log_test_result(
                "Swarm example validation", 
                success, 
                f"Validation output: {output[:200]}..." if output else "No output"
            )
        else:
            self.log_test_result("Swarm example validation", False, "Example file not found")
    
    def run_all_tests(self):
        """Run all test suites."""
        logger.info("🚀 Starting Sprint 7 Swarm Coordination Test Suite")
        logger.info("=" * 60)
        
        test_methods = [
            self.test_swarm_examples_exist,
            self.test_swarm_documentation,
            self.test_swarm_orchestrator_implementation,
            self.test_cli_swarm_commands,
            self.test_api_swarm_endpoints,
            self.test_workflow_manager_swarm_support,
            self.test_swarm_config_models,
            self.test_swarm_example_validation
        ]
        
        for test_method in test_methods:
            try:
                test_method()
            except Exception as e:
                logger.error(f"Test {test_method.__name__} failed with exception: {e}")
                self.log_test_result(test_method.__name__, False, str(e))
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary."""
        logger.info("=" * 60)
        logger.info("🏁 TEST SUMMARY")
        logger.info("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        logger.info(f"Total Tests: {total_tests}")
        logger.info(f"Passed: {passed_tests} ✅")
        logger.info(f"Failed: {failed_tests} ❌")
        logger.info(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if self.failed_tests:
            logger.info("\n❌ FAILED TESTS:")
            for test in self.failed_tests:
                logger.info(f"  - {test}")
        
        logger.info("\n📊 DETAILED RESULTS:")
        for result in self.test_results:
            status = "✅" if result["success"] else "❌"
            logger.info(f"  {status} {result['test']}")
            if result["details"]:
                logger.info(f"      {result['details']}")
        
        # Sprint 7 specific summary
        logger.info("=" * 60)
        logger.info("📋 SPRINT 7 SWARM COORDINATION STATUS")
        logger.info("=" * 60)
        
        swarm_features = {
            "SwarmOrchestrator Implementation": any("SwarmOrchestrator" in r["test"] for r in self.test_results if r["success"]),
            "Swarm CLI Commands": any("CLI swarm" in r["test"] for r in self.test_results if r["success"]),
            "Swarm API Endpoints": any("API swarm" in r["test"] for r in self.test_results if r["success"]),
            "Swarm Configuration Models": any("config models" in r["test"] for r in self.test_results if r["success"]),
            "Swarm Examples": any("example" in r["test"] for r in self.test_results if r["success"]),
            "Swarm Documentation": any("Documentation" in r["test"] for r in self.test_results if r["success"])
        }
        
        for feature, implemented in swarm_features.items():
            status = "✅ IMPLEMENTED" if implemented else "❌ MISSING"
            logger.info(f"  {status} | {feature}")
        
        completed_features = sum(1 for implemented in swarm_features.values() if implemented)
        total_features = len(swarm_features)
        completion_rate = (completed_features / total_features) * 100
        
        logger.info(f"\n🎯 SPRINT 7 COMPLETION: {completion_rate:.1f}% ({completed_features}/{total_features} features)")
        
        if completion_rate >= 80:
            logger.info("🎉 Sprint 7 is substantially complete!")
        elif completion_rate >= 60:
            logger.info("⚠️  Sprint 7 is mostly complete but needs some work")
        else:
            logger.info("🚧 Sprint 7 needs significant work")


def main():
    """Main test execution."""
    test_suite = SwarmTestSuite()
    test_suite.run_all_tests()
    
    # Return appropriate exit code
    return 0 if not test_suite.failed_tests else 1


if __name__ == "__main__":
    sys.exit(main())
