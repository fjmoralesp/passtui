import pytest
from passtui.widgets.pass_data import PassData
from passtui.models.pass_store import PassModel
from textual.app import App, ComposeResult


class AppHelper(App):
    def compose(self) -> ComposeResult:
        yield PassData(id="pass_data")


def test_passdata_init():
    pass_data = PassData()
    assert pass_data._is_dirty == False
    assert pass_data._pass_model is None
    assert pass_data._pass_path is None


@pytest.mark.asyncio
async def test_passdata_set_password():
    app = AppHelper()
    async with app.run_test() as pilot:
        pass_data = app.query_one("#pass_data", PassData)
        pass_model = PassModel("testpass\nUsername: testuser\nURL: test.com")

        pass_data.set_password(pass_model, "test/path")
        assert pass_data._pass_model == pass_model
        assert pass_data._pass_path == "test/path"


@pytest.mark.asyncio
async def test_passdata_add_new_password():
    app = AppHelper()
    async with app.run_test() as pilot:
        pass_data = app.query_one("#pass_data", PassData)
        pass_data.add_new_password()
        assert pass_data._is_dirty == True
        assert pass_data._pass_model is not None


@pytest.mark.asyncio
async def test_passdata_copy_password():
    app = AppHelper()
    async with app.run_test() as pilot:
        pass_data = app.query_one("#pass_data", PassData)
        pass_data.action_copy_password()


@pytest.mark.asyncio
async def test_passdata_copy_username():
    app = AppHelper()
    async with app.run_test() as pilot:
        pass_data = app.query_one("#pass_data", PassData)
        pass_data.action_copy_username()


@pytest.mark.asyncio
async def test_passdata_copy_current_line():
    app = AppHelper()
    async with app.run_test() as pilot:
        pass_data = app.query_one("#pass_data", PassData)
        pass_data.action_copy_current_line()


@pytest.mark.asyncio
async def test_passdata_save():
    app = AppHelper()
    async with app.run_test() as pilot:
        pass_data = app.query_one("#pass_data", PassData)
        pass_data.action_save()
