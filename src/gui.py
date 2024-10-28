import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime
from automation import AutomationHelper
import re
import json
import os


# Mapping of Order Line names to their corresponding numbers
order_line_mapping = {
    "Software": "180200",
    "Intern Indkøring": "700300",
    "Extern Indkøring": "700800",
    "Kursus Intern": "100002",
    "Kørsel/Rejsetid": "500900"
}


class OrderForm(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Order Entry Form")
        self.geometry("600x100")
        self.current_task = None
        self.current_frame = None
        self.order_numbers_file = 'order_numbers.json'
        self.load_order_numbers()

        # Initialize order_name_var
        self.order_name_var = tk.StringVar()

        # Create the menu bar
        self.create_menu()

        # Create frames for different forms
        self.create_frames()

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
        uproduktiv_menu.add_command(label="Intern Møde", command=lambda: self.load_form('Uproduktiv Tid'))
        uproduktiv_menu.add_command(label="Intern Kursus", command=lambda: self.load_form('Uproduktiv Tid'))
        uproduktiv_menu.add_command(label="Extern Kursus", command=lambda: self.load_form('Uproduktiv Tid'))
        menubar.add_cascade(label="Uproduktiv Tid", menu=uproduktiv_menu)

        # "Free days" Menu
        free_days_menu = tk.Menu(menubar, tearoff=0)
        free_days_menu.add_command(label="Ferie", command=lambda: self.load_form('Uproduktiv Tid'))
        free_days_menu.add_command(label="Sygdom", command=lambda: self.load_form('Uproduktiv Tid'))
        free_days_menu.add_command(label="Barns sygedag", command=lambda: self.load_form('Uproduktiv Tid'))
        free_days_menu.add_command(label="Afspasering", command=lambda: self.load_form('Uproduktiv Tid'))
        menubar.add_cascade(label="Free days", menu=free_days_menu)

        self.config(menu=menubar)

    def create_frames(self):
        self.form_configs = {
            'Internal commissioning': {
                'fields': [
                    {'label': 'Order Type', 'type': 'text_readonly', 'var': tk.StringVar(), 'default': 'Sag'},
                    {'label': 'Order Number', 'type': 'ordernumber_combobox', 'var': tk.StringVar()},
                    {'label': 'Order Name', 'type': 'label', 'var': self.order_name_var},
                    {'label': 'Order Line', 'type': 'combobox', 'options': ['Software', 'Intern Indkøring', 'Extern Indkøring', 'Kørsel/Rejsetid'], 'var': tk.StringVar(), 'default': 'Intern Indkøring'},
                    {'label': 'Date', 'type': 'date_entry', 'var': tk.StringVar()},
                    {'label': 'Time (H:M:S)', 'type': 'time_entry', 'var': tk.StringVar(), 'default': '08:00:00'},
                    {'label': 'Description', 'type': 'text', 'var': tk.StringVar()},
                ]
            },
            'External commissioning': {
                'fields': [
                    {'label': 'Order Type', 'type': 'text_readonly', 'var': tk.StringVar(), 'default': 'Sag'},
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
                    {'label': 'Order Type', 'type': 'text_readonly', 'var': tk.StringVar(), 'default': 'Sag'},
                    {'label': 'Order Number', 'type': 'ordernumber_combobox', 'var': tk.StringVar()},
                    {'label': 'Order Name', 'type': 'label', 'var': self.order_name_var},
                    {'label': 'Order Line', 'type': 'combobox', 'options': ['Software', 'Intern Indkøring', 'Extern Indkøring', 'Kørsel/Rejsetid'], 'var': tk.StringVar(), 'default': 'Software'},
                    {'label': 'Date', 'type': 'date_entry', 'var': tk.StringVar()},
                    {'label': 'Time (H:M:S)', 'type': 'time_entry', 'var': tk.StringVar(), 'default': '08:00:00'},
                    {'label': 'Description', 'type': 'text', 'var': tk.StringVar()},
                ]
            },
            'Driving': {
                'fields': [
                    {'label': 'Date', 'type': 'date_entry', 'var': tk.StringVar()},
                    {'label': 'Driving Time (H:M:S)', 'type': 'time_entry', 'var': tk.StringVar()},
                    {'label': 'Description', 'type': 'text', 'var': tk.StringVar()},
                ]
            },
            'Uproduktiv Tid': {
                'fields': [
                    {'label': 'Date', 'type': 'date_entry', 'var': tk.StringVar()},
                    {'label': 'Time (H:M:S)', 'type': 'time_entry', 'var': tk.StringVar()},
                    {'label': 'Description', 'type': 'text', 'var': tk.StringVar()},
                ]
            },
            
        }

    def load_form(self, task_name):
        self.current_task = task_name
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = tk.Frame(self)
        self.current_frame.pack(fill='both', expand=True)
        self.generate_form(self.form_configs[task_name])
        self.geometry("600x600")

    def generate_form(self, config):
        for idx, field in enumerate(config['fields']):
            label = tk.Label(self.current_frame, text=field['label'])
            label.grid(row=idx, column=0, padx=10, pady=5, sticky='w')

            field_var = field['var']
            default_value = field.get('default', '')

            if field['type'] == 'entry':
                entry = tk.Entry(self.current_frame, textvariable=field_var)
                entry.grid(row=idx, column=1, padx=10, pady=5)
                field_var.set(default_value)
            elif field['type'] == 'combobox':
                combobox = ttk.Combobox(self.current_frame, textvariable=field_var, values=field.get('options', []))
                combobox.grid(row=idx, column=1, padx=10, pady=5)
                combobox.set(default_value)
            elif field['type'] == 'ordernumber_combobox':
                ordernumber = ttk.Combobox(self.current_frame, textvariable=field_var, values=list(self.order_numbers.keys()))
                ordernumber.grid(row=idx, column=1, padx=10, pady=10)
                ordernumber.bind("<<ComboboxSelected>>", self.populate_order_number)
                ordernumber.bind("<FocusOut>", self.check_new_order_number)
                field['widget'] = ordernumber  # Store the widget reference
                self.order_number_combobox = ordernumber  # For later access
            elif field['type'] == 'time_entry':
                entry = tk.Entry(self.current_frame, textvariable=field_var)
                entry.grid(row=idx, column=1, padx=10, pady=5)
                entry.bind('<KeyRelease>', lambda event, e=entry: self.format_time_entry(event, e))
                field_var.set(default_value)
            elif field['type'] == 'date_entry':
                date_entry = DateEntry(self.current_frame, textvariable=field_var, width=12, background='darkblue', foreground='white', borderwidth=2)
                date_entry.grid(row=idx, column=1, padx=10, pady=5)
                if default_value:
                    date_entry.set_date(datetime.strptime(default_value, '%Y-%m-%d'))
                else:
                    date_entry.set_date(datetime.now())
                field['widget'] = date_entry  # Store reference
            elif field['type'] == 'label':
                if field.get('default'):
                    # For static text labels
                    static_label = tk.Label(self.current_frame, text=field['default'], anchor='w')
                    static_label.grid(row=idx, column=1, padx=10, pady=5, sticky='w')
                    field['widget'] = static_label
                else:
                    # For dynamic labels like 'Order Name'
                    dynamic_label = tk.Label(self.current_frame, textvariable=field['var'], anchor='w')
                    dynamic_label.grid(row=idx, column=1, padx=10, pady=5, sticky='w')
                    field['widget'] = dynamic_label
            elif field['type'] == 'text_readonly':
                # Multi-line uneditable text using a read-only Text widget
                text_widget = tk.Text(self.current_frame, height=4, width=30)
                text_widget.grid(row=idx, column=1, padx=10, pady=5)
                text_widget.insert('1.0', default_value)
                text_widget.config(state='disabled')  # Make it read-only
                field['widget'] = text_widget  # Store reference for later use
            elif field['type'] == 'text':
                text_widget = tk.Text(self.current_frame, height=4, width=30)
                text_widget.grid(row=idx, column=1, padx=10, pady=5)
                text_widget.insert('1.0', default_value)
                field['widget'] = text_widget  # Store reference for later use


        # Add Submit Button
        submit_button = tk.Button(self.current_frame, text="Submit", command=self.submit_form)
        submit_button.grid(row=len(config['fields']), column=1, padx=10, pady=10, sticky='e')

        # Add Reset Button
        reset_button = tk.Button(self.current_frame, text="Reset", command=self.reset_to_defaults)
        reset_button.grid(row=len(config['fields']), column=0, padx=10, pady=10, sticky='w')

    def format_time_entry(self, event, entry_widget):
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
                field_var.set(default_value)
    
    def load_order_numbers(self):
        # Load order numbers from file or initialize empty dict
        if os.path.exists(self.order_numbers_file):
            with open(self.order_numbers_file, 'r') as f:
                self.order_numbers = json.load(f)
        else:
            self.order_numbers = {}  # Format: {"Order Number": "Order Name"}

    def save_order_numbers(self):
        with open(self.order_numbers_file, 'w') as f:
            json.dump(self.order_numbers, f)

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
                self.save_order_numbers()
                self.order_name_var.set(order_name)
            else:
                messagebox.showinfo("Info", "Order Number not added.")
                event.widget.set('')  # Clear the invalid entry
                self.order_name_var.set("")

    def submit_form(self):
        config = self.form_configs[self.current_task]
        data = {'Task': self.current_task}
        for field in config['fields']:
            if field['type'] == 'text':
                text_content = field['widget'].get("1.0", tk.END).strip()
                data[field['label']] = text_content
            else:
                data[field['label']] = field['var'].get()

        # Map the order line name to its number
        order_line = data.get('Order Line')
        order_line_number = order_line_mapping.get(order_line, None)
        if not order_line_number:
            messagebox.showerror("Input Error", f"Order Line '{order_line}' is not valid.")
            return
        data['Order Line'] = order_line_number

        # Pass the data to AutomationHelper
        automation = AutomationHelper(data)
        result = automation.perform_automation()
        if result:
            messagebox.showerror("Automation Error", result)
        else:
            messagebox.showinfo("Automation", "The data has been submitted to the application.")


if __name__ == "__main__":
    import tkinter.simpledialog as simpledialog
    app = OrderForm()
    app.mainloop()
