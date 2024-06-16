class EventHandler:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.listeners = {}

    def register_listener(self, event_name, listener):
        """
        Register a listener for a specific event.
        """
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(listener)

    def emit(self, event_name, data):
        """
        Emit an event, triggering all registered listeners.
        """
        if event_name in self.listeners:
            for listener in self.listeners[event_name]:
                listener(data)
