import threading


class Engine:
    POLLING_INTERVAL = 2.0

    def __init__(self, adapter, calculator):
        self.adapter = adapter
        self.calculator = calculator
        self.original_gamma = self.adapter.get_original_gamma()

        self.is_active = False
        self.current_temp = 1.0

        # Primitivas de concurrencia seguras
        self._stop_event = threading.Event()
        self._state_lock = threading.Lock()
        self._thread = None

    def start(self):
        """init the guardian thread"""
        if self._thread is not None and self._thread.is_alive():
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._guardian_loop, daemon=True)
            self._thread.start()

    def stop(self):
        """stop the guardian thread"""
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=3.0)
        self.restore()

    def _guardian_loop(self):
        """background loop that reapplies the filter every certain interval"""
        while not self._stop_event.wait(self.POLLING_INTERVAL):
            with self._state_lock:
                is_active = self.is_active

            if is_active:
                self._apply_current_state()

    def _apply_current_state(self):
        """apply the current state to the adapter"""
        with self._state_lock:
            if not self.is_active:
                return
            temp = self.current_temp

        new_gamma = self.calculator.calculate_gamma(
            self.original_gamma["r"],
            self.original_gamma["g"],
            self.original_gamma["b"],
            temp,
        )

        try:
            self.adapter.set_gamma(
                self.original_gamma["size"],
                new_gamma["r"],
                new_gamma["g"],
                new_gamma["b"],
            )
        except Exception as e:
            print(f"Error applying gamma: {e}")

    def restore(self):
        """restore the original gamma values"""

        with self._state_lock:
            self.is_active = False
            self.current_temp = 1.0

        try:
            self.adapter.set_gamma(
                self.original_gamma["size"],
                self.original_gamma["r"],
                self.original_gamma["g"],
                self.original_gamma["b"],
            )
        except Exception as e:
            print(f"Error restoring gamma: {e}")

    def set_temperature(self, temp):
        """update the temperature instantly"""
        with self._state_lock:
            self.current_temp = temp
            self.is_active = True
        self._apply_current_state()
