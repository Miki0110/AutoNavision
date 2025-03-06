import tkinter as tk
from tkinter import ttk

class UiSetupMixin:
    def create_menu(self):
        menubar = tk.Menu(self)

        # "Sag" Work Menu
        case_menu = tk.Menu(menubar, tearoff=0)
        case_menu.add_command(label="Internal commissioning", command=lambda: self.load_form('Internal commissioning'))
        case_menu.add_command(label="External commissioning", command=lambda: self.load_form('External commissioning'))
        case_menu.add_command(label="Software", command=lambda: self.load_form('Software'))
        menubar.add_cascade(label="Case work", menu=case_menu)

        # Driving Menu
        driving_menu = tk.Menu(menubar, tearoff=0)
        driving_menu.add_command(label="Standard", command=lambda: self.load_form('Driving'))
        menubar.add_cascade(label="Driving", menu=driving_menu)

        # "Uproduktiv Tid" Menu
        uproduktiv_menu = tk.Menu(menubar, tearoff=0)
        uproduktiv_menu.add_command(label="Intern Møde", command=lambda: self.load_form('Internal meetings'))
        uproduktiv_menu.add_command(label="Intern Kursus", command=lambda: self.load_form('Internal courses'))
        uproduktiv_menu.add_command(label="Extern Kursus", command=lambda: self.load_form('External courses'))
        uproduktiv_menu.add_command(label="Kontor tid", command=lambda: self.load_form('Deskwork'))
        menubar.add_cascade(label="Uproduktiv Tid", menu=uproduktiv_menu)

        # "Free days" Menu
        free_days_menu = tk.Menu(menubar, tearoff=0)
        free_days_menu.add_command(label="Ferie", command=lambda: self.load_form('Holiday'))
        free_days_menu.add_command(label="Sygdom", command=lambda: self.load_form('Sickday'))
        free_days_menu.add_command(label="Barns sygedag", command=lambda: self.load_form('Childs Sickday'))
        free_days_menu.add_command(label="Afspasering", command=lambda: self.load_form('Compensatory Leave'))
        menubar.add_cascade(label="Free days", menu=free_days_menu)

        self.config(menu=menubar)


    def create_buttons_frame(self):
        self.buttons_frame = tk.Frame(self.main_frame)

        # Add Entry Button
        self.add_entry_button = tk.Button(
            self.buttons_frame, text="Add Entry", command=self.add_entry
        )
        self.add_entry_button.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        # Process All Button
        self.process_all_button = tk.Button(
            self.buttons_frame, text="Process All", command=self.start_event_listeners
        )
        self.process_all_button.grid(row=0, column=1, padx=10, pady=10, sticky='e')

        # Configure grid weights for buttons_frame
        self.buttons_frame.grid_columnconfigure(0, weight=1)
        self.buttons_frame.grid_columnconfigure(1, weight=1)


    def create_entries_frame(self):
        self.entries_frame = tk.Frame(self.main_frame)
        
        # Treeview to display entries
        self.entries_tree = ttk.Treeview(
            self.entries_frame, 
            columns=('Index', 'Date', 'Order Number', 'Order Line', 'Hours'), 
            show='headings'
        )
        self.entries_tree.heading('Date', text='Date')
        self.entries_tree.heading('Order Number', text='Order Number')
        self.entries_tree.heading('Order Line', text='Order Line')
        self.entries_tree.heading('Hours', text='Hours')
        self.entries_tree.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

        self.entries_frame.grid_rowconfigure(1, weight=1)
        self.entries_frame.grid_columnconfigure(0, weight=1)

        # Bind right-click event to create a delete entry option
        self.entries_tree.bind("<Button-3>", self.show_context_menu)
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Delete Entry", command=self.delete_entry)
