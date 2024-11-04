import warnings
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


def create_limiter(app, rules_config):
    """
    Initialize and apply the rate limiter if limiting is enabled.
    :param app: The Flask app instance.
    :param rules_config: The configuration that contains limiting rules.
    :return: Limiter object or None if limiting is disabled.
    """
    # Suppress the specific warning about in-memory storage
    warnings.filterwarnings(
        "ignore",
        message="Using the in-memory storage for tracking rate limits as no storage was explicitly specified",
    )

    if rules_config.get("limiting_enabled", False):
        rate_limit = rules_config.get("rate_limit", "10 per minute")
        limiter = Limiter(get_remote_address, app=app, default_limits=[rate_limit])
        app.logger.info(f"Rate limiting enabled with limit: {rate_limit}")
        return limiter

    app.logger.info("Rate limiting is disabled")
    return None
