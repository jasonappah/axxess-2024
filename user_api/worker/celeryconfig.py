from api.config import settings

broker_url = settings.CELERY_BROKER_URL
result_backend = "db+" + settings.DATABASE_URI

task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]
timezone = "America/Chicago"
enable_utc = True
