from dataclasses import dataclass


@dataclass()
class Unit:
    name: str
    min: int
    max: int


unitMinute = Unit("minute", 0, 59)
unitHour = Unit("hour", 0, 23)
unitDay = Unit("day", 1, 31)
unitMonth = Unit("month", 1, 12)
unitWeekday = Unit("weekday", 0, 6)


units = [unitMinute, unitHour, unitDay, unitMonth, unitWeekday]
