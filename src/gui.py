import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime, timedelta
from automation import AutomationHelper
from formHandler import FormHandler
from config_handler import get_config, update_config
import re
from pynput import mouse, keyboard
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener, Key
import tkinter.simpledialog as simpledialog 

class OrderForm(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Order Entry Form")
        self.formhandler = FormHandler(self)
        self.value_config = get_config()
        self.current_task = None
        self.order_numbers = self.value_config["order_numbers"]
        self.unproductive_number = self.value_config["defaults"]["unproductive_number"]
        self.order_line_mapping = self.value_config["order_line_mapping"]
        self.mouse_listener = None
        self.keyboard_listener = None
        self.ctrl_pressed = False

        # Set the minimum window size
        self.minsize(400, 150)

        # Initialize order_name_var
        self.order_name_var = tk.StringVar()

        # Create the menu bar
        self.create_menu()

        # Create the main frame
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill='both', expand=True)

        # Create a placeholder for form_frame
        self.form_frame = tk.Frame(self.main_frame)
        self.form_frame.grid(row=0, column=0, sticky='nsew')

        # Create buttons_frame and grid it
        self.create_buttons_frame()
        self.buttons_frame.grid(row=1, column=0, sticky='nsew')

        # Create entries_frame
        self.create_entries_frame()

        # Configure grid weights
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=0)
        self.main_frame.grid_rowconfigure(2, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Create frames for different forms
        self.create_frames()

    def create_menu(self):
        # Menu bar configuration
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

        # Add Add Entry Button
        self.add_entry_button = tk.Button(self.buttons_frame, text="Add Entry", command=self.add_entry)
        self.add_entry_button.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        # Add Process All Button
        self.process_all_button = tk.Button(self.buttons_frame, text="Process All", command=self.start_event_listeners)
        self.process_all_button.grid(row=0, column=1, padx=10, pady=10, sticky='e')

        # Configure grid weights for buttons_frame
        self.buttons_frame.grid_columnconfigure(0, weight=1)
        self.buttons_frame.grid_columnconfigure(1, weight=1)


    def create_frames(self):
        # Define the GUI configuration for each form
        self.form_configs = {
            # ------------------ Case Work ------------------
            'Internal commissioning': {
                'fields': [
                    {'label': 'Order Type', 'type': 'label', 'var': tk.StringVar(), 'default': 'Sag'},
                    {'label': 'Order Number', 'type': 'ordernumber_combobox', 'var': tk.StringVar()},
                    {'label': 'Order Name', 'type': 'label', 'var': self.order_name_var},
                    {'label': 'Order Line', 'type': 'combobox', 'options': ['Software', 'Intern Indkøring', 'Extern Indkøring'], 'var': tk.StringVar(), 'default': 'Intern Indkøring'},
                    {'label': 'Date', 'type': 'date_entry', 'var': tk.StringVar()},
                    {'label': 'Time (H:M:S)', 'type': 'time_entry', 'var': tk.StringVar(), 'default': '08:00:00'},
                    {'label': 'Description', 'type': 'text', 'var': tk.StringVar()},
                ]
            },
            'External commissioning': {
                'fields': [
                    {'label': 'Order Type', 'type': 'label', 'var': tk.StringVar(), 'default': 'Sag'},
                    {'label': 'Order Number', 'type': 'ordernumber_combobox', 'var': tk.StringVar()},
                    {'label': 'Order Name', 'type': 'label', 'var': self.order_name_var},
                    {'label': 'Order Line', 'type': 'combobox', 'options': ['Software', 'Intern Indkøring', 'Extern Indkøring', 'Kørsel/Rejsetid'], 'var': tk.StringVar(), 'default': 'Extern Indkøring'},
                    {'label': 'Date', 'type': 'date_entry', 'var': tk.StringVar()},
                    {'label': 'Time (H:M:S)', 'type': 'time_entry', 'var': tk.StringVar(), 'default': '08:00:00'},
                    {'label': 'Description', 'type': 'text', 'var': tk.StringVar()},
                ]
            },
            'Software': {
                'fields': [
                    {'label': 'Order Type', 'type': 'label', 'var': tk.StringVar(), 'default': 'Sag'},
                    {'label': 'Order Number', 'type': 'ordernumber_combobox', 'var': tk.StringVar()},
                    {'label': 'Order Name', 'type': 'label', 'var': self.order_name_var},
                    {'label': 'Order Line', 'type': 'combobox', 'options': ['Software', 'Intern Indkøring', 'Extern Indkøring', 'Kørsel/Rejsetid'], 'var': tk.StringVar(), 'default': 'Software'},
                    {'label': 'Date', 'type': 'date_entry', 'var': tk.StringVar()},
                    {'label': 'Time (H:M:S)', 'type': 'time_entry', 'var': tk.StringVar(), 'default': '08:00:00'},
                    {'label': 'Description', 'type': 'text', 'var': tk.StringVar()},
                ]
            },
            # ------------------ Driving ------------------
            'Driving': {
                'fields': [
                    {'label': 'Order Type', 'type': 'label', 'var': tk.StringVar(), 'default': 'Sag'},
                    {'label': 'Date', 'type': 'date_entry', 'var': tk.StringVar()},
                    {'label': 'Order Number', 'type': 'ordernumber_combobox', 'var': tk.StringVar()},
                    {'label': 'Order Name', 'type': 'label', 'var': self.order_name_var},
                    {'label': 'Order Line', 'type': 'combobox', 'options': ['Kørsel/Rejsetid'], 'var': tk.StringVar(), 'default': 'Kørsel/Rejsetid'},
                    {'label': 'Driving Time (H:M:S)', 'type': 'time_entry', 'var': tk.StringVar()},
                    {'label': 'Description', 'type': 'text', 'var': tk.StringVar()},
                ]
            },
            # ------------------ "Uproduktiv Tid" ------------------
            'Internal meetings': {
                'fields': [
                    {'label': 'Order Type', 'type': 'label', 'var': tk.StringVar(), 'default': 'Sag'},
                    {'label': 'Date', 'type': 'date_entry', 'var': tk.StringVar()},
                    {'label': 'Order Line', 'type': 'combobox', 'options': ['Kurses Intern', 'Kursus Extern', 'Intern Møde'], 'var': tk.StringVar(), 'default': 'Intern Møde'},
                    {'label': 'Time (H:M:S)', 'type': 'time_entry', 'var': tk.StringVar(), 'default': '08:00:00'},
                    {'label': 'Description', 'type': 'text', 'var': tk.StringVar()},
                ]
            },
            'Internal courses': {
                'fields': [
                    {'label': 'Order Type', 'type': 'label', 'var': tk.StringVar(), 'default': 'Sag'},
                    {'label': 'Date', 'type': 'date_entry', 'var': tk.StringVar()},
                    {'label': 'Order Line', 'type': 'combobox', 'options': ['Kurses Intern', 'Kursus Extern', 'Intern Møde'], 'var': tk.StringVar(), 'default': 'Kurses Intern'},
                    {'label': 'Time (H:M:S)', 'type': 'time_entry', 'var': tk.StringVar(), 'default': '08:00:00'},
                    {'label': 'Description', 'type': 'text', 'var': tk.StringVar()},
                ]
            },
            'External courses': {
                'fields': [
                    {'label': 'Order Type', 'type': 'label', 'var': tk.StringVar(), 'default': 'Sag'},
                    {'label': 'Date', 'type': 'date_entry', 'var': tk.StringVar()},
                    {'label': 'Order Line', 'type': 'combobox', 'options': ['Kontor tid', 'Kurses Intern', 'Kursus Extern', 'Intern Møde'], 'var': tk.StringVar(), 'default': 'Kursus Extern'},
                    {'label': 'Time (H:M:S)', 'type': 'time_entry', 'var': tk.StringVar(), 'default': '08:00:00'},
                    {'label': 'Description', 'type': 'text', 'var': tk.StringVar()},
                ]
            },
            'Deskwork': {
                'fields': [
                    {'label': 'Order Type', 'type': 'label', 'var': tk.StringVar(), 'default': 'Sag'},
                    {'label': 'Date', 'type': 'date_entry', 'var': tk.StringVar()},
                    {'label': 'Order Line', 'type': 'combobox', 'options': ['Kontor tid', 'Kurses Intern', 'Kursus Extern', 'Intern Møde'], 'var': tk.StringVar(), 'default': 'Kontor tid'},
                    {'label': 'Time (H:M:S)', 'type': 'time_entry', 'var': tk.StringVar(), 'default': '08:00:00'},
                    {'label': 'Description', 'type': 'text', 'var': tk.StringVar()},
                ]
            },
            # ------------------ Free Days ------------------
            'Holiday': {
                'fields': [
                    {'label': 'Order Type', 'type': 'label', 'var': tk.StringVar(), 'default': 'Sag'},
                    {'label': 'Date', 'type': 'date_entry', 'var': tk.StringVar()},
                    {'label': 'Order Line', 'type': 'combobox', 'options': ['Ferie', 'Sygdom', 'Barns sygedag', 'Afspasering'], 'var': tk.StringVar(), 'default': 'Ferie'},
                    {'label': 'Time (H:M:S)', 'type': 'time_entry', 'var': tk.StringVar(), 'default': '08:00:00'},
                    {'label': 'Description', 'type': 'text', 'var': tk.StringVar()},
                ]
            },
            'Sickday': {
                'fields': [
                    {'label': 'Order Type', 'type': 'label', 'var': tk.StringVar(), 'default': 'Sag'},
                    {'label': 'Date', 'type': 'date_entry', 'var': tk.StringVar()},
                    {'label': 'Order Line', 'type': 'combobox', 'options': ['Ferie', 'Sygdom', 'Barns sygedag', 'Afspasering'], 'var': tk.StringVar(), 'default': 'Sygdom'},
                    {'label': 'Time (H:M:S)', 'type': 'time_entry', 'var': tk.StringVar(), 'default': '08:00:00'},
                    {'label': 'Description', 'type': 'text', 'var': tk.StringVar()},
                ]
            },
            'Childs Sickday': {
                'fields': [
                    {'label': 'Order Type', 'type': 'label', 'var': tk.StringVar(), 'default': 'Sag'},
                    {'label': 'Date', 'type': 'date_entry', 'var': tk.StringVar()},
                    {'label': 'Order Line', 'type': 'combobox', 'options': ['Ferie', 'Sygdom', 'Barns sygedag', 'Afspasering'], 'var': tk.StringVar(), 'default': 'Barns sygedag'},
                    {'label': 'Time (H:M:S)', 'type': 'time_entry', 'var': tk.StringVar(), 'default': '08:00:00'},
                    {'label': 'Description', 'type': 'text', 'var': tk.StringVar()},
                ]
            },
            'Compensatory Leave': {
                'fields': [
                    {'label': 'Order Type', 'type': 'label', 'var': tk.StringVar(), 'default': 'Sag'},
                    {'label': 'Date', 'type': 'date_entry', 'var': tk.StringVar()},
                    {'label': 'Order Line', 'type': 'combobox', 'options': ['Ferie', 'Sygdom', 'Barns sygedag', 'Afspasering'], 'var': tk.StringVar(), 'default': 'Afspasering'},
                    {'label': 'Time (H:M:S)', 'type': 'time_entry', 'var': tk.StringVar(), 'default': '08:00:00'},
                    {'label': 'Description', 'type': 'text', 'var': tk.StringVar()},
                ]
            }
        }

        # Add 'Multiple Days' and 'End Date' fields to all forms
        for form_name, config in self.form_configs.items():
            # Append 'Multiple Days' checkbox
            config['fields'].append({'label': 'Multiple Days', 'type': 'checkbox', 'var': tk.BooleanVar(), 'default': False})

            # Append 'End Date' field, initially disabled
            config['fields'].append({'label': 'End Date', 'type': 'date_entry', 'var': tk.StringVar(), 'state': 'disabled'})

    def create_entries_frame(self):
        self.entries_frame = tk.Frame(self.main_frame)
        
        # Add Treeview to display entries
        self.entries_tree = ttk.Treeview(self.entries_frame, columns=('Index', 'Date', 'Order Number', 'Order Line', 'Hours'), show='headings')
        self.entries_tree.heading('Date', text='Date')
        self.entries_tree.heading('Order Number', text='Order Number')
        self.entries_tree.heading('Order Line', text='Order Line')
        self.entries_tree.heading('Hours', text='Hours')
        self.entries_tree.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

        # Configure grid weights for entries_frame
        self.entries_frame.grid_rowconfigure(1, weight=1)
        self.entries_frame.grid_columnconfigure(0, weight=1)

        # Bind right-click event to create a delete entry option
        self.entries_tree.bind("<Button-3>", self.show_context_menu)
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Delete Entry", command=self.delete_entry)

        # Populate the Treeview with existing entries
        for i, entry in enumerate(self.formhandler):
            total_hours = entry["Normal Hours"] + entry["Overwork 1 Hours"] + entry["Overwork 2 Hours"] + entry["Normal Driving"] + entry["Overwork 1 Driving"] + entry["Overwork 2 Driving"]
            self.entries_tree.insert('', 'end', values=(
            i,
            entry["Date"],
            entry["Number"],
            entry["Line"],
            f'{total_hours:.2f}'
            ))


    def load_form(self, task_name):
        # Load the form for the selected task
        self.current_task = task_name
        if self.form_frame:
            self.form_frame.destroy()
        self.form_frame = tk.Frame(self.main_frame)
        self.form_frame.grid(row=0, column=0, sticky='nsew')
        self.generate_form(self.form_configs[task_name])
        
        # Update window size
        self.update_idletasks()
        self.geometry('')

    def generate_form(self, config):
        # This method generates the GUI based on the type of fields in the config
        # If it's desired to add more field types, they can be added here
        for idx, field in enumerate(config['fields']):
            label = tk.Label(self.form_frame, text=field['label'])
            label.grid(row=idx, column=0, padx=10, pady=5, sticky='w')

            field_var = field['var']
            default_value = field.get('default', '')

            if field['type'] == 'entry':
                entry = tk.Entry(self.form_frame, textvariable=field_var)
                entry.grid(row=idx, column=1, padx=10, pady=5)
                field_var.set(default_value)
            elif field['type'] == 'combobox':
                combobox = ttk.Combobox(self.form_frame, textvariable=field_var, values=field.get('options', []))
                combobox.grid(row=idx, column=1, padx=10, pady=5)
                combobox.set(default_value)
            elif field['type'] == 'ordernumber_combobox':
                ordernumber = ttk.Combobox(self.form_frame, textvariable=field_var, values=list(self.order_numbers.keys()))
                ordernumber.grid(row=idx, column=1, padx=10, pady=10)
                ordernumber.bind("<<ComboboxSelected>>", self.populate_order_number)
                ordernumber.bind("<FocusOut>", self.check_new_order_number)
                field['widget'] = ordernumber  # Store the widget reference
                self.order_number_combobox = ordernumber  # For later access
            elif field['type'] == 'time_entry':
                entry = tk.Entry(self.form_frame, textvariable=field_var)
                entry.grid(row=idx, column=1, padx=10, pady=5)
                entry.bind('<KeyRelease>', lambda event, e=entry: self.format_time_entry(event, e))
                field_var.set(default_value)
            elif field['type'] == 'date_entry':
                date_entry = DateEntry(self.form_frame, textvariable=field_var, width=12, background='darkblue', foreground='white', borderwidth=2)
                date_entry.grid(row=idx, column=1, padx=10, pady=5)
                if default_value:
                    date_entry.set_date(datetime.strptime(default_value, '%Y-%m-%d'))
                else:
                    date_entry.set_date(datetime.now())
                field['widget'] = date_entry  # Store reference
                # If 'state' is 'disabled', disable the widget
                if field.get('state') == 'disabled':
                    date_entry.config(state='disabled')
            elif field['type'] == 'label':
                if field.get('default'):
                    # For static text labels
                    static_label = tk.Label(self.form_frame, text=field['default'], anchor='w')
                    static_label.grid(row=idx, column=1, padx=10, pady=5, sticky='w')
                    field['widget'] = static_label
                else:
                    # For dynamic labels like 'Order Name'
                    dynamic_label = tk.Label(self.form_frame, textvariable=field['var'], anchor='w')
                    dynamic_label.grid(row=idx, column=1, padx=10, pady=5, sticky='w')
                    field['widget'] = dynamic_label
            elif field['type'] == 'text_readonly':
                # Multi-line uneditable text using a read-only Text widget
                text_widget = tk.Text(self.form_frame, height=4, width=30)
                text_widget.grid(row=idx, column=1, padx=10, pady=5)
                text_widget.insert('1.0', default_value)
                text_widget.config(state='disabled')  # Make it read-only
                field['widget'] = text_widget  # Store reference for later use
            elif field['type'] == 'text':
                text_widget = tk.Text(self.form_frame, height=4, width=30)
                text_widget.grid(row=idx, column=1, padx=10, pady=5)
                text_widget.insert('1.0', default_value)
                field['widget'] = text_widget  # Store reference for later use
            elif field['type'] == 'checkbox':
                checkbox = tk.Checkbutton(self.form_frame, text='', variable=field_var)
                checkbox.grid(row=idx, column=1, padx=10, pady=5)
                field['widget'] = checkbox  # Store reference
                # If there is a need to bind a command to the checkbox, to enable/disable 'End Date'
                if field['label'] == 'Multiple Days':
                    field_var.set(field.get('default', False))
                    field_var.trace('w', self.multiple_days_toggled)
        
        # Update window size
        self.update_idletasks()
        self.geometry('')

    def add_entry(self):
        # Collect form data
        config = self.form_configs[self.current_task]
        multiple_days = False
        end_date = None
        order_template = {}

        # Collect 'Multiple Days' value
        for field in config['fields']:
            if field['label'] == 'Multiple Days':
                multiple_days = field['var'].get()
                break

        # Collect other fields
        for field in config['fields']:
            if field['label'] == 'Order Type':
                order_template['type'] = field['var'].get()
            elif field['label'] == 'Order Number':
                order_template['number'] = field['var'].get() or self.unproductive_number
            elif field['label'] == 'Order Line':
                order_line = field['var'].get()
                order_template['line'] = self.order_line_mapping.get(order_line, None)
                if not order_template['line']:
                    messagebox.showerror("Order Line Error", f"Order Line '{order_line}' is not valid.")
                    return
            elif field['label'] == 'Date':
                start_date = field['widget'].get_date()
            elif field['label'] == 'End Date':
                if multiple_days:
                    end_date = field['widget'].get_date()
            elif field['label'] == 'Time (H:M:S)':
                time_str = field['var'].get()
                order_template['work_hours_used'] = self.convert_time_to_hours(time_str if time_str else "00:00:00")
            elif field['label'] == 'Driving Time (H:M:S)':
                driving_time_str = field['var'].get()
                order_template['driving_hours_used'] = self.convert_time_to_hours(driving_time_str if driving_time_str else "00:00:00")
            elif field['label'] == 'Description':
                order_template['description'] = field['widget'].get('1.0', tk.END).strip()

            if not self.entries_frame.winfo_ismapped():
                self.entries_frame.grid(row=2, column=0, sticky='nsew')
                # Optionally, update window size
                self.update_idletasks()
                self.geometry('')

        # Add entries to FormHandler
        if multiple_days and end_date and end_date >= start_date:
            delta = (end_date - start_date).days + 1
            for i in range(delta):
                current_date = start_date + timedelta(days=i)
                self.formhandler.add_form(
                    date=current_date.strftime('%d-%m-%y'),
                    type=order_template['type'],
                    number=order_template['number'],
                    name=self.order_numbers.get(order_template['number'], ""),
                    line=order_template['line'],
                    work_hours_used=order_template.get('work_hours_used', 0),
                    driving_hours_used=order_template.get('driving_hours_used', 0),
                    description=order_template.get('description', "")
                )
        else:
            self.formhandler.add_form(
                date=start_date.strftime('%d-%m-%y'),
                type=order_template['type'],
                number=order_template['number'],
                name=self.order_numbers.get(order_template['number'], ""),
                line=order_template['line'],
                work_hours_used=order_template.get('work_hours_used', 0),
                driving_hours_used=order_template.get('driving_hours_used', 0),
                description=order_template.get('description', "")
            )

        # Refresh Treeview and reset form
        self.refresh_entries_tree()
        self.reset_to_defaults()
        messagebox.showinfo("Entry Added", "The entry has been added.")

    def start_event_listeners(self):
        """Start mouse and keyboard listeners for CTRL + Left Click."""
        self.mouse_listener = MouseListener(on_click=self.on_mouse_click)
        self.keyboard_listener = KeyboardListener(on_press=self.on_key_press, on_release=self.on_key_release)
        
        self.mouse_listener.start()
        self.keyboard_listener.start()

    def stop_event_listeners(self):
        """Stop the listeners when the app is closed."""
        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.keyboard_listener:
            self.keyboard_listener.stop()

    def on_key_press(self, key):
        """Track if CTRL is pressed."""
        if key in [Key.ctrl_l, Key.ctrl_r]:
            self.ctrl_pressed = True

    def on_key_release(self, key):
        """Track if CTRL is released."""
        if key in [Key.ctrl_l, Key.ctrl_r]:
            self.ctrl_pressed = False

    def on_mouse_click(self, x, y, button, pressed):
        """Trigger `process_all_entries` on CTRL + Left Click."""
        if pressed and button == mouse.Button.left and self.ctrl_pressed:
            # Wait for the CTRL key to be released
            while self.ctrl_pressed:
                pass
            self.process_all_entries()
            # Stop the listeners
            self.stop_event_listeners()

    def process_all_entries(self):
        """Process all entries when triggered."""
        if len(self.formhandler) == 0:
            messagebox.showwarning("No Entries", "No entries to process.")
            return

        # Pass the data to AutomationHelper
        automation = AutomationHelper(self.formhandler)
        result = automation.perform_automation()
        if result:
            messagebox.showerror("Automation Error", result)
        else:
            messagebox.showinfo("Automation", "All entries have been submitted to the application.")
            # Clear entries after processing
            self.formhandler.data_list = []
            self.refresh_entries_tree()

    def format_time_entry(self, event, entry_widget):
        # Format the time entry as HH:MM:SS
        if event.keysym in ('BackSpace', 'Delete', 'Tab'):
            return
        content = entry_widget.get()
        # Remove all non-digit characters
        content = re.sub(r'\D', '', content)
        # Limit to 6 digits (HHMMSS)
        content = content[:6]
        # Insert colons at appropriate positions
        formatted = ''
        if len(content) >= 2:
            formatted += content[:2] + ':'
            if len(content) >= 4:
                formatted += content[2:4] + ':'
                formatted += content[4:]
            else:
                formatted += content[2:]
        else:
            formatted += content
        # Update the entry widget without moving the cursor
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, formatted)

    def reset_to_defaults(self):
        config = self.form_configs[self.current_task]
        for field in config['fields']:
            default_value = field.get('default', '')
            field_var = field['var']

            # Skip uneditable fields
            if field['type'] in ['label', 'text_readonly']:
                continue

            if field['type'] == 'date_entry':
                if field['label'] == 'End Date':
                    field_var.set('')
                    field['widget'].config(state='disabled')
                else:
                    field_var.set('')
                    field['widget'].set_date(datetime.now())
            elif field['type'] == 'checkbox':
                field_var.set(False)
            elif field['type'] == 'text':
                field['widget'].delete('1.0', tk.END)
            else:
                field_var.set(default_value)

    def populate_order_number(self, event):
        selected_order_number = event.widget.get()
        order_name = self.order_numbers.get(selected_order_number, "")
        self.order_name_var.set(order_name)

    def check_new_order_number(self, event):
        current_value = event.widget.get()
        if current_value and current_value not in self.order_numbers:
            # Prompt for the name of the Order Number
            order_name = simpledialog.askstring("New Order Number", f"Enter a name for Order Number '{current_value}':")
            if order_name:
                self.order_numbers[current_value] = order_name
                # Update the combobox values
                self.order_number_combobox.config(values=list(self.order_numbers.keys()))
                self.config['order_number'] = self.order_numbers
                update_config(self.config)
                self.order_name_var.set(order_name)
            else:
                messagebox.showinfo("Info", "Order Number not added.")
                event.widget.set('')  # Clear the invalid entry
                self.order_name_var.set("")

    def multiple_days_toggled(self, *args):
        # Find the 'Multiple Days' checkbox and 'End Date' field
        multiple_days_checked = False
        end_date_widget = None
        for field in self.form_configs[self.current_task]['fields']:
            if field['label'] == 'Multiple Days':
                multiple_days_checked = field['var'].get()
            if field['label'] == 'End Date':
                end_date_widget = field['widget']
        # Enable or disable 'End Date' field
        if end_date_widget:
            if multiple_days_checked:
                end_date_widget.config(state='normal')
            else:
                end_date_widget.config(state='disabled')

    def show_context_menu(self, event):
        # Get the item that was clicked on
        item = self.entries_tree.identify_row(event.y)
        if item:
            # Select the item
            self.entries_tree.selection_set(item)
            # Display the context menu
            try:
                self.context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                # Release the grab (required on some platforms)
                self.context_menu.grab_release()

    def delete_entry(self):
        selected_item = self.entries_tree.selection()
        if selected_item:
            # Confirm deletion
            confirm = messagebox.askyesno("Delete Entry", "Are you sure you want to delete the selected entry?")
            if confirm:
                # Get selected entry's values
                values = self.entries_tree.item(selected_item, "values")
                index, date, number, line = values[0], values[1], values[2], values[3]

                # Remove entry from FormHandler
                self.formhandler.remove_form(int(index))

                # Refresh the Treeview
                self.refresh_entries_tree()
        else:
            messagebox.showwarning("No Selection", "No entry selected.")

    def refresh_entries_tree(self):
        # Clear existing Treeview entries
        self.entries_tree.delete(*self.entries_tree.get_children())

        # Populate Treeview from FormHandler
        for i, item in enumerate(self.formhandler):
            total_hours = item["Normal Hours"] + item["Overwork 1 Hours"] + item["Overwork 2 Hours"] + item["Normal Driving"] + item["Overwork 1 Driving"] + item["Overwork 2 Driving"]
            self.entries_tree.insert('', 'end', values=(
                i,
                item["Date"],
                item["Number"],
                item["Line"], 
                f'{total_hours:.2f}'
            ))
        return


    def convert_time_to_hours(self, time_str):
        h, m, s = map(int, time_str.split(":"))
        return h + m / 60 + s / 3600
    
    def view_entries(self):
        df = self.formhandler.data_frame
        if df.empty:
            messagebox.showinfo("No Entries", "No entries in FormHandler.")
        else:
            print(df)  # Or display the DataFrame in a dedicated UI window
    
    def on_closing(self):
        """Stop listeners and close the application."""
        self.stop_event_listeners()
        self.destroy()


if __name__ == "__main__":
    app = OrderForm()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
