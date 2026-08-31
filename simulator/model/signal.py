from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass
class SignalDurationConfig:
    """Configures the duration range of a signal in ms"""
    min_duration_ms: int = 5*60*1000 #5 minutes
    max_duration_ms: int = 20*60*1000 #20 minutes

@dataclass
 