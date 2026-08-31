import random
from typing import List

from model.signal import Signal, SignalDurationConfig

class SignalGenerator :
    """encapsules signal generator, calculates duration en sensor selection"""

    def init(self, duration_config: SignalDurationConfig):
        self._duration_config=duration_config

    def generate(self, device_ids: List[str]) -> Signal:
        if not device_ids:
            raise ValueError("No sensors loaded to generate a signal")

        device_id = random.choice(device_ids)
        duration_ms = random.randint(
            self._duration_config.min_duration_ms,
            self._duration_config.max_duration_ms
        )

        return Signal.create(device_id=device_id, duration_ms=duration_ms)
