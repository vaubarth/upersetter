from pathlib import Path

from anypath.anypath import AnyPath, path_provider
from anypath.pathprovider.git import GitPath
from anypath.pathprovider.http import HttpPath
from anypath.pathprovider.local import LocalPath
from anypath.pathprovider.mercurial import HgPath
from anypath.pathprovider.sftp import SftpPath

from upersetter.utils import check_if_safe, get_expanded


class FileHandler:
    """Handles creation of files either based on a content string or a template defined in the structure"""
    def __init__(self, key, value, parent, setup):
        self.key = key
        self.value = value
        self.parent = parent
        self.templates_path = setup._templates_path
        self.out_dir = setup._out_dir
        self.unsafe = setup._unsafe
        self.options = setup._options

    def check(self):
        return self.key == ':files' and isinstance(self.value, list)

    def create(self):
        for file in self.value:
            self.make_file(file)

    def make_file(self, file):
        name = list(file.keys())[0]
        file_inner = file[name]
        path = Path(self.parent).joinpath(Path(name)) if self.parent else Path(name)
        if not self.unsafe:
            check_if_safe(path, self.out_dir)
        # Check how to create the content of the file
        if 'template' in file_inner:
            content = self.from_template(file_inner)
        elif 'content' in file_inner:
            content = file_inner['content']
        else:
            raise NotImplemented(f'No appropriate key in the file description to handle {file}')
        self.out_dir.joinpath(path).write_text(content)

    def from_template(self, file_inner):
        if isinstance(file_inner['template'], dict):
            template = file_inner['template']['file']
            options = file_inner['template']['context']
        else:
            template = file_inner['template']
            options = self.options
        return get_expanded(str(self.templates_path), template, options)


class RemoteHandler:
    """Handles getting files and folders from a remote location.
    The files and folders will be copied instead of created from scratch from the structure definition.
    """
    def __init__(self, key, value, parent, setup):
        self.key = key
        self.value = value
        self.parent = Path(parent) if parent else Path()
        path_provider.add(HttpPath, GitPath, HgPath, LocalPath, SftpPath)

    def check(self):
        if self.key == ':remote':
            for local, remote in self.value.items():
                if not isinstance(local, str) and not isinstance(remote, str):
                    return False
            return True

    def create(self):
        for local, remote in self.value.items():
            AnyPath(remote, self.parent.joinpath(local)).fetch()
