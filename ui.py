import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *
from ttkbootstrap.widgets import DateEntry

from event_edit import EventEdit
from main import Agenda
from add_event_ui import AddEventDialog
from edit_event_ui import EditEventDialog
from event_create import EventCreate


class AgendaUI(ttk.Frame):
    def __init__(self, master_window):
        super().__init__(master_window)
        self.agenda = Agenda()
        self.selected_row = None
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
            paginated=True,
            pagesize=10,
            autofit=True,
            bootstyle=PRIMARY,
        )

        table.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        table.view.bind('<ButtonRelease-1>', self.on_row_select)
        return table

    def on_row_select(self, event):
        selected_item = self.table.view.selection()[0]
        item_data = self.table.view.item(selected_item)
        self.selected_row = item_data["values"][0]

    def refresh_table(self):
        self.table.delete_rows()
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
                self.table.insert_row('end', row)
        self.table.load_table_data()
        self.agenda.rebuild_index()
        self.agenda.save_agenda()

    def sidebar(self):
        container = ttk.Frame(self)
        container.pack(side=LEFT, anchor=N, padx=10, pady=10, fill=Y)

        date = DateEntry(
            master=container,
        )
        date.pack(padx=5, pady=5, fill=X, expand=YES)

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
            command="",
        )
        cancel_btn.pack(padx=5, pady=5, fill=X)

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
        dialog = AddEventDialog(self, title="Delete Event")

if __name__ == "__main__":
    app = ttk.Window(title="Agenda",
                     themename="darkly",
                     size=(800,600))
    AgendaUI(app)
    app.mainloop()
