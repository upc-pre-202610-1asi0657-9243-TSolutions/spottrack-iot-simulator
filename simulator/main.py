import os
from model.signal import SignalDurationConfig
from model.signal_generator import SignalGenerator
from interfaces.mqtt_publisher import MqttPublisher
from interfaces.api import SimulatorApi

MQTT_HOST = os.environ.get("MQTT_HOST", "localhost")
MQTT_PORT = int(os.environ.get("MQTT_PORT", 1883))
BACKEND_DEVICES_URL = os.environ.get("BACKEND_DEVICES_URL", "http://localhost:8080/api/devices")

def main():
    duration_config = SignalDurationConfig(
        min_duration_ms=5 * 60 * 1000,
        max_duration_ms=20 * 60 * 1000
    )
    generator = SignalGenerator(duration_config)
    publisher = MqttPublisher(host=MQTT_HOST, port=MQTT_PORT)

    api = SimulatorApi(
        generator=generator,
        publisher=publisher,
        backend_devices_url=BACKEND_DEVICES_URL
    )
    api.run()

if __name__ == "__main__":
    main()