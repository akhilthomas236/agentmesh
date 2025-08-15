"""Message models for AgentMesh."""

from typing import Any, Dict, Optional, Union
from enum import Enum
from datetime import datetime
import uuid


class MessageType(str, Enum):
    """Message type enumeration."""
    TEXT = "text"
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    FUNCTION = "function"


class BaseChatMessage:
    """Base class for chat messages."""
    
    def __init__(
        self,
        content: str,
        message_type: MessageType = MessageType.TEXT,
        sender_id: Optional[str] = None,
        recipient_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None,
        message_id: Optional[str] = None
    ):
        self.message_id = message_id or str(uuid.uuid4())
        self.content = content
        self.message_type = message_type
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.metadata = metadata or {}
        self.timestamp = timestamp or datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary."""
        return {
            "message_id": self.message_id,
            "content": self.content,
            "message_type": self.message_type.value,
            "sender_id": self.sender_id,
            "recipient_id": self.recipient_id,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BaseChatMessage":
        """Create message from dictionary."""
        timestamp = None
        if data.get("timestamp"):
            timestamp = datetime.fromisoformat(data["timestamp"])
        
        return cls(
            content=data["content"],
            message_type=MessageType(data.get("message_type", MessageType.TEXT)),
            sender_id=data.get("sender_id"),
            recipient_id=data.get("recipient_id"),
            metadata=data.get("metadata", {}),
            timestamp=timestamp,
            message_id=data.get("message_id")
        )
    
    def __str__(self) -> str:
        return f"Message({self.message_type.value}): {self.content[:100]}..."
    
    def __repr__(self) -> str:
        return f"BaseChatMessage(id={self.message_id}, type={self.message_type.value})"


class TextMessage(BaseChatMessage):
    """Text message implementation."""
    
    def __init__(
        self,
        content: str,
        sender_id: Optional[str] = None,
        recipient_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None,
        message_id: Optional[str] = None
    ):
        super().__init__(
            content=content,
            message_type=MessageType.TEXT,
            sender_id=sender_id,
            recipient_id=recipient_id,
            metadata=metadata,
            timestamp=timestamp,
            message_id=message_id
        )


class SystemMessage(BaseChatMessage):
    """System message implementation."""
    
    def __init__(
        self,
        content: str,
        sender_id: Optional[str] = None,
        recipient_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None,
        message_id: Optional[str] = None
    ):
        super().__init__(
            content=content,
            message_type=MessageType.SYSTEM,
            sender_id=sender_id,
            recipient_id=recipient_id,
            metadata=metadata,
            timestamp=timestamp,
            message_id=message_id
        )


class UserMessage(BaseChatMessage):
    """User message implementation."""
    
    def __init__(
        self,
        content: str,
        sender_id: Optional[str] = None,
        recipient_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None,
        message_id: Optional[str] = None
    ):
        super().__init__(
            content=content,
            message_type=MessageType.USER,
            sender_id=sender_id,
            recipient_id=recipient_id,
            metadata=metadata,
            timestamp=timestamp,
            message_id=message_id
        )


class AssistantMessage(BaseChatMessage):
    """Assistant message implementation."""
    
    def __init__(
        self,
        content: str,
        sender_id: Optional[str] = None,
        recipient_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None,
        message_id: Optional[str] = None
    ):
        super().__init__(
            content=content,
            message_type=MessageType.ASSISTANT,
            sender_id=sender_id,
            recipient_id=recipient_id,
            metadata=metadata,
            timestamp=timestamp,
            message_id=message_id
        )


class FunctionMessage(BaseChatMessage):
    """Function call message implementation."""
    
    def __init__(
        self,
        content: str,
        function_name: str,
        function_args: Optional[Dict[str, Any]] = None,
        sender_id: Optional[str] = None,
        recipient_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None,
        message_id: Optional[str] = None
    ):
        metadata = metadata or {}
        metadata.update({
            "function_name": function_name,
            "function_args": function_args or {}
        })
        
        super().__init__(
            content=content,
            message_type=MessageType.FUNCTION,
            sender_id=sender_id,
            recipient_id=recipient_id,
            metadata=metadata,
            timestamp=timestamp,
            message_id=message_id
        )
    
    @property
    def function_name(self) -> str:
        """Get function name."""
        return self.metadata.get("function_name", "")
    
    @property
    def function_args(self) -> Dict[str, Any]:
        """Get function arguments."""
        return self.metadata.get("function_args", {})


# Utility functions
def create_text_message(content: str, sender_id: Optional[str] = None) -> TextMessage:
    """Create a text message."""
    return TextMessage(content=content, sender_id=sender_id)


def create_system_message(content: str) -> SystemMessage:
    """Create a system message."""
    return SystemMessage(content=content, sender_id="system")


def create_user_message(content: str, user_id: Optional[str] = None) -> UserMessage:
    """Create a user message."""
    return UserMessage(content=content, sender_id=user_id or "user")


def create_assistant_message(content: str, assistant_id: Optional[str] = None) -> AssistantMessage:
    """Create an assistant message."""
    return AssistantMessage(content=content, sender_id=assistant_id or "assistant")
