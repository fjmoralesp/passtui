from typing import NamedTuple

from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Input


class GpgKeyData(NamedTuple):
    name: str
    email: str
    path: str | None


class GpgKeygenModalScreen(Screen[GpgKeyData | None]):
    BINDINGS = [
        Binding("enter", "submit", "Submit", priority=True),
        Binding("escape", "cancel", "Cancel"),
    ]

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Enter your name", id="name")
        yield Input(placeholder="Enter your email", id="email")
        yield Input(placeholder="Optional store path", id="path")

    def action_submit(self) -> None:
        name = self.query_one("#name", Input).value
        email = self.query_one("#email", Input).value
        path = self.query_one("#path", Input).value
        if name and email:
            self.dismiss(
                GpgKeyData(name=name, email=email, path=path if path else None)
            )
        else:
            self.notify("Name and email are required", severity="error")

    def action_cancel(self) -> None:
        self.dismiss(None)
