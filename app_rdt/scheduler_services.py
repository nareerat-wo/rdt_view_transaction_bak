from apscheduler.schedulers.background import BackgroundScheduler

from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

scheduler = BackgroundScheduler(timezone="Asia/Bangkok")
scheduler.add_jobstore(DjangoJobStore(), "default")
register_events(scheduler)
scheduler.start()