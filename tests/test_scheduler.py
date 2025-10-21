import re
from apscheduler.triggers.cron import CronTrigger
from agent.scheduler import create_scheduler, schedule_morning_brief


def test_schedule_morning_brief_0730_berlin():
    events = []

    def job():
        events.append("ran")

    sched = create_scheduler("Europe/Berlin")
    schedule_morning_brief(sched, job)

    jobs = sched.get_jobs()
    assert len(jobs) == 1
    j = jobs[0]
    assert isinstance(j.trigger, CronTrigger)
    rep = repr(j.trigger)
    assert "hour='7'" in rep and "minute='30'" in rep
    # APScheduler 3.x uses pytz timezones with .zone attribute
    tz = j.trigger.timezone
    # Accept both pytz and zoneinfo timezones
    zone = getattr(tz, "zone", None) or getattr(tz, "key", None)
    assert zone == "Europe/Berlin"
