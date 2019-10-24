import os

PROD_MODE = os.environ.get("PROD_MODE", "False") == "TRUE"
CACHE_REDIS_URL = os.environ.get("CACHE_REDIS_URL", None)
API_V1_ROOT = "/api/v1/"