from typing import Optional, Iterator
from git.repo.base import Repo

class Store:
    gpg_bin: str
    git_bin: str
    gpg_opts: list[str]
    store_dir: str
    repo: Optional[Repo]
    interactive: bool
    verbose: bool

    def __init__(
        self,
        gpg_bin: str = ...,
        git_bin: str = ...,
        store_dir: str = ...,
        use_agent: bool = ...,
        interactive: bool = ...,
        verbose: bool = ...,
    ) -> None: ...
    def __iter__(self) -> Iterator[str]: ...
    def is_init(self) -> bool: ...
    def init_store(self, gpg_ids: list[str], path: Optional[str] = None) -> None: ...
    def init_git(self) -> None: ...
    def git(self, method: str, *args: str, **kwargs: str) -> Optional[str]: ...
    def get_key(self, path: str) -> Optional[str]: ...
    def set_key(self, path: str, key_data: str, force: bool = False) -> None: ...
