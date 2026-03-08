from textual.app import ComposeResult
from textual.screen import Screen
from textual.binding import Binding
from textual.widgets import Label
from passtui.security import passcli


class AuthScreen(Screen[bool]):
    CSS_PATH = "auth.tcss"

    BINDINGS = [
        Binding("ctrl+u", "unlock", "Unlock"),
    ]

    def compose(self) -> ComposeResult:
        yield Label("Press Ctrl+U to unlock your GPG key. 🔐")

    def action_unlock(self) -> None:
        is_unlocked = passcli.unlock()
        if not is_unlocked:
            return

        self.notify("Your GPG key is unlocked! 🔓", severity="information")
        self.dismiss(True)
