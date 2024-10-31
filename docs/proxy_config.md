# `proxy_config.json` Configuration Guide

This short doc will explain how to set properly proxy config file.

```json
{
    "destination": {
        "host": "127.0.0.1",
        "port": 8080,
        "path": "/"
    }
}
```

**Explanation of Fields:**

* **host**: The IP address or hostname or FQDN of the target server where requests should be forwarded. In this example, it’s set to `127.0.0.1` (localhost) but on real case scenario it would rather look like `application.namespace.svc.cluster.local`.
* **port**: The port on the target server where the application listens.
* **path**: The base path on the destination server to which requests should be forwarded. Using `/` as the path will forward requests to the root of the target server.