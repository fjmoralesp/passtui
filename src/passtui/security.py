import os
import subprocess
import secrets

import passpy

from passpy.gpg import GPG, _get_gpg_recipients, reencrypt_path
from passpy.git import git_add_path
from pathlib import Path
from passtui.models.pass_store import PassModel


class PassCLI:
    def __init__(self):
        self._store = passpy.Store()
        self._gpg = GPG(gpgbinary=self._store.gpg_bin, options=self._store.gpg_opts)

    def get_store_key(self, key: str) -> PassModel | None:
        key_data = self._store.get_key(key)
        return PassModel(key_data) if key_data else None

    def save_store_key(self, path: str, pass_model: PassModel) -> None:
        self._store.set_key(path, str(pass_model), force=True)

    def list_keys(self) -> list[str]:
        if not self._store.is_init():
            return []
        return list(self._store)

    def is_git_initialized(self) -> bool:
        return self._store.repo is not None

    def init_git(self, repo_url: str) -> None:
        """
        This method is intended for new stores only.
        Stores that were previously created in the repository will cause an error and will not sync.
        """
        if self.is_git_initialized():
            return

        self._store.init_git()
        self._store.git("remote", "add", "origin", repo_url)
        self._store.git("push", "origin", "HEAD")

    def sync_git(self) -> None:
        if not self.is_git_initialized():
            return

        self._store.git("pull", "--rebase", "origin", "HEAD")
        self._store.git("push", "origin", "HEAD")

    def create_gpg_store(self, name: str, email: str, path=None) -> str | None:
        """
        This method creates a GPG key and a store in the provided path. If no path is provided,
        it will use the default store path "~/.password-store" or the "PASSWORD_STORE_DIR"
        environment variable.

        If the path already has a initialired Store, it will configure the new GPG key created and
        then reencrypt all the existing entries.
        """
        if self._store.is_init():
            return

        input_data = self._gpg.gen_key_input(
            name_real=name,
            name_email=email,
            key_type="RSA",
            key_length=4096,
            expire_date="0",
        )

        key = self._gpg.gen_key(input_data)
        self._store.init_store(key.fingerprint, path)
        return key.fingerprint if key else None

    def export_gpg_key(
        self, passphrase: str, output_path: str | None = None
    ) -> str | None:
        """
        This method exports the GPG key associated with the store. The store must be initialised and
        it should have only one GPG key.
        """
        if not self._store.is_init():
            return

        if output_path is None:
            export_dir = Path.home() / "passtui"
            export_dir.mkdir(exist_ok=True)
            output_path = str(export_dir / "gpg-export.asc")
        else:
            output_path = str(Path(output_path).expanduser())
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        keys = _get_gpg_recipients(self._store.store_dir)
        keys_data = self._gpg.export_keys(keys, passphrase=passphrase, secret=True)
        if not keys_data:
            return
        with open(output_path, "w") as f:
            f.write(keys_data)
        return output_path

    def import_gpg_key(self, file_path: str) -> bool:
        """
        Import a GPG key and use it to re-encrypt the password store.
        """
        if not self._store.is_init():
            return False

        input_path = str(Path(file_path).expanduser())
        results = self._gpg.import_keys_file(input_path)

        gpg_ids = results.fingerprints
        if gpg_ids is None:
            return False
        if not isinstance(gpg_ids, list):
            gpg_ids = [gpg_ids]

        gpg_ids = list(dict.fromkeys(gpg_ids))
        current_ids = _get_gpg_recipients(self._store.store_dir)
        key_names = self.list_keys()
        if not key_names:
            return False

        # Unlock the password store
        try:
            key = self.get_store_key(key_names[0])
            if not key:
                return False
        except Exception:
            return False

        # Make the new key trusted
        try:
            self._gpg.trust_keys(gpg_ids, "TRUST_ULTIMATE")
        except Exception:
            return False

        # Update .gpg-id
        all_keys = list(dict.fromkeys(current_ids + gpg_ids))
        gpg_id_path = os.path.join(self._store.store_dir, ".gpg-id")
        with open(gpg_id_path, "w") as gpg_id_file:
            gpg_id_file.write("\n".join(all_keys))
            gpg_id_file.write("\n")

        git_add_path(
            self._store.repo,
            gpg_id_path,
            f"Set GPG id to {', '.join(all_keys)}. [{secrets.token_hex(4)}]",
            verbose=False,
        )

        # once the newly imported key is trusted, we need to reencrypt the store.
        # All the fingerprints listed in the in .gpg-id file need to be signed
        reencrypt_path(
            self._store.store_dir,
            gpg_bin=self._store.gpg_bin,
            gpg_opts=self._store.gpg_opts,
        )

        git_add_path(
            self._store.repo,
            self._store.store_dir,
            f"Reencrypt password store using new GPG id {', '.join(all_keys)}. [{secrets.token_hex(4)}]",
            verbose=False,
        )

        return results.count > 0


passcli = PassCLI()
