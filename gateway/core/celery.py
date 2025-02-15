import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('plantigo')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Konfiguracja zadań
app.conf.update(
    task_acks_late=True,
    task_time_limit=30,  # 30 sekund na wykonanie zadania
    task_soft_time_limit=20,  # Soft limit 20 sekund
    worker_prefetch_multiplier=1,  # Jeden task na workera
    task_always_eager=False,  # Asynchroniczne wykonywanie w produkcji
)

app.autodiscover_tasks()
