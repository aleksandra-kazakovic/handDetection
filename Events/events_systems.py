class Event:
    def __init__(self):
        self.events = {}

    def register_event(self, event, function):
        handlers = self.events.get(event)
        if handlers is None:
            self.events[event] = [function]
        else:
            handlers.append(function)

    def dispatch(self, event, data):
        handlers = self.events.get(event)
        if event is None:
            raise ValueError(f"Event {event} was not found")
        for handler in handlers:
            handler(data)