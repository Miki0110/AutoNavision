import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import re
from datetime import datetime, timedelta

class FormHandlingMixin:
    def load_form(self, task_name):
        """Load the specified form configuration into self.form_frame."""
        self.current_task = task_name
        if self.form_frame:
            self.form_frame.destroy()

        self.form_frame = tk.Frame(self.main_frame)
        self.form_frame.grid(row=0, column=0, sticky='nsew')

        # Generate the form fields based on self.form_configs
        self.generate_form(self.form_configs[task_name])

        # Update window size
        self.update_idletasks()
        self.geometry('')


    def generate_form(self, config):
        """Dynamically create form widgets from the config dictionary."""
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
                from tkinter import ttk
                combobox = ttk.Combobox(self.form_frame, textvariable=field_var, values=field.get('options', []))
                combobox.grid(row=idx, column=1, padx=10, pady=5)
                combobox.set(default_value)

            elif field['type'] == 'ordernumber_combobox':
                from tkinter import ttk
                ordernumber = ttk.Combobox(self.form_frame, textvariable=field_var, values=list(self.order_numbers.keys()))
                ordernumber.grid(row=idx, column=1, padx=10, pady=10)
                ordernumber.bind("<<ComboboxSelected>>", self.populate_order_number)
                ordernumber.bind("<FocusOut>", self.check_new_order_number)
                field['widget'] = ordernumber
                self.order_number_combobox = ordernumber

            elif field['type'] == 'time_entry':
                entry = tk.Entry(self.form_frame, textvariable=field_var)
                entry.grid(row=idx, column=1, padx=10, pady=5)
                # Format time while typing
                entry.bind('<KeyRelease>', lambda event, e=entry: self.format_time_entry(event, e))
                field_var.set(default_value)

            elif field['type'] == 'date_entry':
                date_entry = DateEntry(
                    self.form_frame, textvariable=field_var, width=12,
                    background='darkblue', foreground='white', borderwidth=2
                )
                date_entry.grid(row=idx, column=1, padx=10, pady=5)

                if default_value:
                    # Attempt to parse default_value if it's a str like '2023-01-01'
                    try:
                        date_entry.set_date(datetime.strptime(default_value, '%Y-%m-%d'))
                    except:
                        date_entry.set_date(datetime.now())
                else:
                    date_entry.set_date(datetime.now())

                field['widget'] = date_entry

                # If 'state' is 'disabled', disable widget
                if field.get('state') == 'disabled':
                    date_entry.config(state='disabled')

            elif field['type'] == 'label':
                if field.get('default'):
                    # Static label
                    static_label = tk.Label(self.form_frame, text=field['default'], anchor='w')
                    static_label.grid(row=idx, column=1, padx=10, pady=5, sticky='w')
                    field['widget'] = static_label
                else:
                    # Dynamic label (like "Order Name")
                    dynamic_label = tk.Label(self.form_frame, textvariable=field_var, anchor='w')
                    dynamic_label.grid(row=idx, column=1, padx=10, pady=5, sticky='w')
                    field['widget'] = dynamic_label

            elif field['type'] == 'text':
                text_widget = tk.Text(self.form_frame, height=4, width=30)
                text_widget.grid(row=idx, column=1, padx=10, pady=5)
                text_widget.insert('1.0', default_value)
                field['widget'] = text_widget

            elif field['type'] == 'checkbox':
                checkbox = tk.Checkbutton(self.form_frame, variable=field_var)
                checkbox.grid(row=idx, column=1, padx=10, pady=5, sticky='w')
                field['widget'] = checkbox
                if field['label'] == 'Multiple Days':
                    field_var.set(field.get('default', False))
                    # This toggles the end date between enabled/disabled
                    field_var.trace('w', self.multiple_days_toggled)

        self.update_idletasks()
        self.geometry('')


    def add_entry(self):
        """Collect user input from the current form and add it to formhandler."""
        config = self.form_configs[self.current_task]
        multiple_days = False
        end_date = None
        order_template = {}

        # Check if 'Multiple Days' is active
        for field in config['fields']:
            if field['label'] == 'Multiple Days':
                multiple_days = field['var'].get()
                break

        start_date = None
        for field in config['fields']:
            label = field['label']
            if label == 'Order Type':
                order_template['type'] = field['var'].get()
            elif label == 'Order Number':
                order_template['number'] = field['var'].get() or self.unproductive_number
            elif label == 'Order Line':
                order_line = field['var'].get()
                order_template['line'] = self.order_line_mapping.get(order_line, None)
                if not order_template['line']:
                    messagebox.showerror("Order Line Error", f"Order Line '{order_line}' is not valid.")
                    return
            elif label == 'Date':
                start_date = field['widget'].get_date()
            elif label == 'End Date':
                if multiple_days:
                    end_date = field['widget'].get_date()
            elif label == 'Time (H:M:S)':
                time_str = field['var'].get() or "00:00:00"
                order_template['work_hours_used'] = self.convert_time_to_hours(time_str)
            elif label == 'Driving Time (H:M:S)':
                driving_str = field['var'].get() or "00:00:00"
                order_template['driving_hours_used'] = self.convert_time_to_hours(driving_str)
            elif label == 'Description':
                order_template['description'] = field['widget'].get('1.0', tk.END).strip()

        # Ensure entries_frame is visible
        if not self.entries_frame.winfo_ismapped():
            self.entries_frame.grid(row=2, column=0, sticky='nsew')
            self.update_idletasks()
            self.geometry('')

        # Create form entries in formHandler
        if multiple_days and end_date and end_date >= start_date:
            delta = (end_date - start_date).days + 1
            for i in range(delta):
                cur_date = (start_date + timedelta(days=i)).strftime('%d-%m-%y')
                self.formhandler.add_form(
                    date=cur_date,
                    type=order_template['type'],
                    number=order_template['number'],
                    name=self.order_numbers.get(order_template['number'], ""),
                    line=order_template['line'],
                    work_hours_used=order_template.get('work_hours_used', 0),
                    driving_hours_used=order_template.get('driving_hours_used', 0),
                    description=order_template.get('description', "")
                )
        else:
            # Single day
            self.formhandler.add_form(
                date=start_date.strftime('%d-%m-%y') if start_date else '',
                type=order_template['type'],
                number=order_template['number'],
                name=self.order_numbers.get(order_template['number'], ""),
                line=order_template['line'],
                work_hours_used=order_template.get('work_hours_used', 0),
                driving_hours_used=order_template.get('driving_hours_used', 0),
                description=order_template.get('description', "")
            )

        self.refresh_entries_tree()
        self.reset_to_defaults()
        messagebox.showinfo("Entry Added", "The entry has been added.")


    def reset_to_defaults(self):
        """Reset the form fields to their default values."""
        config = self.form_configs[self.current_task]
        for field in config['fields']:
            default_value = field.get('default', '')
            field_var = field['var']

            if field['type'] in ['label', 'text_readonly']:
                continue

            if field['type'] == 'date_entry':
                if field['label'] == 'End Date':
                    # Turn off multiple days
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
        """When an order number is selected, populate the order name."""
        selected_order_number = event.widget.get()
        order_name = self.order_numbers.get(selected_order_number, "")
        self.order_name_var.set(order_name)


    def check_new_order_number(self, event):
        """If user typed a new order number, ask for a name and update config."""
        current_value = event.widget.get()
        if current_value and current_value not in self.order_numbers:
            import tkinter.simpledialog as simpledialog
            order_name = simpledialog.askstring(
                "New Order Number", 
                f"Enter a name for Order Number '{current_value}':"
            )
            if order_name:
                self.order_numbers[current_value] = order_name
                self.order_number_combobox.config(values=list(self.order_numbers.keys()))
                self.value_config['order_numbers'] = self.order_numbers
                from config.config_handler import update_config
                update_config(self.value_config)
                self.order_name_var.set(order_name)
            else:
                messagebox.showinfo("Info", "Order Number not added.")
                event.widget.set('')
                self.order_name_var.set("")


    def multiple_days_toggled(self, *args):
        """Enable or disable the 'End Date' field based on the 'Multiple Days' checkbox."""
        multiple_days_checked = False
        end_date_widget = None
        for field in self.form_configs[self.current_task]['fields']:
            if field['label'] == 'Multiple Days':
                multiple_days_checked = field['var'].get()
            if field['label'] == 'End Date':
                end_date_widget = field['widget']
        if end_date_widget:
            if multiple_days_checked:
                end_date_widget.config(state='normal')
            else:
                end_date_widget.config(state='disabled')


    def format_time_entry(self, event, entry_widget):
        """Dynamically format a time entry widget as HH:MM:SS."""
        if event.keysym in ('BackSpace', 'Delete', 'Tab'):
            return
        import re
        content = entry_widget.get()
        # Remove non-digit
        content = re.sub(r'\D', '', content)
        content = content[:6]  # HHMMSS
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
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, formatted)


    def convert_time_to_hours(self, time_str):
        h, m, s = map(int, time_str.split(":"))
        return h + m/60 + s/3600
