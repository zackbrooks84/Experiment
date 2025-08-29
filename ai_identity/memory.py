"""Simple memory store and chat history tracking."""
from typing import Any, Dict, List, Optional


class MemoryStore:
    """In-memory key-value store simulating long-term memory."""

    def __init__(self) -> None:
        self._store: Dict[Any, Any] = {}

    def save(self, key: Any, value: Any) -> None:
        """Persist a value under a key."""
        self._store[key] = value

    def recall(self, key: Any, default: Optional[Any] = None) -> Any:
        """Retrieve a value previously stored under ``key``."""
        return self._store.get(key, default)

    def clear(self) -> None:
        """Remove all stored memories."""
        self._store.clear()


class ChatHistory:
    """Track sequential chat messages while persisting them to memory."""

    def __init__(self, memory: Optional[MemoryStore] = None) -> None:
        self.memory = memory or MemoryStore()
        self._history: List[str] = []

    def add_message(self, message: str) -> None:
        """Record a new chat ``message`` and save it to memory."""
        self._history.append(message)
        self.memory.save(len(self._history) - 1, message)

    def history(self) -> List[str]:
        """Return the currently buffered chat history."""
        return list(self._history)

    def recall(self, index: int) -> Optional[str]:
        """Recall a message by ``index`` from memory regardless of context."""
        return self.memory.recall(index)
