from datetime import datetime
import pickle

class Agenda:
    def __init__(self, filename = 'agendafile.pkl'):
        self.filename = filename
        self.events = {}
        self.event_index = {}
        self.load_agenda()
        self.rebuild_index()
        self.greeting()

    @staticmethod
    def greeting():
        current_hour = datetime.now().hour
        if current_hour < 12:
            day_greeting = "Good Morning"
        elif current_hour < 18:
            day_greeting = "Good Afternoon"
        else:
            day_greeting = "Good Evening"

        greeting = f"{day_greeting}!\nToday is {datetime.now().strftime('%A, %B %d')}."
        return greeting

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

def main():
    Agenda()

if __name__ == "__main__":
    main()
