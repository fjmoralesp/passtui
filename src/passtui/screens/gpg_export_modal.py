from typing import NamedTuple

from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Input


class GpgExportData(NamedTuple):
    passphrase: str
    output_path: str | None


class GpgExportModalScreen(Screen[GpgExportData | None]):
    """
    This only works for GPG keys that were created with passtui,
    where we use only one GPG key per store.
    """

    BINDINGS = [
        Binding("enter", "submit", "Submit", priority=True),
        Binding("escape", "cancel", "Cancel"),
    ]

    def compose(self) -> ComposeResult:
        yield Input(
            placeholder="Enter passphrase associated with GPG key",
            id="passphrase",
            password=True,
        )
        yield Input(
            placeholder="Output file path (optional, default: ~/passtui/gpg-export.asc)",
            id="output",
        )

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
