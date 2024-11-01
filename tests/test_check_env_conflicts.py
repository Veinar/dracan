import pytest
from dracan.utils.config_compliance_check import check_env_config_conflicts

@pytest.fixture
def rules_config():
    # Sample rules configuration for testing
    return {
        "uri_validation_enabled": True,
        "method_validation_enabled": False,
        "json_validation_enabled": True,
        "header_validation_enabled": False,
        "limiting_enabled": True,
        "payload_limiting_enabled": False,
        "ssl_validation_enabled": True
    }

def test_no_conflicts(monkeypatch, rules_config):
    # Set environment variables that match rules_config
    monkeypatch.setenv("URI_VALIDATION_ENABLED", "true")
    monkeypatch.setenv("METHOD_VALIDATION_ENABLED", "false")
    monkeypatch.setenv("JSON_VALIDATION_ENABLED", "true")
    monkeypatch.setenv("HEADER_VALIDATION_ENABLED", "false")
    monkeypatch.setenv("RATE_LIMITING_ENABLED", "true")
    monkeypatch.setenv("PAYLOAD_LIMITING_ENABLED", "false")
    monkeypatch.setenv("SSL_VALIDATION_ENABLED", "true")

    # Expect no exit since there are no conflicts
    check_env_config_conflicts(rules_config)

def test_conflict_in_uri_validation(monkeypatch, rules_config):
    # Introduce a conflict in URI_VALIDATION_ENABLED
    monkeypatch.setenv("URI_VALIDATION_ENABLED", "false")
    
    # Expect SystemExit due to mismatch
    with pytest.raises(SystemExit) as e:
        check_env_config_conflicts(rules_config)
    assert e.type == SystemExit
    assert e.value.code == 1

def test_conflict_in_method_validation(monkeypatch, rules_config):
    # Introduce a conflict in METHOD_VALIDATION_ENABLED
    monkeypatch.setenv("METHOD_VALIDATION_ENABLED", "true")
    
    # Expect SystemExit due to mismatch
    with pytest.raises(SystemExit) as e:
        check_env_config_conflicts(rules_config)
    assert e.type == SystemExit
    assert e.value.code == 1

def test_multiple_conflicts(monkeypatch, rules_config):
    # Set multiple environment variables with conflicts
    monkeypatch.setenv("URI_VALIDATION_ENABLED", "false")
    monkeypatch.setenv("METHOD_VALIDATION_ENABLED", "true")
    monkeypatch.setenv("SSL_VALIDATION_ENABLED", "false")
    
    # Expect SystemExit due to multiple mismatches
    with pytest.raises(SystemExit) as e:
        check_env_config_conflicts(rules_config)
    assert e.type == SystemExit
    assert e.value.code == 1
