from datetime import datetime, timedelta
import string
import random
import pickle


class Event:
    # The class exists to represent the event in a more object-oriented way.
    def __init__(self, uid, name, description,
                 all_day, start_date, end_date,
                 start_time, end_time, completed = False):
        # This initializes the class and its properties.
        self.id = uid
        self.name = name
        self.description = description
        self.all_day = all_day
        self.start_date = start_date
        self.end_date = end_date
        self.start_time = start_time
        self.end_time = end_time
        self.completed = completed


    def __repr__(self):
        # This makes the class more readable instead of throwing gibberish.
        #
        # Instead of it looking like <__main__.Event object at 0x00000269E2FD9A50>,
        # which is some kind of memory address, it looks more like the readable representation below here.
        # That's why it's in the __repr__ function.
        return (f"Event Title: {self.name} ({self.id})\n"
                f"All Day: {'Yes' if self.all_day == 'yes' else 'No'}\n"
                f"Start Date: {self.start_date} ({self.start_time})\n"
                f"End Date: {self.end_date} ({self.end_time})\n"
                f"Event Description: {self.description}\n"
                f"Completed: {'Yes' if self.completed == True else 'No'}")

class Agenda:
    def __init__(self, filename = 'agendafile.pkl'):
        self.filename = filename
        self.events = {}
        self.load_agenda()

    def generate_id(self):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

    def save_agenda(self):
        with open(self.filename, 'wb') as file:
            pickle.dump(self.events, file)

    def load_agenda(self):
        try:
            with open(self.filename, 'rb') as file:
                self.events = pickle.load(file)
            print(f"Agenda loaded from {self.filename}")
        except FileNotFoundError:
            print("No agenda file found. Creating a new one.")

    def add_event(self):
        event_name = input("Enter event name: ")
        event_description = input("Enter event description. If none, press enter: ")
        if event_description == '':
            event_description = "No description given."
        event_all_day = input("Is this an all day event? ").lower()

        # Helper functions to clean up the code
        def get_date(prompt):
            date_str = input(prompt)
            return datetime.strptime(date_str, '%m-%d-%Y').date()

        def get_time(prompt):
            time_str = input(prompt) or '00:00'
            return datetime.strptime(time_str, '%H:%M').time()

        event_start_date = get_date("Enter start date (MM-DD-YYYY): ")
        event_end_date = get_date("Enter end date (MM-DD-YYYY): ")

        if event_all_day == "no":
            event_start_time = get_time("Enter start time (24-hour format, HH:MM): ")
            event_end_time = get_time("Enter end time (24-hour format, HH:MM): ")
        else:
            event_start_time = event_end_time = datetime.strptime('00:00','%H:%M').time()

        # Generate a unique ID (UID)
        event_id = self.generate_id()

        # Create an Event object inside the event_data variable
        event_data = Event(event_id, event_name, event_description,
                           event_all_day, event_start_date, event_end_date,
                           event_start_time, event_end_time)

        self.events[event_id] = event_data

        print(f"Event '{event_name}' with ID '{event_id}' was added successfully!")

        # Save any changes to the pickle file.
        self.save_agenda()

    def remove_event(self):
        remove_event_id = input("Enter the event ID to remove the event: ")

        if remove_event_id in self.events:
            del self.events[remove_event_id]
            print(f"Event with event ID '{remove_event_id} has been successfully removed.")
            self.save_agenda()
        else:
            print("Event not found. Please try again.")

    def edit_event(self):
        edit_event_id = input("Enter the event ID of the event that you wish to edit: ")
        if edit_event_id in self.events:
            event = self.events[edit_event_id]

            new_event_name = input("Enter new event name: ") or event.name
            new_event_desc = input("Enter new event description: ") or event.description

            def get_date_input(prompt, fallback, time_suffix=""):
                date_input = input(prompt) or None
                if date_input:
                    return datetime.strptime(date_input + time_suffix, '%Y-%m-%d %H:%M')
                return fallback

            if event.all_day == 'yes':
                new_event_all_day_prompt = input("Keep this an all-day event? (yes/no): ").lower()

                if new_event_all_day_prompt == 'yes':
                    new_start_date = get_date_input("Enter new event start date: ", event.start_date, " 00:00")
                    new_end_date = get_date_input("Enter new event end date: ", event.end_date, " 00:00")
                elif new_event_all_day_prompt == 'no':
                    new_start_date = get_date_input("Enter new event start date (with time): ", event.start_date)
                    new_end_date = get_date_input("Enter new event end date (with time): ", event.end_date)

            elif event.all_day == 'no':
                new_event_all_day_prompt = input("Make this an all-day event? (yes/no): ").lower()

                if new_event_all_day_prompt == 'no':
                    new_start_date = get_date_input("Enter new event start date (with time): ", event.start_date)
                    new_end_date = get_date_input("Enter new event end date (with time): ", event.end_date)
                elif new_event_all_day_prompt == 'yes':
                    new_start_date = get_date_input("Enter new event start date: ", event.start_date, " 00:00")
                    new_end_date = get_date_input("Enter new event end date: ", event.end_date, " 00:00")

            self.events[edit_event_id] = Event(edit_event_id, new_event_name, new_event_desc, event.all_day,
                                               new_start_date, new_end_date)
            self.save_agenda()
            print(f"Event with ID '{edit_event_id}' has been edited successfully.")
        else:
            print(f"No event with ID '{edit_event_id}' was found.")

    def show_events(self):
        today = datetime.now().date()
        upcoming_events = []

        for event in self.events.values():
            if today <= event.end_date <= today + timedelta(days=7):
                upcoming_events.append(event)

        if upcoming_events:
            print("Upcoming Events:")
            for event in upcoming_events:
                print("-" * 30)
                print(event)
        else:
            print("No upcoming events.")
        print("-" * 30 + "\n")

    def search_event(self):
        find_event_id = input("Enter the ID of the event that you want to search: ")
        if find_event_id in self.events:
            print(self.events[find_event_id])
        else:
            print("Event not found.")

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
            case 1:
                agenda.add_event()
            case 2:
                agenda.remove_event()
            case 3:
                agenda.edit_event()
            case 4:
                agenda.search_event()
            case 5:
                agenda.show_events()
            case 6:
                print("Exiting...")
                exit()
            case _:
                print("Invalid choice. Enter a valid choice.")


if __name__ == "__main__":
    main()
