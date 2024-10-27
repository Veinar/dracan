import os
from threading import Thread
from dracan.core.app_factory import create_app
from dracan.core.health_check import run_health_check_server

app = create_app()

if __name__ == '__main__':
    # Check if health check should be disabled
    healthcheck_disabled = os.getenv("HEALTHCHECK_DISABLED", "false").lower() == "true"

    if not healthcheck_disabled:
        # Start the health check server in a separate thread
        health_thread = Thread(target=run_health_check_server)
        health_thread.daemon = True  # Ensures the thread stops when the main process exits
        health_thread.start()
    else:
        print("Healthcheck not running, disabled by env variable.")

    # Run the Flask app
    app.run(host='0.0.0.0', port=5000)
