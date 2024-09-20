from event import TimedEvent, AllDayEvent
from datetime import datetime, timedelta, time
import string
import random
import pickle

class Agenda:
    def __init__(self, filename = 'agendafile.pkl'):
        self.filename = filename
        self.events = {}
        self.event_index = {}
        self.load_agenda()
        self.rebuild_index()
        self.greeting()
        self.show_upcoming_events()

    @staticmethod
    def greeting():
        current_hour = datetime.now().hour
        if current_hour < 12:
            day_greeting = "Good Morning"
        elif current_hour < 18:
            day_greeting = "Good Afternoon"
        else:
            day_greeting = "Good Evening"

        print(f"{day_greeting}! Today is {datetime.now().strftime('%A, %B %d')}.")

    def save_agenda(self):
        with open(self.filename, 'wb') as file : pickle.dump(self.events, file)

    def load_agenda(self):
        try:
            with open(self.filename, 'rb') as file : self.events = pickle.load(file)
            # print(f"Agenda loaded from {self.filename}")
        except FileNotFoundError:
            print("No agenda file found. Creating a new one.")

    def rebuild_index(self):
        self.event_index = {event_id: (date, event_obj)
                            for date, subdict in self.events.items()
                            for event_id, event_obj in subdict.items()}

    @staticmethod
    def get_date(prompt):
        date_input = input(prompt)
        if date_input: return datetime.strptime(date_input, '%m-%d-%Y').date()
        else: return False

    @staticmethod
    def get_time(prompt):
        time_input = input(prompt)
        if time_input: return datetime.strptime(time_input, '%H:%M').time()
        else: return False

    @staticmethod
    def hour_rounder(t: datetime):
        return (t.replace(second=0, microsecond=0, minute=0, hour=t.hour)
                + timedelta(hours=1))

    def add_event(self):
        event_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        date_today = datetime.strptime(datetime.now().strftime('%m-%d-%Y'), '%m-%d-%Y').date()
        hour_today = datetime.strptime(datetime.now().strftime('%H-%M'), '%H-%M')
        round_hour = self.hour_rounder(hour_today)

        event_name = input("Enter event name: ")
        event_description = input("Enter event description. If none, press enter: ") or "No description given."
        event_all_day = input("Is this an all day event? ").lower()
        event_start_date = self.get_date("Enter start date (MM-DD-YYYY): ") or date_today
        event_end_date = self.get_date("Enter end date (MM-DD-YYYY): ") or date_today

        if event_all_day == "no":
            event_all_day = False
            event_start_time = self.get_time("Enter start time (24-hour format): ") or round_hour.time()
            event_end_time = self.get_time("Enter end time (24-hour format): ") or round_hour + timedelta(hours=1)
            event_end_time = event_end_time.time()

            event_data = TimedEvent(event_id, event_name, event_description,
                                    event_all_day, event_start_date, event_end_date,
                                    event_start_time, event_end_time)
        else:
            event_all_day = True

            event_data = AllDayEvent(event_id, event_name, event_description,
                                    event_all_day, event_start_date, event_end_date)

        if event_start_date not in self.events:
            self.events[event_start_date] = {}

        self.events[event_start_date][event_id] = event_data

        print(f"Event '{event_name}' with ID '{event_id}' was added successfully!")

        # Rebuild index and save any changes to the pickle file.
        self.rebuild_index()
        self.save_agenda()

    def remove_event(self):
        remove_event_id = input("Enter the event ID to remove the event: ")

        if remove_event_id not in self.event_index:
            print("Event not found. Please try again.\n")
            return

        date, _ = self.event_index[remove_event_id]

        del self.events[date][remove_event_id]
        if not self.events[date] : del self.events[date]

        print(f"Event with event ID '{remove_event_id} has been successfully removed.")
        self.rebuild_index()
        self.save_agenda()

    def edit_event(self):
        edit_event_id = input("Enter the event ID of the event that you wish to edit: ")

        # Check if there is an event.
        if edit_event_id not in self.event_index:
            print(f"No event with ID '{edit_event_id}' was found.")
            return

        date, event = self.event_index[edit_event_id]

        new_event_name = input("Enter new event name. If none, press enter: ") or event.name
        new_event_desc = input("Enter new event description. If none, press enter: ") or event.description

        new_start_date = self.get_date("Enter new event start date. If none, press enter: ") or event.start_date
        new_end_date = self.get_date("Enter new event end date. If none, press enter: ") or event.end_date

        all_day_prompt = input("Will this be an all day event or not? ").lower() or 'No'

        if all_day_prompt == 'yes':
            all_day = True
            new_event_data = AllDayEvent(edit_event_id, new_event_name, new_event_desc,
                                         all_day, new_start_date, new_end_date)
        else:
            all_day = False
            new_start_time = self.get_time("Enter new event start time (HH:MM format): ") or event.start_time
            new_end_time = self.get_time("Enter new event end time (HH:MM format): ") or event.end_time
            new_event_data = TimedEvent(edit_event_id, new_event_name, new_event_desc,
                                        all_day, new_start_date, new_end_date,
                                        new_start_time, new_end_time)

        self.events[date][edit_event_id] = new_event_data

        print(f"Event with ID '{edit_event_id}' has been edited successfully.")

        self.rebuild_index()
        self.save_agenda()

    def show_upcoming_events(self):
        today = datetime.now().date()

        upcoming_events = [
            event for subdict in self.events.values()
            for event in subdict.values()
            if today <= event.end_date <= today + timedelta(days=7)
        ]

        if not upcoming_events:
            print("\nNo upcoming events.\n")
            return

        sorted_events = sorted(upcoming_events,
                               key=lambda e: (e.start_date, e.start_time if isinstance(e, TimedEvent) else time.min))

        current_date = None
        print(f"You currently have {len(sorted_events)} events.")
        for event in sorted_events:
            if event.start_date != current_date:
                current_date = event.start_date
                print(f"\n{current_date.strftime('%A, %b. %d')}")

            print(event.minified_str())

        print("-" * 30 + "\n")

    def search_event(self):
        find_event_id = input("Enter the ID of the event that you want to search: ")

        if find_event_id not in self.event_index:
            print("Event not found.")
            return
        _, event = self.event_index[find_event_id]
        print(f"Event found!\n"
              f"{event}\n")

def main():
    agenda = Agenda()

    while True:
        print("Agenda")
        print("-" * 30)
        print("1. Add Event")
        print("2. Remove Event")
        print("3. Edit Event")
        print("4. Search Event")
        print("5. Exit")
        choice = int(input("Enter your choice: "))

        match choice:
            case 1: agenda.add_event()
            case 2: agenda.remove_event()
            case 3: agenda.edit_event()
            case 4: agenda.search_event()
            case 5: print("Exiting...") or exit()
            case _: print("Invalid choice. Enter a valid choice.")


if __name__ == "__main__":
    main()
