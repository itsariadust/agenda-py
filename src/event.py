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