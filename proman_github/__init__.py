# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: MPL-2.0, see LICENSE for more details.
'''GitHub based package manager.'''

import logging
import os
# import site
from typing import List, Optional
# from urllib.parse import urljoin

from github import Github
from proman_common.config import Config
from proman_common.filepaths import GlobalDirs
from proman_common.manifest import LockFile, SourceTreeFile
# from proman_common.system import System

from .config import ProjectPaths, Manifest
# from .distributions import LocalDistributionPath, UserDistributionPath
from .package_manager import PackageManager

# package metadata
__author__ = 'Jesse P. Johnson'
__title__ = 'proman-github'
__version__ = '0.1.0'
__license__ = 'MPL-2.0'

logging.getLogger(__name__).addHandler(logging.NullHandler())


def get_package_manager(
    token: Optional[str] = os.getenv('GITHUB_TOKEN')
) -> PackageManager:
    '''Get package manager instance.'''
    # Load configuration files
    project_paths = ProjectPaths()
    if os.path.exists(project_paths.pyproject_path):
        source_tree_cfg = Config(
            filepath=project_paths.pyproject_path, writable=True
        )
        print('writable', source_tree_cfg.writable)
        source_tree_file = SourceTreeFile(
            source_tree_cfg, basepath='/tool/proman/github'
        )
        # local_distribution.create_pypackages_pth()
        # local_distribution.load_pypackages()

        if not os.path.exists(project_paths.lock_path):
            lock_cfg = Config(filepath=project_paths.lock_path, writable=True)
            lockfile = LockFile(lock_cfg, basepath='/github')
        else:
            print('err')
    else:
        print('err')

    print(source_tree_cfg)

    manifest: Manifest = Manifest(
        source_tree=source_tree_file,
        lockfile=lockfile,
    )

    # Setup package manager
    return PackageManager(
        github=Github(token),
        dirs=GlobalDirs(),
        manifest=manifest,
        force=False,
        update=False,
        options={}
    )


__all__: List[str] = ['get_package_manager']