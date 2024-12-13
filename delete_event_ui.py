import ttkbootstrap as ttk
from ttkbootstrap.widgets import Entry, Checkbutton, DateEntry
from tkinter.simpledialog import Dialog

class DeleteEventDialog(Dialog):
    def __init__(self, parent, event, **kwargs):
        self.event = event
        super().__init__(parent, **kwargs)

    def body(self, master):
        # Event Name
        ttk.Label(master, text=f"Are you sure you want to delete {self.event.name}?").grid(row=0, column=0, sticky=ttk.W)

    def apply(self):
        self.result = True