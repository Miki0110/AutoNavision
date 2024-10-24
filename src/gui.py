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
    """
    Order Entry Form using Tkinter

    Initialize the main window and form fields

    """
    def __init__(self):
        super().__init__()
        self.order_lines = ["Software", "Intern Indkøring", "Extern Indkøring", "Kursus Intern", "Kørsel/Rejsetid"] # Order line dropdown menu
        self.title("Order Entry Form")
        self.geometry("450x600")

        # Load order numbers from local file or initialize empty dict
        self.order_numbers_file = 'order_numbers.json'
        self.load_order_numbers()

        # Order Type Dropdown (Combobox)
        self.label_order_type = tk.Label(self, text="Order Type")
        self.label_order_type.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        self.order_type = ttk.Combobox(self, values=["Sag", "Service", "Produktion"])
        self.order_type.grid(row=0, column=1, padx=10, pady=10)
        self.order_type.current(0)  # Set default to the first option

        # Order Number Combobox
        self.label_order_number = tk.Label(self, text="Order Number")
        self.label_order_number.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        self.order_number_var = tk.StringVar()
        self.order_number = ttk.Combobox(self, textvariable=self.order_number_var, values=list(self.order_numbers.keys()))
        self.order_number.grid(row=1, column=1, padx=10, pady=10)
        self.order_number.bind("<<ComboboxSelected>>", self.populate_order_number)
        self.order_number.bind("<FocusOut>", self.check_new_order_number)

        # Display selected Order Number's name
        self.label_order_name = tk.Label(self, text="Order Name")
        self.label_order_name.grid(row=2, column=0, padx=10, pady=10, sticky='w')

        self.order_name_var = tk.StringVar()
        self.order_name_label = tk.Label(self, textvariable=self.order_name_var)
        self.order_name_label.grid(row=2, column=1, padx=10, pady=10, sticky='w')

        # Order Line Dropdown (Combobox)
        self.label_order_line = tk.Label(self, text="Order Line")
        self.label_order_line.grid(row=3, column=0, padx=10, pady=10, sticky='w')

        self.order_line_var = tk.StringVar()
        self.order_line = ttk.Combobox(self, textvariable=self.order_line_var, values=self.order_lines)
        self.order_line.grid(row=3, column=1, padx=10, pady=10)
        self.order_line.bind("<<ComboboxSelected>>", self.check_new_order_line)
        self.order_line.bind("<FocusOut>", self.check_new_order_line_focus_out)
        self.order_line.current(0)  # Set default to the first option

        # Date Input (DateEntry from tkcalendar)
        self.label_date = tk.Label(self, text="Date")
        self.label_date.grid(row=4, column=0, padx=10, pady=10, sticky='w')

        self.date_entry = DateEntry(self, width=12, background='darkblue',
                                    foreground='white', borderwidth=2)
        self.date_entry.grid(row=4, column=1, padx=10, pady=10)
        self.date_entry.set_date(datetime.now())  # Default to current date

        # Hours Input (Time Entry in H:M:S format)
        self.label_hours = tk.Label(self, text="Time (H:M:S)")
        self.label_hours.grid(row=5, column=0, padx=10, pady=10, sticky='w')

        self.hours = tk.Entry(self)
        self.hours.grid(row=5, column=1, padx=10, pady=10)
        self.hours.bind('<KeyRelease>', lambda event: self.format_time_entry(event, self.hours))

        # Driving Hours Input (Time Entry in H:M:S format)
        self.label_driving_hours = tk.Label(self, text="Driving Time (H:M:S)")
        self.label_driving_hours.grid(row=6, column=0, padx=10, pady=10, sticky='w')

        self.driving_hours = tk.Entry(self)
        self.driving_hours.grid(row=6, column=1, padx=10, pady=10)
        self.driving_hours.bind('<KeyRelease>', lambda event: self.format_time_entry(event, self.driving_hours))

        # Description Text Area
        self.label_description = tk.Label(self, text="Description")
        self.label_description.grid(row=7, column=0, padx=10, pady=10, sticky='w')

        self.description = tk.Text(self, height=4, width=30)
        self.description.grid(row=7, column=1, padx=10, pady=10)

        # Submit Button
        self.submit_button = tk.Button(self, text="Submit", command=self.submit_form)
        self.submit_button.grid(row=8, column=1, padx=10, pady=10, sticky='e')

        # Default Button
        self.default_button = tk.Button(self, text="Default", command=self.set_default_values)
        self.default_button.grid(row=8, column=0, padx=10, pady=10, sticky='w')

        # Indkøring Button
        self.indkoering_button = tk.Button(self, text="Indkøring", command=self.set_ind_values)
        self.indkoering_button.grid(row=9, column=0, padx=10, pady=10, sticky='w')

        # Kursus Button
        self.kursus_button = tk.Button(self, text="Kursus", command=self.set_kursus_values)
        self.kursus_button.grid(row=10, column=0, padx=10, pady=10, sticky='w')

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

    def populate_order_number(self, event=None):
        selected_order_number = self.order_number_var.get()
        order_name = self.order_numbers.get(selected_order_number, "")
        self.order_name_var.set(order_name)

    def check_new_order_number(self, event=None):
        current_value = self.order_number_var.get()
        if current_value and current_value not in self.order_numbers:
            # Prompt for the name of the Order Number
            order_name = simpledialog.askstring("New Order Number", f"Enter a name for Order Number '{current_value}':")
            if order_name:
                self.order_numbers[current_value] = order_name
                self.order_number.config(values=list(self.order_numbers.keys()))
                self.save_order_numbers()
                self.order_name_var.set(order_name)
            else:
                messagebox.showinfo("Info", "Order Number not added.")
                self.order_number_var.set("")  # Clear the invalid entry
                self.order_name_var.set("")

    def check_new_order_line(self, event=None):
        current_value = self.order_line_var.get()
        if current_value not in self.order_lines:
            response = messagebox.askyesno("New Order Line", f"'{current_value}' is not in the list. Add it?")
            if response:
                self.order_lines.append(current_value)
                self.order_line.config(values=self.order_lines)
                self.save_order_lines()

    def check_new_order_line_focus_out(self, event=None):
        self.check_new_order_line()

    def validate_time_input(self, action, value_if_allowed):
        if action == '1':  # Insert
            pattern = r'^(\d{0,2}(:\d{0,2}){0,2})?$'
            return re.match(pattern, value_if_allowed) is not None
        else:
            return True

    def parse_time_input(self, time_str):
        parts = time_str.strip().split(':')
        try:
            if len(parts) == 3:
                hours = int(parts[0])
                minutes = int(parts[1])
                seconds = int(parts[2])
            elif len(parts) == 2:
                hours = int(parts[0])
                minutes = int(parts[1])
                seconds = 0
            elif len(parts) == 1:
                hours = int(parts[0])
                minutes = 0
                seconds = 0
            else:
                raise ValueError("Invalid time format")
            return hours, minutes, seconds
        except ValueError:
            raise ValueError("Invalid time format")

    def format_time_entry(self, event, entry_widget):
        if event.keysym in ('BackSpace', 'Delete'):
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

    def parse_time_input(self, time_str):
        # Parse time input in H:M:S format
        parts = time_str.strip().split(':')
        try:
            hours = int(parts[0]) if len(parts) > 0 and parts[0] else 0
            minutes = int(parts[1]) if len(parts) > 1 and parts[1] else 0
            seconds = int(parts[2]) if len(parts) > 2 and parts[2] else 0
            return hours, minutes, seconds
        except ValueError:
            raise ValueError("Invalid time format")
        
    def set_default_values(self):
        # Set default values for fields
        self.order_type.set("Sag")
        # If the order number is already set, keep it
        if not self.order_number_var.get():
            # If not set it to the newest order number
            self.order_number_var.set(list(self.order_numbers.keys())[-1])
        self.order_line.set("Software")
        self.date_entry.set_date(datetime.now())
        self.hours.delete(0, tk.END)
        # Check if it's Friday or Weekend
        weekday = datetime.now().strftime('%A')
        if weekday == "Friday":
            self.hours.insert(0, "5:00:00")
        else:
            self.hours.insert(0, "8:00:00")
        self.driving_hours.delete(0, tk.END)
        self.driving_hours.insert(0, "0:00:00")
        self.description.delete("1.0", tk.END)

    def set_ind_values(self):
        # Set default values for fields
        self.order_type.set("Sag")
        # If the order number is already set, keep it
        if not self.order_number_var.get():
            # If not set it to the newest order number
            self.order_number_var.set(list(self.order_numbers.keys())[-1])
        self.order_line.set("Intern Indkøring")
        self.date_entry.set_date(datetime.now())
        self.hours.delete(0, tk.END)
        self.hours.insert(0, "8:00:00")
        self.driving_hours.delete(0, tk.END)
        self.driving_hours.insert(0, "0:00:00")
        self.description.delete("1.0", tk.END)

    def set_kursus_values(self):
        # Set default values for fields
        self.order_type.set("Sag")
        self.order_number_var.set("0240008")
        self.order_name_var.set(self.order_numbers.get("0240008", ""))
        self.order_line.set("Kursus Intern")
        self.date_entry.set_date(datetime.now())
        self.hours.delete(0, tk.END)
        self.hours.insert(0, "8:00:00")
        self.driving_hours.delete(0, tk.END)
        self.driving_hours.insert(0, "0:00:00")
        self.description.delete("1.0", tk.END)

    def submit_form(self):
        # Collect data from form fields
        order_type = self.order_type.get()
        order_number = self.order_number_var.get()
        order_name = self.order_name_var.get()
        order_line = self.order_line_var.get()
        date = self.date_entry.get_date().strftime('%d-%m-%y')
        hours_input = self.hours.get()
        driving_hours_input = self.driving_hours.get()
        description = self.description.get("1.0", tk.END).strip()


        # Validation checks
        # Ensure the order_line is translated into the corresponding number
        order_line_number = order_line_mapping.get(order_line, None)
        if not order_line_number:
            messagebox.showerror("Input Error", f"Order Line '{order_line}' is not valid.")
            return

        # Simple validation check
        if not order_number or not hours_input:
            messagebox.showerror("Input Error", "Order Number and Hours are required.")
            return

        # Parse time inputs
        try:
            hours_h, hours_m, hours_s = self.parse_time_input(hours_input)
            total_hours = hours_h + hours_m / 60 + hours_s / 3600
        except ValueError:
            messagebox.showerror("Input Error", "Invalid time format for Hours. Please use H:M:S.")
            return

        try:
            driving_h, driving_m, driving_s = self.parse_time_input(driving_hours_input)
            total_driving_hours = driving_h + driving_m / 60 + driving_s / 3600
        except ValueError:
            messagebox.showerror("Input Error", "Invalid time format for Driving Hours. Please use H:M:S.")
            return


        # Prepare data dictionary
        data = {
            'order_type': order_type,
            'order_number': order_number,
            'order_name': order_name,
            'order_line': order_line_number,
            'date': date,
            'hours_input': hours_input,
            'driving_hours_input': driving_hours_input,
            'description': description
        }

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
