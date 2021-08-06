# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: MPL-2.0, see LICENSE for more details.
'''Configuration for package manager.'''

import os
from dataclasses import dataclass, field
from typing import Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from proman_common.manifest import LockFile, SourceTreeFile

url_base = os.getenv('PROMAN_GITHUB_URL', 'https://api.github.com')


@dataclass
class ProjectPaths:
    '''Project directories.'''

    working_dir: str = os.getcwd()
    virtualenv_dir: Optional[str] = os.getenv('VIRTUAL_ENV', None)
    pyproject_path: str = field(init=False)
    lock_path: str = field(init=False)
    pypackages_dir: str = field(init=False)

    def __post_init__(self) -> None:
        '''Initialize python project.'''
        self.pyproject_path = os.path.join(self.working_dir, 'pyproject.toml')
        self.lock_path = os.path.join(self.working_dir, 'proman-lock.json')
        self.pypackages_dir = os.path.join(self.working_dir, '__pypackages__')


class Manifest:
    '''Provide package manifest.'''

    def __init__(
        self,
        source_tree: 'SourceTreeFile',
        lockfile: 'LockFile',
    ) -> None:
        '''Initialize project manifest.'''
        self.__source_tree = source_tree
        self.__lockfile = lockfile

    def save(self) -> None:
        '''Save each configuration.'''
        self.__source_tree.save()
        self.__lockfile.save()

    def add_dependency(
        self,
        name: str,
        version: str,
        dev: bool = False,
        **kwargs: Any,
    ) -> None:
        '''Add dependency to configuration.'''
        if self.__source_tree.is_dependency(name, dev):
            dependency = self.__source_tree.get_dependency(name, dev)
            print('package:', dependency)
        else:
            self.__source_tree.add_dependency(name, version, dev)

        if self.__lockfile.is_locked(name, dev):
            locked = self.__lockfile.get_lock(name, dev)
            print('package locked:', locked)
        else:
            self.__lockfile.add_lock(name, version, dev)
        self.save()

    def remove_dependency(self, name: str, dev: bool = False) -> None:
        '''Remove dependency from configuration.'''
        if self.__source_tree.is_dependency(name, dev):
            self.__source_tree.remove_dependency(name, dev)
        else:
            print('package is not tracked:', name)
        if self.__lockfile.is_locked(name, dev):
            self.__lockfile.remove_lock(name, dev)
        else:
            print('lock is not locked:', name)
        self.save()