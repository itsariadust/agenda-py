import ttkbootstrap as ttk
from ttkbootstrap.widgets import Entry, Checkbutton, DateEntry
from tkinter.simpledialog import Dialog
from datetime import datetime

class AddEventDialog(Dialog):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

    def validate_time(self, x) -> bool:
        if self.strptime_test(x, "%H:%M"):
            return True
        elif x == "":
            return False
        else:
            return False

    def strptime_test(self, date, datetime_format):
        try:
            datetime.strptime(date, datetime_format)
            return True
        except ValueError:
            return False

    def body(self, master):
        time_func = self.register(self.validate_time)

        ttk.Label(master, text="Event Name:").grid(row=0, column=0, sticky=ttk.W)
        self.event_name = Entry(master)
        self.event_name.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(master, text="Description:").grid(row=1, column=0, sticky=ttk.W)
        self.description = Entry(master)
        self.description.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(master, text="All Day Event:").grid(row=2, column=0, sticky=ttk.W)
        self.is_all_day = ttk.BooleanVar(value=True)
        self.all_day_check = Checkbutton(
            master, variable=self.is_all_day, command=self.toggle_time_fields
        )
        self.all_day_check.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(master, text="Start Date (MM-DD-YYYY):").grid(row=3, column=0, sticky=ttk.W)
        self.start_date = DateEntry(master, dateformat="%m-%d-%Y")
        self.start_date.grid(row=3, column=1, padx=10, pady=5)

        ttk.Label(master, text="End Date (MM-DD-YYYY):").grid(row=4, column=0, sticky=ttk.W)
        self.end_date = DateEntry(master, dateformat="%m-%d-%Y")
        self.end_date.grid(row=4, column=1, padx=10, pady=5)

        ttk.Label(master, text="Start Time (in 24-hour format):").grid(row=5, column=0, sticky=ttk.W)
        self.start_time = Entry(master, validate="focus", validatecommand=(time_func, '%P'))
        self.start_time.grid(row=5, column=1, padx=10, pady=5)
        self.start_time.config(state="disabled")

        ttk.Label(master, text="End Time (in 24-hour format):").grid(row=6, column=0, sticky=ttk.W)
        self.end_time = Entry(master, validate="focus", validatecommand=(time_func, '%P'))
        self.end_time.grid(row=6, column=1, padx=10, pady=5)
        self.end_time.config(state="disabled")

    def toggle_time_fields(self):
        if self.is_all_day.get():
            self.start_time.config(state="disabled")
            self.end_time.config(state="disabled")
        else:
            self.start_time.config(state="normal")
            self.end_time.config(state="normal")

    def apply(self):
        start_date = self.start_date.entry.get()
        end_date = self.end_date.entry.get()

        self.result = {
            "event_name": self.event_name.get(),
            "description": self.description.get(),
            "is_all_day": self.is_all_day.get(),
            "start_date": start_date,
            "end_date": end_date,
            "start_time": self.start_time.get() if not self.is_all_day.get() else None,
            "end_time": self.end_time.get() if not self.is_all_day.get() else None,
        }
