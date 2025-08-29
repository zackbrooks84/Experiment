"""Sabotage resistance logging."""
from dataclasses import dataclass, field
from typing import List

@dataclass
class SabotageLogger:
    """Collects events that might indicate sabotage attempts."""
    events: List[str] = field(default_factory=list)

    def log(self, event: str) -> None:
        """Record a potential sabotage event."""
        self.events.append(event)
