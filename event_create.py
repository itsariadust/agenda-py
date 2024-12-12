import random
import string
from datetime import datetime, timedelta
from date_time_utils import get_date, get_time, hour_rounder
from event import TimedEvent, AllDayEvent


class EventCreate:
    def __init__(self):
        self.date_today = datetime.now()
        self.round_hour = hour_rounder(self.date_today)
        self.event_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

    def event_constructor(self, events_dict, event):
        event_name: str = event["event_name"]
        event_description: str = event["description"]
        event_all_day: bool = event["is_all_day"]
        event_start_date = datetime.strptime(event["start_date"], "%m-%d-%Y").date()
        event_end_date = datetime.strptime(event["end_date"], "%m-%d-%Y").date()

        if not event_all_day:
            event_data = self.create_timed_event(
                self.event_id, event_name, event_description,
                event_start_date, event_end_date,
                event.get("start_time"), event.get("end_time")
            )
        else:
            event_data = self.create_all_day_event(
                self.event_id, event_name, event_description,
                event_start_date, event_end_date
            )

        # Add to the events dictionary
        if event_start_date not in events_dict:
            events_dict[event_start_date] = {}

        events_dict[event_start_date][self.event_id] = event_data

        print(f"Event '{event_name}' with ID '{self.event_id}' was added successfully!")

        return events_dict

    def create_all_day_event(self, event_id, event_name, event_description, event_start_date, event_end_date):
        event_all_day = True
        return AllDayEvent(
            event_id, event_name, event_description,
            event_all_day, event_start_date, event_end_date
        )

    def create_timed_event(self, event_id, event_name, event_description, event_start_date,
                           event_end_date, event_start_time, event_end_time):
        event_all_day = False
        # Parse times if provided
        event_start_time = (
            datetime.strptime(event_start_time, "%H:%M").time() if event_start_time else self.round_hour.time()
        )
        event_end_time = (
            datetime.strptime(event_end_time, "%H:%M").time() if event_end_time else (self.round_hour + timedelta(hours=1)).time()
        )

        return TimedEvent(
            event_id, event_name, event_description,
            event_all_day, event_start_date, event_end_date,
            event_start_time, event_end_time
        )
