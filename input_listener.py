from pynput import keyboard
import threading

class GlobalInputListener:
    def __init__(self, toggle_callback):
        self.toggle_callback = toggle_callback
        self.listener = None
        self.thread = None

    def on_release(self, key):
        try:
            # Check if key is '0'
            if hasattr(key, 'char') and key.char == '0':
                self.toggle_callback()
        except AttributeError:
            pass

    def start(self):
        """Starts the listener in a non-blocking way."""
        # pynput Listener blocks, so we run it in a thread or use its non-blocking start
        self.listener = keyboard.Listener(on_release=self.on_release)
        self.listener.start()

    def stop(self):
        if self.listener:
            self.listener.stop()
