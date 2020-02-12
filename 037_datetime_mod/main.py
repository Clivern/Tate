# 037. datetime
#
# datetime, timedelta, timezone, calendar, zoneinfo, and strftime.
#
# Run: python 037_datetime_mod/main.py

# --- datetime mod ---
from datetime import datetime, timezone

now = datetime.now(timezone.utc)
print(now.year, now.month, now.tzinfo)
print(datetime(2025, 1, 15, 12, 0).isoformat())
print(now.strftime("%A"))

# --- timedelta ---
from datetime import datetime, timedelta

start = datetime(2025, 1, 1)
print(start + timedelta(days=10, hours=5))
print(timedelta(hours=2).total_seconds())

# --- timezone ---
from datetime import datetime, timezone, timedelta

cet = timezone(timedelta(hours=1), name="CET")
print(datetime(2025, 1, 1, tzinfo=timezone.utc).astimezone(cet))

# --- calendar ---
import calendar

print(calendar.month_name[1], calendar.weekday(2025, 1, 1))
print(calendar.monthcalendar(2025, 1)[0])

# --- zoneinfo ---
from datetime import datetime

from zoneinfo import ZoneInfo

winter = datetime(2025, 1, 15, 12, 0, tzinfo=ZoneInfo("Europe/Berlin"))
summer = datetime(2025, 7, 15, 12, 0, tzinfo=ZoneInfo("Europe/Berlin"))
print(winter.strftime("%z"), summer.strftime("%z"))

# --- datetime fmt ---
from datetime import datetime

d = datetime(2025, 3, 14, 15, 9, 26)
print(d.strftime("%Y-%m-%d %H:%M"))
print(datetime.strptime("2025-01-02", "%Y-%m-%d").date())
print(datetime.fromisoformat("2025-01-02T03:04:05"))
