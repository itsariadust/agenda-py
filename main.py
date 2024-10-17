from event import TimedEvent
from event_create import EventCreate
from event_remove import EventRemove
from event_edit import EventEdit
from datetime import datetime, timedelta, time
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

    def add_event(self):
        event_create = EventCreate()
        self.events = event_create.event_constructor(self.events)
        self.rebuild_index()
        self.save_agenda()

    def remove_event(self):
        event_remove = EventRemove()
        self.events = event_remove.event_remover(self.events, self.event_index)
        self.rebuild_index()
        self.save_agenda()

    def edit_event(self):
        event_edit = EventEdit()
        self.events = event_edit.event_editor(self.events, self.event_index)
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
