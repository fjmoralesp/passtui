import threading
import pyperclip

from rich.text import Text
from passtui.models.pass_store import PassModel

CLIP_TTL = 10

_active_timer: threading.Timer | None = None


def _copy_with_ttl(value: str) -> bool:
    global _active_timer
    try:
        if _active_timer:
            _active_timer.cancel()
        pyperclip.copy(value)
        _active_timer = threading.Timer(CLIP_TTL, lambda: pyperclip.copy(""))
        _active_timer.start()
        return True
    except Exception:
        return False


def copy_username_to_clipboard(pass_model: PassModel | None) -> bool:
    if not pass_model:
        return False

    if not pass_model.username:
        return False

    return _copy_with_ttl(pass_model.username)


def copy_password_to_clipboard(pass_model: PassModel | None) -> bool:
    if not pass_model:
        return False

    if not pass_model.password:
        return False

    return _copy_with_ttl(pass_model.password)


def copy_line_to_clipboard(line: Text) -> bool:
    return _copy_with_ttl(str(line))
