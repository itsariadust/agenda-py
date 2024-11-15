from datetime import datetime

import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *
from ttkbootstrap.widgets import DateEntry

class AgendaUI(ttk.Frame):
    def __init__(self, master_window):
        super().__init__(master_window)
        self.pack(fill=BOTH, expand=YES)
        self.container()
        self.table = self.create_table()

    def create_table(self):
        col_data = [
            {"text": "Event ID"},
            {"text": "Event Name"},
            {"text": "Event Description"},
            {"text": "Event Start"},
            {"text": "Event End"},
        ]

        row_data = [
            ('asdf', 'Test', 'Test Desc', datetime.now(), datetime.now()),
            ('ghjk', 'Test1', 'Test Desc', datetime.now(), datetime.now()),
            ('klzx', 'Test2', 'Test Desc', datetime.now(), datetime.now()),
        ]

        table = Tableview(
            master=self,
            coldata=col_data,
            rowdata=row_data,
            paginated=True,
            pagesize=10, # Number of rows to show per page
            autofit=True, # Whether to automatically change the size of a column based on the existing data
            bootstyle=PRIMARY,
        )

        table.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        return table

    def container(self):
        date_container = ttk.Frame(self)
        date_container.pack(side=LEFT, anchor=N, padx=10, pady=10, fill=Y)

        date = DateEntry(
            master=date_container,
        )
        date.pack(padx=5, pady=5, fill=X, expand=YES)

        add_btn = ttk.Button(
            master=date_container,
            text="Add",
            width=6,
        )
        add_btn.pack(padx=5, pady=5, fill=X)

        edit_btn = ttk.Button(
            master=date_container,
            text="Edit",
            width=6,
        )
        edit_btn.pack(padx=5, pady=5, fill=X)

        cancel_btn = ttk.Button(
            master=date_container,
            text="Delete",
            style=DANGER,
            width=6,
        )
        cancel_btn.pack(padx=5, pady=5, fill=X)

if __name__ == "__main__":
    app = ttk.Window(title="Agenda",
                     themename="darkly",
                     size=(800,600))
    AgendaUI(app)
    app.mainloop()


