import unittest
from tools.scribe.core.ports import AtomicFileWriter
import tempfile
import os

class TestPorts(unittest.TestCase):
    def test_atomic_file_writer(self):
        writer = AtomicFileWriter()
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            path = tmp.name
        content = "Test content"
        success = writer.write(path, content)
        self.assertTrue(success)
        with open(path, 'r') as f:
            self.assertEqual(f.read(), content)
        os.unlink(path)

if __name__ == '__main__':
    unittest.main() 