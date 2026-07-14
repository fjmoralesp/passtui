import os
import tomlkit
from enum import StrEnum
from pathlib import Path
from platformdirs import user_config_path
from textual.binding import Binding, BindingType

DEFAULT_THEME = "rose-pine-moon"
DEFAULT_PASSWORD_STORE_PATH = Path("~/.password-store")
DEFAULT_CLIP_TIMEOUT = 10
PASSWORD_STORE_ENV_VAR = "PASSWORD_STORE_DIR"


class ViewName(StrEnum):
    HOME = "Home"
    PASSWORDS = "Passwords"
    EDITOR = "Editor"
    SEARCH = "Search"


_DEFAULT_BINDINGS: dict[ViewName, list[dict]] = {
    ViewName.HOME: [
        {
            "action": "search_password",
            "key": "/",
            "description": "Search password",
            "show": False,
        },
        {"action": "add_new_password", "key": "n", "description": "Add new password"},
        {
            "action": "focus_editor",
            "key": "e",
            "description": "Focus editor",
            "show": False,
        },
        {
            "action": "focus_explorer",
            "key": "t",
            "description": "Focus explorer",
            "show": False,
        },
        {"action": "sync", "key": "s", "description": "Sync"},
        {
            "action": "create_gpg_store",
            "key": "g",
            "description": "Create new GPG Store",
            "show": False,
        },
        {
            "action": "export_gpg",
            "key": "x",
            "description": "Export GPG key",
            "show": False,
        },
        {
            "action": "import_gpg",
            "key": "z",
            "description": "Import GPG key",
            "show": False,
        },
    ],
    ViewName.PASSWORDS: [
        {"action": "cursor_down", "key": "j", "description": "Cursor Down"},
        {"action": "cursor_up", "key": "k", "description": "Cursor Up"},
        {"action": "scroll_left", "key": "h", "description": "Scroll left"},
        {"action": "scroll_right", "key": "l", "description": "Scroll right"},
        {"action": "select_cursor", "key": "enter", "description": "Select"},
        {"action": "copy_password", "key": "c", "description": "Copy password"},
        {"action": "copy_username", "key": "b", "description": "Copy username"},
    ],
    ViewName.EDITOR: [
        {
            "action": "cancel",
            "key": "escape",
            "description": "Cancel",
            "priority": True,
        },
        {"action": "insert", "key": "i", "description": "Insert"},
        {"action": "copy_password", "key": "c", "description": "Copy password"},
        {"action": "copy_username", "key": "b", "description": "Copy username"},
        {"action": "copy_current_line", "key": "y", "description": "Copy current line"},
        {"action": "cursor_down", "key": "j", "description": "Cursor Down"},
        {"action": "cursor_up", "key": "k", "description": "Cursor Up"},
        {"action": "cursor_left", "key": "h", "description": "Cursor left"},
        {"action": "cursor_right", "key": "l", "description": "Cursor right"},
        {"action": "save", "key": "ctrl+s", "description": "Save"},
    ],
    ViewName.SEARCH: [
        {"action": "search", "key": "enter", "description": "Search", "priority": True},
        {"action": "cancel", "key": "escape", "description": "Cancel"},
    ],
}


def _build_default_document() -> tomlkit.TOMLDocument:
    document = tomlkit.document()

    general = tomlkit.table()
    general.add("theme", DEFAULT_THEME)
    general.add("password_store_path", str(DEFAULT_PASSWORD_STORE_PATH))
    general.add("clip_timeout", DEFAULT_CLIP_TIMEOUT)
    document.add("general", general)

    keymap = tomlkit.table(is_super_table=True)
    for view_name, binding_defs in _DEFAULT_BINDINGS.items():
        view_table = tomlkit.table()
        for binding_def in binding_defs:
            view_table.add(binding_def["action"], binding_def["key"])
        keymap.add(str(view_name), view_table)
    document.add("keymap", keymap)

    return document


class PassConfig:
    def __init__(self) -> None:
        self._initialization_error: Exception | None = None
        self._config_file_path = self._resolve_config_file_path()
        self._data = self._load_or_create_config()
        self._password_store_path = self._resolve_password_store_path()

    def _resolve_config_file_path(self) -> Path:
        try:
            config_directory = user_config_path("passtui", ensure_exists=True)
            return config_directory / "config.toml"
        except Exception as error:
            self._initialization_error = error
            return Path.home() / ".passtui" / "config.toml"

    def _load_or_create_config(self) -> tomlkit.TOMLDocument:
        try:
            if not self._config_file_path.exists():
                return self._create_default_config()
            return tomlkit.loads(self._config_file_path.read_text())
        except Exception as error:
            self._initialization_error = error
            return _build_default_document()

    def _create_default_config(self) -> tomlkit.TOMLDocument:
        document = _build_default_document()
        self._config_file_path.parent.mkdir(parents=True, exist_ok=True)
        self._config_file_path.write_text(tomlkit.dumps(document))
        return document

    def _resolve_password_store_path(self) -> str:
        try:
            store_path = os.environ.get(PASSWORD_STORE_ENV_VAR)
            if not store_path:
                store_path = self._data.get("general", {}).get(
                    "password_store_path", str(DEFAULT_PASSWORD_STORE_PATH)
                )

            return str(Path(str(store_path)).expanduser())
        except Exception as error:
            self._initialization_error = error
            return str(DEFAULT_PASSWORD_STORE_PATH.expanduser())

    @property
    def password_store_path(self) -> str:
        return self._password_store_path

    @property
    def initialization_error(self) -> Exception | None:
        return self._initialization_error

    @property
    def theme(self) -> str:
        return str(self._data.get("general", {}).get("theme", DEFAULT_THEME))

    @property
    def clip_timeout(self) -> int:
        return int(
            self._data.get("general", {}).get("clip_timeout", DEFAULT_CLIP_TIMEOUT)
        )

    def get_bindings_for(self, view: ViewName) -> list[BindingType]:
        try:
            user_keymap = self._data.get("keymap", {}).get(str(view), {})
            return [
                self._build_binding(binding_def, user_keymap)
                for binding_def in _DEFAULT_BINDINGS.get(view, [])
            ]
        except Exception as error:
            self._initialization_error = error
            return [
                Binding(
                    binding_def["key"],
                    binding_def["action"],
                    binding_def["description"],
                    show=binding_def.get("show", True),
                    priority=binding_def.get("priority", False),
                )
                for binding_def in _DEFAULT_BINDINGS.get(view, [])
            ]

    def _build_binding(self, binding_def: dict, user_keymap: dict) -> Binding:
        action = binding_def["action"]
        key = str(user_keymap.get(action, binding_def["key"]))
        return Binding(
            key,
            action,
            binding_def["description"],
            show=binding_def.get("show", True),
            priority=binding_def.get("priority", False),
        )


pass_config = PassConfig()
