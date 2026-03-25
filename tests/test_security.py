from unittest.mock import Mock, patch, mock_open
from passtui.security import PassCLI, passcli
from pathlib import Path


def test_passcli_init():
    cli = PassCLI()
    assert hasattr(cli, "_store")
    assert hasattr(cli, "_gpg")


def test_get_store_key():
    cli = PassCLI()
    with patch.object(cli._store, "get_key", return_value=None):
        result = cli.get_store_key("test/path")
        assert result is None

    mock_key_data = Mock()
    with patch.object(cli._store, "get_key", return_value=mock_key_data):
        with patch("passtui.security.PassModel") as mock_pass_model:
            mock_pass_model.return_value = "mock_model"
            result = cli.get_store_key("test/path")
            assert result == "mock_model"


def test_save_store_key():
    cli = PassCLI()
    pass_model = Mock()

    with patch.object(cli._store, "set_key") as mock_set_key:
        cli.save_store_key("test/path", pass_model)
        mock_set_key.assert_called_once_with("test/path", str(pass_model), force=True)


def test_list_keys():
    cli = PassCLI()
    with patch.object(cli._store, "is_init", return_value=False):
        result = cli.list_keys()
        assert result == []

    with patch.object(cli._store, "is_init", return_value=True):
        mock_store = Mock()
        mock_store.__iter__ = Mock(return_value=iter(["key1", "key2"]))
        with patch.object(cli, "_store", mock_store):
            result = cli.list_keys()
            assert set(result) == {"key1", "key2"}


def test_is_git_initialized():
    cli = PassCLI()
    with patch.object(cli._store, "repo", None):
        assert cli.is_git_initialized() == False

    with patch.object(cli._store, "repo", Mock()):
        assert cli.is_git_initialized() == True


@patch("passtui.security.passcli")
def test_init_git_already_initialized(mock_passcli):
    mock_passcli.is_git_initialized.return_value = True

    passcli.init_git("test/repo")

    mock_passcli._store.init_git.assert_not_called()
    mock_passcli._store.git.assert_not_called()


def test_init_git_not_initialized():
    with patch.object(passcli, "is_git_initialized", return_value=False):
        with patch.object(passcli._store, "init_git") as mock_init_git:
            with patch.object(passcli._store, "git") as mock_git:
                passcli.init_git("test/repo")
                mock_init_git.assert_called_once()
                mock_git.assert_any_call("remote", "add", "origin", "test/repo")
                mock_git.assert_any_call("push", "origin", "master")


def test_sync_git_not_initialized():
    cli = PassCLI()
    with patch.object(cli, "is_git_initialized", return_value=False):
        cli.sync_git()


def test_sync_git_initialized():
    cli = PassCLI()
    with patch.object(cli, "is_git_initialized", return_value=True):
        with patch.object(cli._store, "git") as mock_git:
            cli.sync_git()
            mock_git.assert_any_call("pull", "--rebase")
            mock_git.assert_any_call("push")


def test_create_gpg_store_already_initialized():
    cli = PassCLI()
    with patch.object(cli._store, "is_init", return_value=True):
        result = cli.create_gpg_store("Test", "test@example.com")
        assert result is None


def test_create_gpg_store_not_initialized():
    cli = PassCLI()
    with patch.object(cli._store, "is_init", return_value=False):
        mock_input_data = Mock()
        mock_key = Mock()
        mock_key.fingerprint = "test-fingerprint"

        with patch.object(cli._gpg, "gen_key_input", return_value=mock_input_data):
            with patch.object(cli._gpg, "gen_key", return_value=mock_key):
                with patch.object(cli._store, "init_store") as mock_init_store:
                    result = cli.create_gpg_store(
                        "Test", "test@example.com", "/test/path"
                    )
                    assert result == "test-fingerprint"
                    mock_init_store.assert_called_once_with(
                        "test-fingerprint", "/test/path"
                    )


def test_export_gpg_key_not_initialized():
    cli = PassCLI()
    with patch.object(cli._store, "is_init", return_value=False):
        result = cli.export_gpg_key("testpass")
        assert result is None


def test_export_gpg_key_no_output_path():
    cli = PassCLI()
    with patch.object(cli._store, "is_init", return_value=True):
        with patch("passtui.security._get_gpg_recipients", return_value=["key1"]):
            with patch.object(cli._gpg, "export_keys", return_value="keydata"):
                with patch("pathlib.Path.home") as mock_home:
                    mock_home.return_value = Path("/home/test")
                    with patch("pathlib.Path.mkdir"):
                        with patch("builtins.open", mock_open()) as mock_file:
                            with patch(
                                "pathlib.Path.expanduser",
                                return_value=Path("/home/test/passtui/gpg-export.asc"),
                            ):
                                result = cli.export_gpg_key("testpass")
                                assert result is not None
                                assert "gpg-export.asc" in result


def test_import_gpg_key_not_initialized():
    cli = PassCLI()
    with patch.object(cli._store, "is_init", return_value=False):
        result = cli.import_gpg_key("/test/key.asc")
        assert result is False


def test_import_gpg_key_no_keys():
    cli = PassCLI()
    with patch.object(cli._store, "is_init", return_value=True):
        with patch.object(cli, "list_keys", return_value=[]):
            with patch("pathlib.Path.exists", return_value=True):
                with patch.object(cli._gpg, "import_keys_file") as mock_import:
                    mock_result = Mock()
                    mock_result.fingerprints = None
                    mock_import.return_value = mock_result
                    result = cli.import_gpg_key("/test/key.asc")
                    assert result is False
