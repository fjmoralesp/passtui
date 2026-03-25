import pytest
from passtui.screens.gpg_keygen_modal import GpgKeygenModalScreen
from textual.app import App, ComposeResult
from textual.widgets import Static


class AppWrapper(App):
    def compose(self) -> ComposeResult:
        yield Static()


@pytest.mark.asyncio
async def test_gpg_keygen_modal_submit():
    app = AppWrapper()
    async with app.run_test() as pilot:
        modal = GpgKeygenModalScreen()
        app.push_screen(modal)

        await pilot.pause()

        await pilot.press("t")
        await pilot.press("e")
        await pilot.press("s")
        await pilot.press("t")
        await pilot.press("tab")
        await pilot.press("t")
        await pilot.press("e")
        await pilot.press("s")
        await pilot.press("t")
        await pilot.press("@")
        await pilot.press("e")
        await pilot.press("x")
        await pilot.press("a")
        await pilot.press("m")
        await pilot.press("p")
        await pilot.press("l")
        await pilot.press("e")
        await pilot.press(".")
        await pilot.press("c")
        await pilot.press("o")
        await pilot.press("m")
        await pilot.press("tab")
        await pilot.press("p")
        await pilot.press("a")
        await pilot.press("t")
        await pilot.press("h")
        await pilot.press("enter")


@pytest.mark.asyncio
async def test_gpg_keygen_modal_submit_missing_fields():
    app = AppWrapper()
    async with app.run_test() as pilot:
        modal = GpgKeygenModalScreen()
        app.push_screen(modal)

        await pilot.pause()

        await pilot.press("t")
        await pilot.press("e")
        await pilot.press("s")
        await pilot.press("t")
        await pilot.press("enter")


@pytest.mark.asyncio
async def test_gpg_keygen_modal_cancel():
    app = AppWrapper()
    async with app.run_test() as pilot:
        modal = GpgKeygenModalScreen()
        app.push_screen(modal)

        await pilot.pause()

        await pilot.press("escape")
