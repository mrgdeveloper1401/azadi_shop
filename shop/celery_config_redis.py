from decouple import config


# broker_url = 'redis://127.0.0.1:6379/1'
broker_url = config("LIARA_REDIS_URL", cast=str)
# result_backend = 'redis://localhost/1'
result_backend = config("LIARA_REDIS_URL", cast=str)
accept_content = ['application/json']
task_serializer = 'json'
result_serializer = 'json'
timezone = 'Asia/Tehran'
result_expires = 120
task_always_eager = False
worker_prefetch_multiplier = 1
broker_connection_retry_on_startup = True
enable_utc = True
