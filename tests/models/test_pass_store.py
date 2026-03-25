from passtui.models.pass_store import PassModel


def test_pass_model_init_with_none():
    model = PassModel(None)
    assert model.password == ""
    assert model.username == ""
    assert model.url == ""
    assert model.meta == []
    assert model._raw_data == ""


def test_pass_model_init_with_empty_string():
    model = PassModel("")
    assert model.password == ""
    assert model.username == ""
    assert model.url == ""
    assert model.meta == []
    assert model._raw_data == ""


def test_pass_model_init_with_password_only():
    model = PassModel("mypassword")
    assert model.password == "mypassword"
    assert model.username == ""
    assert model.url == ""
    assert model.meta == []
    assert model._raw_data == "mypassword"


def test_pass_model_init_with_password_and_username():
    model = PassModel("mypassword\nUsername: myuser")
    assert model.password == "mypassword"
    assert model.username == "myuser"
    assert model.url == ""
    assert model.meta == []
    assert model._raw_data == "mypassword\nUsername: myuser"


def test_pass_model_init_with_all_fields():
    data = "mypassword\nUsername: myuser\nURL: https://example.com\nExtra: metadata"
    model = PassModel(data)
    assert model.password == "mypassword"
    assert model.username == "myuser"
    assert model.url == "https://example.com"
    assert model.meta == ["Extra: metadata"]
    assert model._raw_data == data


def test_pass_model_str():
    data = "mypassword\nUsername: myuser\nURL: https://example.com"
    model = PassModel(data)
    assert str(model) == data


def test_pass_model_get_new_entry_template():
    model, template = PassModel.get_new_entry_template()

    assert isinstance(model, PassModel)
    assert isinstance(template, str)

    assert "(add your password here)" in template

    assert model.password == "(add your password here)"
