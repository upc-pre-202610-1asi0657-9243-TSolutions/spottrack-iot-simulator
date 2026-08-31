import threading
import time
import requests
from flask import Flask, jsonify

from model.signal_generator import SignalGenerator
from interfaces.mqtt_publisher import MqttPublisher


class SimulatorApi:
    """Expone el endpoint /update y controla el loop de emisión de señales."""

    def __init__(
        self,
        generator: SignalGenerator,
        publisher: MqttPublisher,
        backend_devices_url: str,
        emit_interval_seconds: int = 8
    ):
        self._generator = generator
        self._publisher = publisher
        self._backend_devices_url = backend_devices_url
        self._emit_interval_seconds = emit_interval_seconds
        self._device_ids = []
        self._app = Flask(__name__)
        self._register_routes()

    def _register_routes(self):
        @self._app.route("/update", methods=["POST"])
        def update_devices():
            try:
                response = requests.get(self._backend_devices_url, timeout=5)
                response.raise_for_status()
                data = response.json()
                self._device_ids = [d["deviceId"] for d in data]
                return jsonify({"status": "ok", "count": len(self._device_ids)}), 200
            except requests.RequestException as e:
                return jsonify({"status": "error", "message": str(e)}), 500

        @self._app.route("/status", methods=["GET"])
        def status():
            return jsonify({"deviceCount": len(self._device_ids), "deviceIds": self._device_ids}), 200

    def _simulation_loop(self):
        while True:
            if self._device_ids:
                signal = self._generator.generate(self._device_ids)
                self._publisher.publish_signal(signal)
            time.sleep(self._emit_interval_seconds)

    def run(self, host: str = "0.0.0.0", port: int = 5000):
        self._publisher.connect()
        threading.Thread(target=self._simulation_loop, daemon=True).start()
        self._app.run(host=host, port=port)