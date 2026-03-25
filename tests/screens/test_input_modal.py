import pytest
from passtui.screens.input_modal import InputModalScreen
from textual.app import App, ComposeResult
from textual.widgets import Static


class AppHelper(App):
    def compose(self) -> ComposeResult:
        yield Static()


@pytest.mark.asyncio
async def test_input_modal_submit():
    app = AppHelper()
    async with app.run_test() as pilot:
        modal = InputModalScreen(label="Test", placeholder="Enter value")
        app.push_screen(modal)

        await pilot.pause()

        await pilot.press("t")
        await pilot.press("e")
        await pilot.press("s")
        await pilot.press("t")
        await pilot.press("enter")


@pytest.mark.asyncio
async def test_input_modal_cancel():
    app = AppHelper()
    async with app.run_test() as pilot:
        modal = InputModalScreen(label="Test", placeholder="Enter value")
        app.push_screen(modal)

        await pilot.pause()

        await pilot.press("escape")


@pytest.mark.asyncio
async def test_input_modal_empty_submit():
    app = AppHelper()
    async with app.run_test() as pilot:
        modal = InputModalScreen(label="Test", placeholder="Enter value")
        app.push_screen(modal)

        await pilot.pause()

        await pilot.press("enter")
