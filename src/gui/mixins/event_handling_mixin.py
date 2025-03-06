from pynput import mouse, keyboard
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener, Key
from tkinter import messagebox

class EventHandlingMixin:
    def start_event_listeners(self):
        """Start mouse and keyboard listeners for CTRL + Left Click."""
        self.mouse_listener = MouseListener(on_click=self.on_mouse_click)
        self.keyboard_listener = KeyboardListener(
            on_press=self.on_key_press,
            on_release=self.on_key_release
        )
        self.mouse_listener.start()
        self.keyboard_listener.start()
        messagebox.showinfo("Automation", "Ready to import all entries. CTRL + Left Click a column in Navision to start.")

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

        from automation import AutomationHelper
        automation = AutomationHelper(self.formhandler)
        result = automation.perform_automation()
        if result:
            messagebox.showerror("Automation Error", result)
        else:
            messagebox.showinfo("Automation", "All entries have been submitted to the application.")
            # Clear entries after processing
            self.formhandler.data_list = []
            self.refresh_entries_tree()

    def on_closing(self):
        """Stop listeners and close the application."""
        self.stop_event_listeners()
        self.destroy()
