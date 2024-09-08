from datetime import datetime, timedelta
import string
import random
import pickle


class Event:
    """
    The class exists to represent the event in a more object-oriented way.

    Attributes:
        name (str): The name of the event.
        description (str): The description of the event.
        all_day (str): Shows if the event is a day-long event or not.
        start_date (datetime): The starting date of the event.
        end_date (datetime): The ending date of the event.
    """
    def __init__(self, uid, name, description, all_day, start_date, end_date):
        """
        This initializes the class and its properties.

        Parameters:
            name (str): The name of the event.
            description (str): The description of the event.
            all_day (str): Shows if the event is a day-long event or not.
            start_date (datetime): The starting date of the event.
            end_date (datetime): The ending date of the event.
        """
        self.id = uid
        self.name = name
        self.description = description
        self.all_day = all_day
        self.start_date = start_date
        self.end_date = end_date
        self.completed = completed


    def __repr__(self):
        """
        This makes the class more readable instead of throwing gibberish.

        Instead of it looking like <__main__.Event object at 0x00000269E2FD9A50>,
        which is some kind of memory address, it looks more like the readable representation below here.
        That's why it's in the __repr__ function.
        """
        return (f"Event Title: {self.name} ({self.id})\n"
                f"All Day: {'Yes' if self.all_day == 'yes' else 'No'}\n"
                f"Start Date: {self.start_date}\n"
                f"End Date: {self.end_date}\n"
                f"Event Description: {self.description}\n"
                f"Completed: {self.completed}")


class Agenda:
    """
    This class containerizes all the important program functions into one class.

    When initialized, it will create a dictionary accessible inside this class only.
    """
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
        if event_all_day == "yes":
            event_start_date = input("What day will this event occur? ") + " 00:00"
            event_end_date = input("What day will this event end? ") + " 00:00"
        elif event_all_day == "no":
            event_start_date = input("Enter start date (MM-DD-YYYY HH:MM format): ")
            event_end_date = input("Enter end date (MM-DD-YYYY HH:MM format): ")

        # Parse date data wit datetime
        event_start_date = datetime.strptime(event_start_date, '%m-%d-%Y %H:%M')
        event_end_date = datetime.strptime(event_end_date, '%m-%d-%Y %H:%M')

        # Generate a unique ID (UID)
        event_id = self.generate_id()

        # Create an Event object inside the event_data variable
        event_data = Event(event_id, event_name, event_description, event_all_day, event_start_date, event_end_date)

        # Insert event_data to the dictionary with the event ID as its key. event_data is the value of the key.
        self.events[event_id] = event_data

        print(f"Event '{event_name}' with ID '{event_id}' was added successfully!")

        # Save any changes to the pickle file.
        self.save_agenda()

    def remove_event(self):
        remove_event_id = input("Enter the event ID to remove the event: ")

        if remove_event_id in self.events[remove_event_id]:
            del self.events[remove_event_id]
            print(f"Event with event ID '{remove_event_id} has been successfully removed.")
        else:
            print("Event not found. Please try again.")

    def edit_event(self):
        edit_event_id = input("Enter the event ID of the event that you wish to edit: ")
        if edit_event_id in self.events:
            event = self.events[edit_event_id]
            print(event)
            print(event.name)
            print(event.description)
            print(event.all_day)
            print(event.start_date)
            print(event.end_date)

    def show_events(self):
        today = datetime.now()
        upcoming_events = []

        for event in self.events.values():
            if today <= event.end_date <= today + timedelta(days=7):
                upcoming_events.append(event)

        if upcoming_events:
            print("\nEvents:")
            for event in upcoming_events:
                print(event)
                print("-" * 30)
        else:
            print("No upcoming events.")


def main():
    agenda = Agenda()

    while True:
        print("Agenda")
        print("-" * 20)
        print("1. Add Event")
        print("2. Remove Event")
        print("3. Edit Event")
        print("4. Show events")
        print("5. Exit")
        choice = int(input("Enter your choice: "))

        match choice:
            case 1:
                agenda.add_event()
            case 2:
                agenda.remove_event()
            case 3:
                agenda.edit_event()
            case 4:
                agenda.show_events()
            case 5:
                print("Exiting...")
                exit()
            case _:
                print("Invalid choice. Enter a valid choice.")


if __name__ == "__main__":
    main()
