import unittest
from tools.scribe.core.event_bus import EventBus
import threading
import time

class TestEventBus(unittest.TestCase):
    def setUp(self):
        self.bus = EventBus(maxsize=5)

    def test_publish_subscribe(self):
        result = []
        def handler(data):
            result.append(data)
        self.bus.subscribe('test_event', handler)
        self.bus.publish('test_event', 'data1')
        time.sleep(0.1)  # Allow processing
        self.assertEqual(result, ['data1'])

    def test_multiple_subscribers(self):
        results = [0, 0]
        def handler1(data): results[0] += data
        def handler2(data): results[1] += data
        self.bus.subscribe('multi', handler1)
        self.bus.subscribe('multi', handler2)
        self.bus.publish('multi', 5)
        time.sleep(0.1)
        self.assertEqual(results, [5, 5])

if __name__ == '__main__':
    unittest.main() 