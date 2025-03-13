import tkinter as tk
from tkinter import messagebox

class TreeViewMixin:
    def show_context_menu(self, event):
        item = self.entries_tree.identify_row(event.y)
        if item:
            self.entries_tree.selection_set(item)
            try:
                self.context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                self.context_menu.grab_release()

    def delete_entry(self):
        selected_item = self.entries_tree.selection()
        if selected_item:
            confirm = messagebox.askyesno("Delete Entry", "Are you sure you want to delete the selected entry?")
            if confirm:
                values = self.entries_tree.item(selected_item, "values")
                index = int(values[0])
                self.formhandler.remove_form(index)
                self.formvalues.pop(index)
                self.refresh_entries_tree()
        else:
            messagebox.showwarning("No Selection", "No entry selected.")
    
    def load_entry(self):
        selected_item = self.entries_tree.selection()
        index = int(self.entries_tree.item(selected_item, "values")[0])
        values = self.formvalues[index]

        self.load_form(values["task_name"])
        config = self.form_configs[self.current_task]
        for field in config['fields']:
            if field['type'] != 'checkbox':
                value = values['config_values'][field['label']]
                field['var'].set(value)

    def refresh_entries_tree(self):
        # Clear existing Treeview entries
        self.entries_tree.delete(*self.entries_tree.get_children())

        # Populate Treeview from FormHandler
        for i, item in enumerate(self.formhandler):
            total_hours = (
                item["Normal Hours"] +
                item["Overwork 1 Hours"] +
                item["Overwork 2 Hours"] +
                item["Normal Driving"] +
                item["Overwork 1 Driving"] +
                item["Overwork 2 Driving"]
            )
            self.entries_tree.insert(
                '', 'end',
                values=(i, item["Date"], item["Number"], item["Line"], f'{total_hours:.2f}')
            )