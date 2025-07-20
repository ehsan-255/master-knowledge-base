import queue
from typing import Any, Callable, Dict, List

class EventBus:
    def __init__(self, maxsize: int = 0):
        self._subscribers: Dict[str, List[Callable[[Any], None]]] = {}
        self._queue = queue.Queue(maxsize=maxsize)
    
    def qsize(self) -> int:
        """Return the approximate size of the queue."""
        return self._queue.qsize()

    def subscribe(self, event_type: str, handler: Callable[[Any], None]):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)

    def publish(self, event_type: str, data: Any):
        self._queue.put({'type': event_type, 'data': data})

    def process_events(self):
        """Process all events currently in the queue."""
        while not self._queue.empty():
            try:
                event = self._queue.get_nowait()
                handlers = self._subscribers.get(event['type'], [])
                for handler in handlers:
                    handler(event['type'], event['data'])
                self._queue.task_done()
            except:
                break 