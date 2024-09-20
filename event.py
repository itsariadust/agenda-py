from datetime import datetime

class Event:
    def __init__(self, uid: str, name: str, description: str,
                 start_date: datetime.date, end_date: datetime.date):
        self.id = uid
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date


class AllDayEvent(Event):
    def __init__(self, uid: str, name: str, description: str,
                 all_day: bool, start_date: datetime.date, end_date: datetime.date):
        super().__init__(uid, name, description, start_date, end_date)
        self.all_day = all_day

    def __str__(self):
        return (f"Event Title: {self.name} ({self.id})\n"
                f"All Day: {'Yes' if self.all_day == True else 'No'}\n"
                f"Start Date: {self.start_date}\n"
                f"End Date: {self.end_date}\n"
                f"Event Description: {self.description}\n")

    def minified_str(self):
        return f"{'All Day'.ljust(20)} {self.name} ({self.id})"


class TimedEvent(Event):
    def __init__(self, uid: str, name: str, description: str,
                 all_day: bool, start_date: datetime.date, end_date: datetime.date,
                 start_time: datetime.time, end_time: datetime.time):
        super().__init__(uid, name, description, start_date, end_date)
        self.start_time = start_time
        self.end_time = end_time
        self.all_day = all_day

    def __str__(self):
        return (f"Event Title: {self.name} ({self.id})\n"
                f"All Day: {'No' if self.all_day == False else 'yes'}\n"
                f"Start Date: {self.start_date} ({self.start_time})\n"
                f"End Date: {self.end_date} ({self.end_time})\n"
                f"Event Description: {self.description}\n")

    def minified_str(self):
        start_and_end_time_str = f"{self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"
        return f"{start_and_end_time_str.ljust(20)} {self.name} ({self.id})"