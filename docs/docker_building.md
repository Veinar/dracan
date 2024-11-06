# Building Docker image

In order to prepare Docker image inside root directory of project execute:
```bash
docker build . -t dracan:latest
```
> You may want to change name or tag for this build command

> Docker image released on DockerHub does not contain config JSON files, remember to uncomment them from `.dockerignore` file!

### Docker environmental variables

To **explicitly disable** validation, filtering or restriction, use environment variables which, when passed to the container, will ignore the activation via `rules_config.json`.
> Dracan by default disables filtering/limiting/validation if entry is not present in `rules_config.json` file.

Additional `env`:
```bash
# Proxy TimeOut can be set or it will be 180 seconds by default
PROXY_TIMEOUT=180

# Health Check variables
HEALTHCHECK_DISABLED=false
HEALTHCHECK_PORT=9000 # Unused when HEALTHCHECK_DISABLED=true

# Metrics variables
ALLOW_METRICS_ENDPOINT=true
METRICS_PORT=9100 # Unused when ALLOW_METRICS_ENDPOINT=false

# Optional
LOG_LEVEL=INFO
CONFIG_LOCATION=/some/dir
```
For further details on configuration of env variables, refer to [this doc](./docs/docker_env_config.md).