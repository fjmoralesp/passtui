from typing import NamedTuple

from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Grid, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Input, Label, Button


class GpgExportData(NamedTuple):
    passphrase: str
    output_path: str | None


class GpgExportModalScreen(ModalScreen[GpgExportData | None]):
    """
    This only works for GPG keys that were created with passtui,
    where we use only one GPG key per store.
    """

    BINDINGS = [
        Binding("enter", "submit", "Submit", priority=True),
        Binding("escape", "cancel", "Cancel"),
    ]

    DEFAULT_CSS = """
    GpgExportModalScreen {
        align: center middle;
    }
    GpgExportModalScreen Grid {
        column-span: 2;
        grid-size: 2;
        grid-gutter: 0 2;
        padding: 0 2;
        width: 80;
        height: 11;
        border: thick $background 80%;
        background: $surface;
    }
    GpgExportModalScreen Horizontal {
        column-span: 2;
        border: solid $primary-muted;
    }
    GpgExportModalScreen Horizontal Label {
        margin: 0 1 0 0;
    }
    GpgExportModalScreen Button {
        width: 1fr;
        height: 1fr;
    }
    """

    def compose(self) -> ComposeResult:
        with Grid():
            with Horizontal():
                yield Label("Enter GPG key passphrase:")
                yield Input(
                    placeholder="(e.g., password)",
                    id="passphrase",
                    password=True,
                    compact=True,
                )
            with Horizontal():
                yield Label("Output file path (optional):")
                yield Input(
                    placeholder="(defaults: ~/passtui/gpg-export.asc)",
                    id="output",
                    compact=True,
                )
            yield Button("(Enter) Submit", variant="primary", id="submit")
            yield Button("(Esc) Cancel", variant="error", id="cancel")

    @on(Button.Pressed, "#submit")
    async def handle_button_submit(self) -> None:
        self.action_submit()

    @on(Button.Pressed, "#cancel")
    async def handle_button_cancel(self) -> None:
        self.action_cancel()

    def action_submit(self) -> None:
        passphrase = self.query_one("#passphrase", Input).value
        output = self.query_one("#output", Input).value
        if passphrase:
            self.dismiss(
                GpgExportData(
                    passphrase=passphrase, output_path=output if output else None
                )
            )
        else:
            self.notify("Passphrase is required", severity="error")

    def action_cancel(self) -> None:
        self.dismiss(None)
