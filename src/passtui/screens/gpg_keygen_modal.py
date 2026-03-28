from typing import NamedTuple

from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Grid, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Input, Label, Button


class GpgKeyData(NamedTuple):
    name: str
    email: str
    path: str | None


class GpgKeygenModalScreen(ModalScreen[GpgKeyData | None]):
    BINDINGS = [
        Binding("enter", "submit", "Submit", priority=True),
        Binding("escape", "cancel", "Cancel"),
    ]

    DEFAULT_CSS = """
    GpgKeygenModalScreen {
        align: center middle;
    }
    GpgKeygenModalScreen Grid {
        grid-size: 2;
        grid-gutter: 1 2;
        padding: 1 2;
        width: 84;
        height: 19;
        border: tall $primary;
        border-title-color: $primary;
        border-title-align: center;
        background: $surface;
    }
    GpgKeygenModalScreen Horizontal {
        column-span: 2;
        border: tall $surface-lighten-2;
        padding: 0 1;
    }
    GpgKeygenModalScreen Horizontal Label {
        margin: 0 1 0 0;
        color: $text-muted;
    }
    GpgKeygenModalScreen Button {
        width: 1fr;
        height: 1fr;
    }
    """

    def compose(self) -> ComposeResult:
        with Grid(id="modal-grid"):
            with Horizontal():
                yield Label("Enter your name:")
                yield Input(
                    placeholder="(e.g., name)",
                    id="name",
                    compact=True,
                )
            with Horizontal():
                yield Label("Enter your email:")
                yield Input(
                    placeholder="(e.g., name@email.com)",
                    id="email",
                    compact=True,
                )
            with Horizontal():
                yield Label("Password Store path (optional):")
                yield Input(
                    placeholder="(e.g., my-passwords/emails/gmail) ",
                    id="path",
                    compact=True,
                )
            yield Button("(Enter) Submit", variant="primary", id="submit")
            yield Button("(Esc) Cancel", variant="error", id="cancel")

    def on_mount(self) -> None:
        self.query_one("#modal-grid").border_title = " Generate GPG Key "

    @on(Button.Pressed, "#submit")
    async def handle_button_submit(self) -> None:
        self.action_submit()

    @on(Button.Pressed, "#cancel")
    async def handle_button_cancel(self) -> None:
        self.action_cancel()

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
