import pytest
from passtui.screens.gpg_export_modal import GpgExportModalScreen
from textual.app import App, ComposeResult
from textual.widgets import Static


class AppWrapper(App):
    def compose(self) -> ComposeResult:
        yield Static()


@pytest.mark.asyncio
async def test_gpg_export_modal_submit():
    app = AppWrapper()
    async with app.run_test() as pilot:
        modal = GpgExportModalScreen()
        app.push_screen(modal)

        await pilot.pause()

        await pilot.press("p")
        await pilot.press("a")
        await pilot.press("s")
        await pilot.press("s")
        await pilot.press("w")
        await pilot.press("o")
        await pilot.press("r")
        await pilot.press("d")
        await pilot.press("tab")
        await pilot.press("o")
        await pilot.press("u")
        await pilot.press("t")
        await pilot.press("p")
        await pilot.press("u")
        await pilot.press("t")
        await pilot.press("enter")


@pytest.mark.asyncio
async def test_gpg_export_modal_submit_missing_passphrase():
    app = AppWrapper()
    async with app.run_test() as pilot:
        modal = GpgExportModalScreen()
        app.push_screen(modal)

        await pilot.pause()

        await pilot.press("enter")


@pytest.mark.asyncio
async def test_gpg_export_modal_cancel():
    app = AppWrapper()
    async with app.run_test() as pilot:
        modal = GpgExportModalScreen()
        app.push_screen(modal)

        await pilot.pause()

        await pilot.press("escape")
