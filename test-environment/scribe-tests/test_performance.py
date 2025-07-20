import unittest
import time
import os
import tempfile
from pathlib import Path
from tools.scribe.engine import ScribeEngine

class TestPerformance(unittest.TestCase):
    def test_throughput(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            engine = ScribeEngine(watch_paths=[tmpdir])
            engine.start()
            start_time = time.time()
            for i in range(100):
                with open(Path(tmpdir) / f'test{i}.md', 'w') as f:
                    f.write(f'# Test {i}')
            time.sleep(5)  # Allow processing
            duration = time.time() - start_time
            engine.stop()
            self.assertLess(duration, 10, f'Processed 100 events in {duration}s') 