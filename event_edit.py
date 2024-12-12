from event import AllDayEvent, TimedEvent
from datetime import datetime

class EventEdit:
    def __init__(self):
        pass

    def event_editor(self, events_dict, result):
        print(events_dict)
        event_id = result.get("id")
        new_event_name = result.get("event_name")
        new_event_desc = result.get("description")
        new_start_date = datetime.strptime(result.get("start_date"), "%m-%d-%Y").date()
        new_end_date = datetime.strptime(result.get("end_date"), "%m-%d-%Y").date()
        is_all_day = result.get("is_all_day")

        # Identify the current event and its date
        original_date = None
        for date, events in events_dict.items():
            if event_id in events:
                original_date = date
                break

        if original_date is None:
            print(f"No event with ID '{event_id}' found in the current dictionary.")
            return events_dict

        del events_dict[original_date][event_id]

        if not events_dict[original_date]:
            del events_dict[original_date]

        if is_all_day:
            new_event_data = self.all_day(event_id, new_event_name, new_event_desc,
                                          new_start_date, new_end_date)
        else:
            new_start_time = result.get("start_time")
            new_end_time = result.get("end_time")
            new_event_data = self.timed(event_id, new_event_name, new_event_desc,
                                        new_start_date, new_end_date, new_start_time, new_end_time)

        if new_start_date not in events_dict:
            events_dict[new_start_date] = {}

        events_dict[new_start_date][event_id] = new_event_data

        print(f"Event with ID '{event_id}' has been updated successfully.")
        return events_dict

    @staticmethod
    def all_day(edit_event_id, new_event_name, new_event_desc,
                new_start_date, new_end_date):
        all_day = True
        return AllDayEvent(edit_event_id, new_event_name, new_event_desc,
                           all_day, new_start_date, new_end_date)

    @staticmethod
    def timed(edit_event_id, new_event_name, new_event_desc,
              new_start_date, new_end_date, new_start_time, new_end_time):
        all_day = False
        return TimedEvent(edit_event_id, new_event_name, new_event_desc,
                          all_day, new_start_date, new_end_date,
                          new_start_time, new_end_time)
