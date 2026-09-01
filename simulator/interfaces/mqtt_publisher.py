import json
import paho.mqtt.client as mqtt
from model.signal import Signal


class MqttPublisher:
    def __init__(self, host: str, port: int = 1883, topic_prefix: str = "sensors"):
        self._host = host
        self._port = port
        self._topic_prefix = topic_prefix
        self._client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    def connect(self):
        self._client.connect(self._host, self._port, keepalive=60)
        self._client.loop_start()

    def disconnect(self):
        self._client.loop_stop()
        self._client.disconnect()

    def publish_signal(self, signal: Signal):
        topic = f"{self._topic_prefix}/{signal.device_id}/signal"
        payload = json.dumps(signal.to_dict())
        self._client.publish(topic, payload)
        print(f"Señal emitida: {signal.device_id}, duración {signal.duration_ms / 1000}s")