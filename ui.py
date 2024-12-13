from datetime import datetime

import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *
from ttkbootstrap.widgets import DateEntry

from delete_event_ui import DeleteEventDialog
from event_edit import EventEdit
from event_remove import EventRemove
from main import Agenda
from add_event_ui import AddEventDialog
from edit_event_ui import EditEventDialog
from event_create import EventCreate


class AgendaUI(ttk.Frame):
    def __init__(self, master_window):
        super().__init__(master_window)
        self.date_var = None
        self.agenda = Agenda()
        self.selected_row = None
        self.selected_date = None
        self.pack(fill=BOTH, expand=YES)
        self.sidebar()
        self.table = self.create_table()
        self.refresh_table()

    def create_table(self):
        col_data = [
            {"text": "Event ID"},
            {"text": "Event Name"},
            {"text": "Event Description"},
            {"text": "All Day"},
            {"text": "Event Start"},
            {"text": "Event End"},
        ]

        table = Tableview(
            master=self,
            coldata=col_data,
            rowdata=[],
            autofit=False,
            bootstyle=PRIMARY,
        )

        table.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        table.view.bind('<ButtonRelease-1>', lambda e : self.on_row_select())
        return table

    def on_row_select(self):
        selected_row = self.table.view.selection()[0]
        selected_row_data = self.table.view.item(selected_row)
        self.selected_row = selected_row_data["values"][0]

    def refresh_table(self):
        self.table.delete_rows()
        if self.selected_date:
            selected_date_events = self.agenda.events.get(self.selected_date)
            for event_id, event_obj in selected_date_events.items():
                row = (
                    event_id,
                    event_obj.name,
                    event_obj.description,
                    event_obj.all_day,
                    f"{event_obj.start_date.strftime('%m-%d-%Y')} ({getattr(event_obj, 'start_time', '00:00')})",
                    f"{event_obj.end_date.strftime('%m-%d-%Y')} ({getattr(event_obj, 'end_time', '00:00')})",
                )
                self.table.insert_row(values=row)
        else:
            for event_date, events in self.agenda.events.items():
                for event_id, event_obj in events.items():
                    row = (
                        event_id,
                        event_obj.name,
                        event_obj.description,
                        event_obj.all_day,
                        f"{event_obj.start_date.strftime('%m-%d-%Y')} ({getattr(event_obj, 'start_time', '00:00')})",
                        f"{event_obj.end_date.strftime('%m-%d-%Y')} ({getattr(event_obj, 'end_time', '00:00')})",
                    )
                    self.table.insert_row(values=row)
        self.table.load_table_data()
        self.agenda.rebuild_index()
        self.agenda.save_agenda()

    def sidebar(self):
        container = ttk.Frame(self)
        container.pack(side=LEFT, anchor=N, padx=10, pady=10, fill=Y)

        ttk.Label(master=container, text=f"{self.agenda.greeting()}", font=('Arial', 12)).pack(padx=5, pady=5, fill=X)

        self.date_var = ttk.StringVar()
        date_entry = DateEntry(
            master=container,
        )
        date_entry.pack(padx=5, pady=5, fill=X)
        date_entry.bind("<FocusOut>", lambda e: self.update_selected_date(date_entry))

        add_btn = ttk.Button(
            master=container,
            text="Add",
            width=6,
            command=self.add_event,
        )
        add_btn.pack(padx=5, pady=5, fill=X)

        edit_btn = ttk.Button(
            master=container,
            text="Edit",
            width=6,
            command=self.edit_event,
        )
        edit_btn.pack(padx=5, pady=5, fill=X)

        cancel_btn = ttk.Button(
            master=container,
            text="Delete",
            style=DANGER,
            width=6,
            command=self.delete_event,
        )
        cancel_btn.pack(padx=5, pady=5, fill=X)

        show_all_btn = ttk.Button(
            master=container,
            text="Show All",
            width=6,
            command=self.show_all_events,
        )
        show_all_btn.pack(padx=5, pady=5, fill=X)

    def show_all_events(self):
        self.selected_date = None
        self.refresh_table()

    def update_selected_date(self, date_entry):
        new_date = datetime.strptime(date_entry.entry.get(), "%m/%d/%Y").date()
        self.selected_date = new_date
        self.refresh_table()

    def add_event(self):
        dialog = AddEventDialog(self, title="New Event")

        if dialog.result:
            event_creator = EventCreate()
            updated_events = event_creator.event_constructor(self.agenda.events, dialog.result)
            self.agenda.events = updated_events
            self.refresh_table()

    def edit_event(self):
        event_to_edit = self.selected_row
        event_data = self.agenda.event_index[event_to_edit][1]
        dialog = EditEventDialog(self, title="Edit Event", event=event_data)

        if dialog.result:
            event_edit = EventEdit()
            updated_events = event_edit.event_editor(self.agenda.events, dialog.result)
            self.agenda.events = updated_events
            self.refresh_table()

    def delete_event(self):
        event_to_edit = self.selected_row
        event_data = self.agenda.event_index[event_to_edit][1]
        dialog = DeleteEventDialog(self, title="Delete Event", event=event_data)

        if dialog.result:
            delete_event = EventRemove()
            updated_events = delete_event.event_remover(event_data.id, self.agenda.events, self.agenda.event_index)
            self.agenda.events = updated_events
            self.refresh_table()

if __name__ == "__main__":
    app = ttk.Window(title="Agenda",
                     themename="darkly",
                     size=(1200,900))
    AgendaUI(app)
    app.mainloop()
