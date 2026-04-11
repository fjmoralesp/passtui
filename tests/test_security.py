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
                mock_git.assert_any_call("push", "origin", "HEAD")


def test_sync_git_not_initialized():
    cli = PassCLI()
    with patch.object(cli, "is_git_initialized", return_value=False):
        cli.sync_git()


def test_sync_git_initialized():
    cli = PassCLI()
    with patch.object(cli, "is_git_initialized", return_value=True):
        with patch.object(cli._store, "git") as mock_git:
            cli.sync_git()
            mock_git.assert_any_call("pull", "--rebase", "origin", "HEAD")
            mock_git.assert_any_call("push", "origin", "HEAD")


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
        result = cli.export_gpg_key()
        assert result is None


def test_export_gpg_key_no_output_path():
    cli = PassCLI()
    with patch.object(cli._store, "is_init", return_value=True):
        with patch("passtui.security._get_gpg_recipients", return_value=["key1"]):
            with patch.object(cli._gpg, "export_keys") as mock_export:
                with patch("pathlib.Path.home") as mock_home:
                    mock_home.return_value = Path("/home/test")
                    with patch("pathlib.Path.mkdir"):
                        result = cli.export_gpg_key()
                        assert result is not None
                        assert "gpg-export.asc" in result
                        mock_export.assert_called_once()
                        _, kwargs = mock_export.call_args
                        assert kwargs.get("secret") is True
                        assert kwargs.get("expect_passphrase") is False


def test_export_gpg_key_invalid_extension():
    cli = PassCLI()
    with patch.object(cli._store, "is_init", return_value=True):
        with patch("pathlib.Path.home") as mock_home:
            mock_home.return_value = Path("/home/test")
            with patch(
                "pathlib.Path.expanduser", return_value=Path("/home/test/key.txt")
            ):
                with patch(
                    "pathlib.Path.resolve", return_value=Path("/home/test/key.txt")
                ):
                    try:
                        cli.export_gpg_key("/home/test/key.txt")
                        assert False, "Expected ValueError"
                    except ValueError as e:
                        assert ".asc" in str(e)


def test_export_gpg_key_valid_custom_path():
    cli = PassCLI()
    with patch.object(cli._store, "is_init", return_value=True):
        with patch("passtui.security._get_gpg_recipients", return_value=["key1"]):
            with patch.object(cli._gpg, "export_keys") as mock_export:
                with patch("pathlib.Path.home") as mock_home:
                    mock_home.return_value = Path("/home/test")
                    with patch(
                        "pathlib.Path.expanduser",
                        return_value=Path("/home/test/my-key.asc"),
                    ):
                        with patch(
                            "pathlib.Path.resolve",
                            return_value=Path("/home/test/my-key.asc"),
                        ):
                            with patch("pathlib.Path.mkdir"):
                                result = cli.export_gpg_key("/home/test/my-key.asc")
                                assert result is not None
                                assert "my-key.asc" in result
                                mock_export.assert_called_once()


def test_import_gpg_key_not_initialized():
    cli = PassCLI()
    with patch.object(cli._store, "is_init", return_value=False):
        result = cli.import_gpg_key("/test/key.asc")
        assert result is False


def test_import_gpg_key_fingerprints_none():
    cli = PassCLI()
    with patch.object(cli._store, "is_init", return_value=True):
        with patch("pathlib.Path.home") as mock_home:
            mock_home.return_value = Path("/home/test")
            with patch(
                "pathlib.Path.expanduser", return_value=Path("/home/test/key.asc")
            ):
                with patch(
                    "pathlib.Path.resolve", return_value=Path("/home/test/key.asc")
                ):
                    with patch.object(cli._gpg, "import_keys_file") as mock_import:
                        mock_result = Mock()
                        mock_result.fingerprints = None
                        mock_import.return_value = mock_result
                        result = cli.import_gpg_key("/home/test/key.asc")
                        assert result is False


def test_import_gpg_key_no_signer():
    cli = PassCLI()
    with patch.object(cli._store, "is_init", return_value=True):
        with patch("pathlib.Path.home") as mock_home:
            mock_home.return_value = Path("/home/test")
            with patch(
                "pathlib.Path.expanduser", return_value=Path("/home/test/key.asc")
            ):
                with patch(
                    "pathlib.Path.resolve", return_value=Path("/home/test/key.asc")
                ):
                    with patch.object(cli._gpg, "import_keys_file") as mock_import:
                        mock_result = Mock()
                        mock_result.fingerprints = ["AAAA1111"]
                        mock_import.return_value = mock_result
                        with patch(
                            "passtui.security._get_gpg_recipients", return_value=[]
                        ):
                            with patch.object(
                                cli, "_ensure_signing_key", return_value=None
                            ):
                                result = cli.import_gpg_key("/home/test/key.asc")
                                assert result is False


def test_import_gpg_key_success():
    cli = PassCLI()
    with patch.object(cli._store, "is_init", return_value=True):
        with patch("pathlib.Path.home") as mock_home:
            mock_home.return_value = Path("/home/test")
            with patch(
                "pathlib.Path.expanduser", return_value=Path("/home/test/key.asc")
            ):
                with patch(
                    "pathlib.Path.resolve", return_value=Path("/home/test/key.asc")
                ):
                    with patch.object(cli._gpg, "import_keys_file") as mock_import:
                        mock_result = Mock()
                        mock_result.fingerprints = ["AAAA1111"]
                        mock_result.count = 1
                        mock_import.return_value = mock_result
                        with patch(
                            "passtui.security._get_gpg_recipients",
                            return_value=["BBBB2222"],
                        ):
                            with patch.object(
                                cli, "_ensure_signing_key", return_value="BBBB2222"
                            ):
                                with patch.object(cli._gpg, "trust_keys"):
                                    with patch("passtui.security.subprocess.run"):
                                        with patch("builtins.open", mock_open()):
                                            with patch("passtui.security.git_add_path"):
                                                with patch(
                                                    "passtui.security.reencrypt_path"
                                                ):
                                                    with patch.object(
                                                        cli._store,
                                                        "store_dir",
                                                        "/home/test/.password-store",
                                                    ):
                                                        with patch.object(
                                                            cli._store, "repo", Mock()
                                                        ):
                                                            result = cli.import_gpg_key(
                                                                "/home/test/key.asc"
                                                            )
                                                            assert result is True


def test_generate_gpg_key():
    cli = PassCLI()
    mock_input_data = Mock()
    mock_key = Mock()
    mock_key.fingerprint = "DEADBEEF"
    with patch.object(
        cli._gpg, "gen_key_input", return_value=mock_input_data
    ) as mock_input:
        with patch.object(cli._gpg, "gen_key", return_value=mock_key):
            result = cli._generate_gpg_key("Test User", "test@example.com")
            assert result == "DEADBEEF"
            mock_input.assert_called_once_with(
                name_real="Test User",
                name_email="test@example.com",
                key_type="RSA",
                key_length=4096,
                expire_date="0",
            )


def test_generate_gpg_key_failure():
    cli = PassCLI()
    mock_input_data = Mock()
    with patch.object(cli._gpg, "gen_key_input", return_value=mock_input_data):
        with patch.object(cli._gpg, "gen_key", return_value=None):
            result = cli._generate_gpg_key("Test User", "test@example.com")
            assert result is None


def test_get_ultimate_signing_key_found():
    cli = PassCLI()
    gpg_output = "sec:u:4096:1:AABBCCDD1234::\nfpr:::::::::AABBCCDD1234FINGERPRINT:\n"
    mock_result = Mock()
    mock_result.stdout = gpg_output
    with patch("passtui.security.subprocess.run", return_value=mock_result):
        result = cli._get_ultimate_signing_key()
        assert result == "AABBCCDD1234FINGERPRINT"


def test_get_ultimate_signing_key_not_found():
    cli = PassCLI()
    gpg_output = "sec:e:4096:1:AABBCCDD1234::\nfpr:::::::::AABBCCDD1234FINGERPRINT:\n"
    mock_result = Mock()
    mock_result.stdout = gpg_output
    with patch("passtui.security.subprocess.run", return_value=mock_result):
        result = cli._get_ultimate_signing_key()
        assert result is None


def test_ensure_signing_key_uses_existing():
    cli = PassCLI()
    with patch.object(cli, "_get_ultimate_signing_key", return_value="EXISTINGKEY"):
        result = cli._ensure_signing_key()
        assert result == "EXISTINGKEY"


def test_ensure_signing_key_generates_new():
    cli = PassCLI()
    with patch.object(cli, "_get_ultimate_signing_key", return_value=None):
        with patch.object(cli, "_generate_gpg_key", return_value="NEWKEY") as mock_gen:
            result = cli._ensure_signing_key()
            assert result == "NEWKEY"
            mock_gen.assert_called_once_with("PassTUI", "passtui@local.com")
