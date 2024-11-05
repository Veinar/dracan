import json
import pytest
from dracan.utils.config_load import load_proxy_config, load_rules_config, check_required_files

@pytest.fixture
def setup_default_config(tmp_path):
    """
    Fixture to set up default configuration files in a temporary directory.
    """
    # Create default config files in the temporary directory
    proxy_config = tmp_path / "proxy_config.json"
    rules_config = tmp_path / "rules_config.json"
    proxy_config.write_text('{"destination": {"host": "127.0.0.1", "port": 8080, "path": "/"}}')
    rules_config.write_text('{"allowed_methods": ["GET", "POST"], "rate_limit": "10 per minute"}')

    return tmp_path

@pytest.fixture
def setup_custom_config(tmp_path):
    """
    Fixture to set up configuration files in a custom directory.
    """
    # Create a custom config directory and files
    custom_config_dir = tmp_path / "custom_config"
    custom_config_dir.mkdir()
    proxy_config = custom_config_dir / "proxy_config.json"
    rules_config = custom_config_dir / "rules_config.json"
    proxy_config.write_text('{"destination": {"host": "127.0.0.1", "port": 8080, "path": "/"}}')
    rules_config.write_text('{"allowed_methods": ["GET", "POST"], "rate_limit": "10 per minute"}')

    return custom_config_dir

def test_load_default_config(setup_default_config, monkeypatch):
    """
    Test loading configuration from the default location.
    """
    monkeypatch.chdir(setup_default_config)  # Change to temporary directory with default config files

    proxy_config = load_proxy_config()
    rules_config = load_rules_config()

    assert proxy_config["destination"]["host"] == "127.0.0.1"
    assert rules_config["allowed_methods"] == ["GET", "POST"]

def test_load_custom_config_location(setup_custom_config, monkeypatch):
    """
    Test loading configuration from a custom location specified by CONFIG_LOCATION.
    """
    monkeypatch.setenv("CONFIG_LOCATION", str(setup_custom_config))

    proxy_config = load_proxy_config()
    rules_config = load_rules_config()

    assert proxy_config["destination"]["host"] == "127.0.0.1"
    assert rules_config["allowed_methods"] == ["GET", "POST"]

def test_missing_config_in_custom_location(tmp_path, monkeypatch):
    """
    Test behavior when config files are missing from the custom CONFIG_LOCATION.
    """
    missing_config_dir = tmp_path / "missing_config"
    missing_config_dir.mkdir()
    monkeypatch.setenv("CONFIG_LOCATION", str(missing_config_dir))

    with pytest.raises(FileNotFoundError, match="proxy_config.json"):
        load_proxy_config()

    with pytest.raises(FileNotFoundError, match="rules_config.json"):
        load_rules_config()

def test_missing_config_location_var(setup_default_config, monkeypatch):
    """
    Test that config loads from the default location when CONFIG_LOCATION is not set.
    """
    monkeypatch.chdir(setup_default_config)

    proxy_config = load_proxy_config()
    rules_config = load_rules_config()

    assert proxy_config["destination"]["host"] == "127.0.0.1"
    assert rules_config["rate_limit"] == "10 per minute"

@pytest.fixture
def setup_invalid_json_config(tmp_path):
    """
    Fixture to set up configuration files with invalid JSON content.
    """
    # Create files with invalid JSON in the temporary directory
    proxy_config = tmp_path / "proxy_config.json"
    rules_config = tmp_path / "rules_config.json"
    proxy_config.write_text('{ "destination": { "host": "127.0.0.1", "port": 8080, "path": "/"')  # Malformed JSON
    rules_config.write_text('{ "allowed_methods": ["GET", "POST"], "rate_limit": "10 per minute"')  # Malformed JSON

    return tmp_path

@pytest.fixture
def setup_missing_fields_config(tmp_path):
    """
    Fixture to set up configuration files with missing required fields.
    """
    # Create files missing required fields in the temporary directory
    proxy_config = tmp_path / "proxy_config.json"
    rules_config = tmp_path / "rules_config.json"
    proxy_config.write_text('{}')  # Missing "destination" key
    rules_config.write_text('{}')  # Make it same...
    return tmp_path

@pytest.fixture
def setup_nonexistent_config_location(tmp_path):
    """
    Fixture for a nonexistent configuration directory to simulate invalid path.
    """
    return tmp_path / "nonexistent_config_dir"  # This directory does not exist

def test_invalid_json_in_config_files(setup_invalid_json_config, monkeypatch):
    """
    Test loading configuration with invalid JSON syntax.
    """
    monkeypatch.chdir(setup_invalid_json_config)  # Change to directory with invalid JSON files

    with pytest.raises(json.JSONDecodeError):
        load_proxy_config()

    with pytest.raises(json.JSONDecodeError):
        load_rules_config()

def test_missing_required_fields_in_config_files(setup_missing_fields_config, monkeypatch):
    """
    Test loading configuration files that are missing required fields.
    """
    monkeypatch.chdir(setup_missing_fields_config)  # Change to directory with missing fields

    with pytest.raises(KeyError, match="destination"):
        load_proxy_config()


def test_nonexistent_config_location(monkeypatch, setup_nonexistent_config_location):
    """
    Test loading configuration with CONFIG_LOCATION set to a nonexistent directory.
    """
    monkeypatch.setenv("CONFIG_LOCATION", str(setup_nonexistent_config_location))

    with pytest.raises(FileNotFoundError, match="proxy_config.json"):
        load_proxy_config()

    with pytest.raises(FileNotFoundError, match="rules_config.json"):
        load_rules_config()


def test_check_required_files_all_present(tmp_path, monkeypatch, capsys):
    """
    Test check_required_files with all required files present.
    """
    # Create the required files in the temporary directory
    (tmp_path / "proxy_config.json").write_text("{}")
    (tmp_path / "rules_config.json").write_text("{}")

    # Mock the CONFIG_LOCATION environment variable to use tmp_path
    monkeypatch.setenv("CONFIG_LOCATION", str(tmp_path))
    
    # Call the function and capture output
    check_required_files(["proxy_config.json", "rules_config.json"])

    # Capture and check that no output is printed (i.e., no error message)
    captured = capsys.readouterr()
    assert captured.out == ""


def test_check_required_files_missing_one_file(tmp_path, monkeypatch, capsys):
    """
    Test check_required_files when one required file is missing.
    """
    # Create only one of the required files in the temporary directory
    (tmp_path / "proxy_config.json").write_text("{}")

    # Mock the CONFIG_LOCATION environment variable to use tmp_path
    monkeypatch.setenv("CONFIG_LOCATION", str(tmp_path))

    # Mock sys.exit to prevent exiting the test
    with pytest.raises(SystemExit) as exit_exception:
        check_required_files(["proxy_config.json", "rules_config.json"])

    # Capture and check the output for the missing file message
    captured = capsys.readouterr()
    assert "Error: Required configuration file 'rules_config.json' is missing." in captured.out
    assert exit_exception.value.code == 1


def test_check_required_files_missing_both_files(tmp_path, monkeypatch, capsys):
    """
    Test check_required_files when both required files are missing.
    """
    # Mock the CONFIG_LOCATION environment variable to use tmp_path
    monkeypatch.setenv("CONFIG_LOCATION", str(tmp_path))

    # Mock sys.exit to prevent exiting the test
    with pytest.raises(SystemExit) as exit_exception:
        check_required_files(["proxy_config.json", "rules_config.json"])

    # Capture and check the output for the missing files message
    captured = capsys.readouterr()
    assert "Error: Required configuration file 'proxy_config.json' is missing." in captured.out # It is displayed first
    assert exit_exception.value.code == 1


@pytest.fixture
def setup_extra_fields_config(tmp_path):
    """
    Fixture to set up a configuration file with unexpected fields in 'destination'.
    """
    proxy_config = tmp_path / "proxy_config.json"
    # Adding an unexpected field 'extra_field' to the 'destination' section
    proxy_config.write_text(json.dumps({
        "destination": {
            "host": "127.0.0.1",
            "port": 8080,
            "path": "/",
            "extra_field": "unexpected_value"  # Unexpected field
        }
    }))
    return tmp_path

def test_load_proxy_config_with_extra_fields(setup_extra_fields_config, monkeypatch):
    """
    Test loading a proxy configuration with unexpected fields in 'destination'.
    """
    # Use the fixture directory as CONFIG_LOCATION
    monkeypatch.setenv("CONFIG_LOCATION", str(setup_extra_fields_config))

    # Expect KeyError due to the unexpected 'extra_field' in the configuration
    with pytest.raises(KeyError, match="Unexpected fields in 'destination': extra_field"):
        load_proxy_config()