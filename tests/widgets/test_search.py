import pytest
from passtui.widgets.search import Search
from textual.app import App, ComposeResult
from textual.widgets import Static


class AppHelper(App):
    def compose(self) -> ComposeResult:
        yield Search(data=["test1", "test2", "other"], id="search")


@pytest.mark.asyncio
async def test_search_initial_state():
    app = AppHelper()
    async with app.run_test() as pilot:
        search = app.query_one("#search", Search)
        assert search.data == ["test1", "test2", "other"]
        assert search.results == ["test1", "test2", "other"]


@pytest.mark.asyncio
async def test_search_filtering():
    app = AppHelper()
    async with app.run_test() as pilot:
        search = app.query_one("#search", Search)

        await pilot.press("t")
        assert search.results == ["test1", "test2", "other"]

        await pilot.press("e")
        assert search.results == ["test1", "test2"]

        await pilot.press("1")
        assert search.results == []

        await pilot.press("backspace")
        await pilot.press("backspace")
        await pilot.press("backspace")
        assert search.results == ["test1", "test2", "other"]

        await pilot.press("t")
        await pilot.press("e")
        await pilot.press("s")
        await pilot.press("t")
        assert search.results == [
            "test1",
            "test2",
        ]


@pytest.mark.asyncio
async def test_search_case_insensitive():
    app = AppHelper()
    async with app.run_test() as pilot:
        search = app.query_one("#search", Search)

        await pilot.press("T")
        await pilot.press("E")
        await pilot.press("S")
        await pilot.press("T")
        assert search.results == ["test1", "test2"]


@pytest.mark.asyncio
async def test_search_actions():
    app = AppHelper()
    async with app.run_test() as pilot:
        search = app.query_one("#search", Search)

        search.action_search()

        search._input.value = "test"
        search.action_cancel()
        assert search._input.value == ""
