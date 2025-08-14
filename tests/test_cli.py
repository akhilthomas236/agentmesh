"""Tests for the CLI functionality."""

import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Add src to path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from agentmesh.cli.__main__ import main


def test_cli_help():
    """Test that CLI shows help when no arguments provided."""
    with patch("autogen_a2a.cli.__main__.print_help") as mock_help:
        result = main([])
        mock_help.assert_called_once()
        assert result == 0


def test_cli_version():
    """Test CLI version argument."""
    with pytest.raises(SystemExit) as exc_info:
        main(["--version"])
    assert exc_info.value.code == 0


def test_agent_create_command():
    """Test agent create command."""
    with patch("autogen_a2a.cli.commands.agent.create_agent") as mock_create:
        mock_create.return_value = 0
        result = main(["agent", "create", "--name", "test", "--type", "assistant"])
        assert result == 0
        mock_create.assert_called_once()


def test_agent_list_command():
    """Test agent list command."""
    with patch("autogen_a2a.cli.commands.agent.list_agents") as mock_list:
        mock_list.return_value = 0
        result = main(["agent", "list"])
        assert result == 0
        mock_list.assert_called_once()


def test_workflow_create_command():
    """Test workflow create command."""
    with patch("autogen_a2a.cli.commands.workflow.create_workflow") as mock_create:
        mock_create.return_value = 0
        result = main(["workflow", "create", "--name", "test"])
        assert result == 0
        mock_create.assert_called_once()


def test_workflow_list_command():
    """Test workflow list command."""
    with patch("autogen_a2a.cli.commands.workflow.list_workflows") as mock_list:
        mock_list.return_value = 0
        result = main(["workflow", "list"])
        assert result == 0
        mock_list.assert_called_once()


def test_server_status_command():
    """Test server status command."""
    with patch("autogen_a2a.cli.commands.server.check_server_status") as mock_status:
        mock_status.return_value = 0
        result = main(["server", "status"])
        assert result == 0
        mock_status.assert_called_once()


def test_keyboard_interrupt():
    """Test handling of KeyboardInterrupt."""
    with patch("autogen_a2a.cli.commands.agent.handle_agent_command") as mock_handle:
        mock_handle.side_effect = KeyboardInterrupt()
        result = main(["agent", "list"])
        assert result == 130  # Standard exit code for SIGINT


def test_unknown_command():
    """Test handling of unknown commands."""
    with pytest.raises(SystemExit) as exc_info:
        main(["unknown", "command"])
    assert exc_info.value.code == 2  # argparse exits with code 2 for invalid arguments


if __name__ == "__main__":
    pytest.main([__file__])
