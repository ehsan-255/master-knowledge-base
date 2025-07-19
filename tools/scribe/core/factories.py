from typing import Dict
from .watcher import Watcher
from .worker import Worker
from .event_bus import EventBus
from .ports import IEventSource, IFileWriter

class WatcherFactory:
    @staticmethod
    def create(config: Dict, event_bus: EventBus, shutdown_event) -> IEventSource:
        watcher_type = config.get('type', 'filesystem')
        if watcher_type == 'filesystem':
            return Watcher(event_bus=event_bus, shutdown_event=shutdown_event, watch_paths=config.get('paths', ['.']), file_patterns=config.get('patterns', ['*.md']))
        raise ValueError(f"Unknown watcher type: {watcher_type}")

class WorkerFactory:
    @staticmethod
    def create(config: Dict, event_bus: EventBus, shutdown_event) -> Worker:
        return Worker(event_bus=event_bus, shutdown_event=shutdown_event, queue_timeout=config.get('timeout', 1.0)) 