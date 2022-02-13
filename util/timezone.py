from zoneinfo import ZoneInfo
from datetime import datetime as dt


def tzdiff(tz1: str, tz2: str) -> float:
    z1 = ZoneInfo(tz1)
    z2 = ZoneInfo(tz2)
    time = dt.now()

    hours = abs(z1.utcoffset(time).seconds - z2.utcoffset(time).seconds) / 3600
    if hours > 12.0:
        hours = 24.0-hours
    return hours

