from .. import env

STREAMING = {
    "BROKER_URL": env("STREAMING_BROKER_URL"),
    "QUEUES": {
        "hope_control_manager": {
            "routing": ["hope.*.*"],
        },
    },
}
