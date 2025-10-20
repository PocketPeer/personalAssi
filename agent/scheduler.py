from typing import Callable
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz


def create_scheduler(timezone: str) -> BackgroundScheduler:
    tz = pytz.timezone(timezone)
    return BackgroundScheduler(timezone=tz)


def schedule_morning_brief(scheduler: BackgroundScheduler, job_func: Callable[[], None]) -> None:
    trigger = CronTrigger(hour=7, minute=30, timezone=scheduler.timezone)
    scheduler.add_job(job_func, trigger=trigger, id="morning_brief", replace_existing=True)
