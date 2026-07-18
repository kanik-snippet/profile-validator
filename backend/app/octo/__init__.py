settings = get_settings()

self.cloud_url = settings.octo_api_base_url.rstrip("/")
self.local_url = settings.octo_local_api.rstrip("/")

self.headers = {
    "X-Octo-Api-Token": settings.octo_api_token,
    "Content-Type": "application/json",
}