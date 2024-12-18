import os
import sys


def check_env_config_conflicts(rules_config):
    """
    Checks for conflicts between environment variables and rules_config settings.
    Exits with status 1 if conflicts are detected, except when config is enabled
    but explicitly disabled in the environment variable, in which case it logs a note.
    """

    # Extract all keys from rules_config that end with '_enabled'
    config_enabled_keys = {
        k: v for k, v in rules_config.items() if k.endswith("_enabled")
    }

    # Iterate over the config keys and check for matching environment variables
    for config_key, config_value in config_enabled_keys.items():
        # Convert config key format to match environment variable naming conventions
        env_key = config_key.upper()

        # Get the value of the environment variable or None if it's not set
        env_value = os.getenv(env_key)

        # If the environment variable is set, compare it with the config value
        if env_value is not None:
            # Convert environment variable to boolean for comparison
            env_value_bool = env_value.lower() == "true"

            if env_value_bool != config_value:
                if config_value and not env_value_bool:
                    # Config file has enabled this setting, but env var disables it
                    print(
                        f"Note: '{env_key}' functionality has been explicitly disabled via environment variables, "
                        f"even though '{config_key}' in `rules_config.json` is set to true."
                    )
                else:
                    # Any other mismatch (e.g., config disabled but env var enables) is an error
                    print(
                        f"Error: Configuration mismatch - Environment variable '{env_key}' is set to "
                        f"{env_value_bool}, but '{config_key}' in `rules_config.json` is set to {config_value}."
                    )
                    print(
                        "Environment variable and configuration integrity check failed. ✖"
                    )
                    sys.exit(1)

    print("Environment variable and configuration integrity check passed. ✓")
