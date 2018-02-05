import unittest
from pathlib import Path

import yaml

from upersetter.utils import get_default_path, check_if_safe, get_expanded


class TestSetup(unittest.TestCase):

    def test_get_default_path_parent(self):
        path = get_default_path('/tmp', 'somefile')
        self.assertEqual(path.resolve(), Path('/tmp/somefile').resolve())

    def test_get_default_path_no_parent(self):
        path = get_default_path(None, '/tmp')
        self.assertEqual(path.resolve(), Path('/tmp').resolve())

    def test_check_if_safe_safe(self):
        safe = check_if_safe(Path('/tmp/foo'), Path('/tmp'))
        self.assertTrue(safe)

    def test_check_if_safe_unsafe(self):
        with self.assertRaisesRegex(IOError, '[Errno Trying to write to a path outside of the out directory]'):
            check_if_safe(Path('/tmp'), Path('/tmp/foo'))


    def test_get_expanded(self):
        options = yaml.safe_load(Path('./resources/options.yaml').read_text())
        expected = """test:
  :files:
    - testfile1:
        content: testfile1 content
    - testfile2:
        content: expanded content
  test1:
    test2:
      :files:
        - 'expanded_filename.txt':
            content: testfile3 content"""
        expanded = get_expanded('./resources', 'expand_structure.yaml', options)

        self.assertEqual(expanded, expected)