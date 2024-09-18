broker_url = 'redis://127.0.0.1:6379'
# broker_url = 'redis://redis:6379/0'
# result_serializer = 'django-db'
result_backend = 'redis://localhost'
accept_content = ['application/json']
task_serializer = 'json'
result_serializer = 'json'
timezone = 'Asia/Tehran'
result_expires = 120
task_always_eager = False
worker_prefetch_multiplier = 1

