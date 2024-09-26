# REDIS CACHE
# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": f"redis://127.0.0.1:6379/1",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         },
#     }
# }

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": [
            "redis://127.0.0.1:6379",
            # 'redis://redis:6379/1',
        ],
        "TIMEOUT": 1200,
    }
}
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
