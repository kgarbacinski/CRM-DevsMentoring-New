from prometheus_client import Histogram


class Metrics:
    upload_urls_created = Histogram(
        "upload_urls", "total number of upload urls created"
    )
