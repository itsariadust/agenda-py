from datetime import datetime, timedelta
import string
import random
import pickle


class Event:
    def __init__(self, uid: str, name: str, description: str,
                 start_date: datetime.date, end_date: datetime.date,
                 completed: bool = False):
        self.id = uid
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.completed = completed

    def __repr__(self):
        return (f"Event Title: {self.name} ({self.id})\n"
                f"Start Date: {self.start_date}\n"
                f"End Date: {self.end_date}\n"
                f"Event Description: {self.description}\n"
                f"Completed: {'Yes' if self.completed == True else 'No'}")
    
class AllDayEvent(Event):
    def __init__(self, uid: str, name: str, description: str,
                 all_day: bool, start_date: datetime.date, end_date: datetime.date, 
                 completed: bool = False):
        super().__init__(uid, name, description, start_date, end_date, completed)
        self.all_day = all_day

    def __repr__(self):
        return (f"Event Title: {self.name} ({self.id})\n"
                f"All Day: {'Yes' if self.all_day == True else 'No'}\n"
                f"Start Date: {self.start_date}\n"
                f"End Date: {self.end_date}\n"
                f"Event Description: {self.description}\n"
                f"Completed: {'Yes' if self.completed == True else 'No'}")

class TimedEvent(Event):
    def __init__(self, uid: str, name: str, description: str,
                 all_day: bool, start_date: datetime.date, end_date: datetime.date,
                 start_time: datetime.time, end_time: datetime.time, completed: bool = False):
        super().__init__(uid, name, description, start_date, end_date, completed)
        self.start_time = start_time
        self.end_time = end_time
        self.all_day = all_day
        
    def __repr__(self):
        return (f"Event Title: {self.name} ({self.id})\n"
                f"All Day: {'No' if self.all_day == False else 'yes'}\n"
                f"Start Date: {self.start_date} ({self.start_time})\n"
                f"End Date: {self.end_date} ({self.end_time})\n"
                f"Event Description: {self.description}\n"
                f"Completed: {'Yes' if self.completed == True else 'No'}")

class Agenda:
    def __init__(self, filename = 'agendafile.pkl'):
        self.filename = filename
        self.events = {}
        self.load_agenda()

    def save_agenda(self):
        with open(self.filename, 'wb') as file : pickle.dump(self.events, file)

    def load_agenda(self):
        try:
            with open(self.filename, 'rb') as file : self.events = pickle.load(file)
            print(f"Agenda loaded from {self.filename}")
        except FileNotFoundError:
            print("No agenda file found. Creating a new one.")

    def add_event(self):
        event_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

        event_name = input("Enter event name: ")
        event_description = input("Enter event description. If none, press enter: ") or "No description given."

        event_all_day = input("Is this an all day event? ").lower()

        # Helper functions to clean up the code
        def get_date(prompt):
            date_input = input(prompt)
            return datetime.strptime(date_input, '%m-%d-%Y').date()

        def get_time(prompt):
            time_input = input(prompt) or '00:00'
            return datetime.strptime(time_input, '%H:%M').time()
        
        event_start_date = get_date("Enter start date (MM-DD-YYYY): ")
        event_end_date = get_date("Enter end date (MM-DD-YYYY): ")

        if event_all_day == "no":
            event_all_day = False
            event_start_time = get_time("Enter start time (24-hour format, HH:MM): ")
            event_end_time = get_time("Enter end time (24-hour format, HH:MM): ")

            # Create a TimedEvent object inside the event_data variable
            event_data = TimedEvent(event_id, event_name, event_description,
                                    event_all_day, event_start_date, event_end_date,
                                    event_start_time, event_end_time)
        else:
            event_all_day = True

            # Create an AllDayEvent object inside the event_data variable
            event_data = AllDayEvent(event_id, event_name, event_description,
                                    event_all_day, event_start_date, event_end_date)

        self.events[event_id] = event_data

        print(f"Event '{event_name}' with ID '{event_id}' was added successfully!")

        # Save any changes to the pickle file.
        self.save_agenda()

    def remove_event(self):
        remove_event_id = input("Enter the event ID to remove the event: ")

        if remove_event_id not in self.events:
            print("Event not found. Please try again.")
            return

        del self.events[remove_event_id]
        print(f"Event with event ID '{remove_event_id} has been successfully removed.")
        self.save_agenda()

    def edit_event(self):
        # Some helper functions
        def get_new_date(prompt):
            date_input = input(prompt) or None
            return datetime.strptime(date_input, '%m-%d-%Y').date()

        def get_new_time(prompt):
            time_input = input(prompt) or '00:00' or None
            return datetime.strptime(time_input, '%H:%M').time()

        edit_event_id = input("Enter the event ID of the event that you wish to edit: ")

        # Check if there is an event.
        if edit_event_id not in self.events :
            print(f"No event with ID '{edit_event_id}' was found.")
            return

        event = self.events[edit_event_id]

        new_event_name = input("Enter new event name. If none, press enter: ") or event.name
        new_event_desc = input("Enter new event description. If none, press enter: ") or event.description

        new_start_date = get_new_date("Enter new event start date. If none, press enter: ") or event.start_date
        new_end_date = get_new_date("Enter new event end date. If none, press enter: ") or event.end_date

        all_day_prompt = input("Will this be an all day event or not? ").lower()

        if all_day_prompt == 'yes':
            all_day = True
            new_event_data = AllDayEvent(edit_event_id, new_event_name, new_event_desc,
                                         all_day, new_start_date, new_end_date)
        else:
            all_day = False
            new_start_time = get_new_time("Enter new event start time (HH:MM format): ") or event.start_time
            new_end_time = get_new_time("Enter new event end time (HH:MM format): ") or event.end_time
            new_event_data = TimedEvent(edit_event_id, new_event_name, new_event_desc,
                                        all_day, new_start_date, new_end_date,
                                        new_start_time, new_end_time)

        self.events[edit_event_id] = new_event_data
        self.save_agenda()
        print(f"Event with ID '{edit_event_id}' has been edited successfully.")

    def show_events(self):
        today = datetime.now().date()
        upcoming_events = []

        for event in self.events.values():
            if today <= event.end_date <= today + timedelta(days=7) : upcoming_events.append(event)

        print("Upcoming Events:" if upcoming_events else "No upcoming events.")
        for event in upcoming_events or []:
            print("-" * 30)
            print(event)
        print("-" * 30 + "\n")

    def search_event(self):
        find_event_id = input("Enter the ID of the event that you want to search: ")
        if find_event_id not in self.events:
            print("Event not found.")
            return
        print(self.events[find_event_id])

def main():
    agenda = Agenda()

    while True:
        print("Agenda")
        print("-" * 30)
        print("1. Add Event")
        print("2. Remove Event")
        print("3. Edit Event")
        print("4. Search Event")
        print("5. Show Events")
        print("6. Exit")
        choice = int(input("Enter your choice: "))

        match choice:
            case 1: agenda.add_event()
            case 2: agenda.remove_event()
            case 3: agenda.edit_event()
            case 4: agenda.search_event()
            case 5: agenda.show_events()
            case 6: print("Exiting...") or exit()
            case _: print("Invalid choice. Enter a valid choice.")


if __name__ == "__main__":
    main()
