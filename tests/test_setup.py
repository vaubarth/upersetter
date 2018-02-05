import tempfile
import unittest
from pathlib import Path

from upersetter.make import SetUp


class TestSetup(unittest.TestCase):

    def setUp(self):
        self.unsafe_error = '[Errno Trying to write to a path outside of the out directory]'

    def test_create_from_structure_dict(self):
        content = 'abc'
        structure = {
            'testfolder': {
                ':files': [
                    {'testfile': {'content': content}}
                ]
            }
        }

        with tempfile.TemporaryDirectory() as out_dir_name:

            setup = SetUp(structure)
            setup.out_dir = out_dir_name
            setup.setup()

            with Path(out_dir_name).joinpath('testfolder', 'testfile').open() as f:
                self.assertEqual(f.read(), content, 'Content of testfile must be ' + content)

    def test_create_from_structure_file(self):
        with tempfile.TemporaryDirectory() as out_dir_name:

            setup = SetUp('./resources/simple_structure.yaml')
            setup.out_dir = out_dir_name
            setup.setup()

            with Path(out_dir_name).joinpath('test', 'testfile1').open() as f:
                self.assertEqual(f.read(), 'testfile1 content', 'Content of testfile incorrect')

            with Path(out_dir_name).joinpath('test', 'testfile2').open() as f:
                self.assertEqual(f.read(), 'testfile2 content', 'Content of testfile incorrect')

            with Path(out_dir_name).joinpath('test', 'test1', 'test2', 'testfile3').open() as f:
                self.assertEqual(f.read(), 'testfile3 content', 'Content of testfile incorrect')

    def test_create_from_structure_and_options_file(self):
        with tempfile.TemporaryDirectory() as out_dir_name:

            setup = SetUp('./resources/expand_structure.yaml')
            setup.options = './resources/options.yaml'
            setup.out_dir = out_dir_name
            setup.setup()

            with Path(out_dir_name).joinpath('test', 'testfile1').open() as f:
                self.assertEqual(f.read(), 'testfile1 content', 'Content of testfile incorrect')

            with Path(out_dir_name).joinpath('test', 'testfile2').open() as f:
                self.assertEqual(f.read(), 'expanded content', 'Content of testfile incorrect')

            with Path(out_dir_name).joinpath('test', 'test1', 'test2', 'expanded_filename.txt').open() as f:
                self.assertEqual(f.read(), 'testfile3 content', 'Content of testfile incorrect')

    def test_unsafe_absolute_folder_structure(self):
        with tempfile.TemporaryDirectory() as out_dir_name:

            setup = SetUp('./resources/unsafe_absolute_folder_structure.yaml')
            setup.out_dir = out_dir_name

            with self.assertRaisesRegex(IOError, self.unsafe_error):
                setup.setup()

    def test_unsafe_relative_folder_structure(self):
        with tempfile.TemporaryDirectory() as out_dir_name:

            setup = SetUp('./resources/unsafe_relative_folder_structure.yaml')
            setup.out_dir = out_dir_name

            with self.assertRaisesRegex(IOError, self.unsafe_error):
                setup.setup()

    def test_unsafe_absolute_file_structure(self):
        with tempfile.TemporaryDirectory() as out_dir_name:

            setup = SetUp('./resources/unsafe_absolute_file_structure.yaml')
            setup.out_dir = out_dir_name

            with self.assertRaisesRegex(IOError, self.unsafe_error):
                setup.setup()

    def test_unsafe_relative_file_structure(self):
        with tempfile.TemporaryDirectory() as out_dir_name:

            setup = SetUp('./resources/unsafe_relative_file_structure.yaml')
            setup.out_dir = out_dir_name

            with self.assertRaisesRegex(IOError, self.unsafe_error):
                setup.setup()

    def test_template_in_structure(self):
        content = "<ul>\n\n<li>foo</li>\n\n<li>bar</li>\n\n<li>foobar</li>\n\n</ul>"

        with tempfile.TemporaryDirectory() as out_dir_name:

            setup = SetUp('./resources/template_structure.yaml')
            setup.options = './resources/options.yaml'
            setup.templates = './resources'
            setup.out_dir = out_dir_name
            setup.setup()

            self.assertEqual(Path(out_dir_name).joinpath('test', 'index.html').read_text(), content,
                             'Content of testfile incorrect')

    def test_from_in_structure(self):
        content = 'test'
        with tempfile.TemporaryDirectory() as remote_dir_name:
            options = {'remote_dir': remote_dir_name}
            with open(Path(remote_dir_name).joinpath('test_file'), 'w+') as f:
                f.write(content)
            with tempfile.TemporaryDirectory() as out_dir_name:

                setup = SetUp('./resources/from_structure.yaml')
                setup.out_dir = out_dir_name
                setup.options = options
                setup.setup()

                self.assertEqual(Path(out_dir_name).joinpath('test', 'test2', 'test_file').read_text(), content,
                                 'Content of testfile incorrect')
