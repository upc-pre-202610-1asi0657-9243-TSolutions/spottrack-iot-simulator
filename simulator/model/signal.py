from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass
class SignalDurationConfig:
    """Configures the duration range of a signal in ms"""
    min_duration_ms: int = 5*60*1000 #5 minutes
    max_duration_ms: int = 20*60*1000 #20 minutes

@dataclass
class Signal :
    """Represents a signal emitted from a sensor"""
    device_id:  str
    signal_type: str
    duration_ms: int
    timestamp: str

    @staticmethod
    def create(device_id: str, duration_ms: int, signal_type: str ="ACTIVATED") -> "Signal":
        return Signal(
            device_id=device_id,
            signal_type=signal_type,
            duration_ms=duration_ms,
            timestamp=datetime.now(timezone.utc).isoformat()
        )