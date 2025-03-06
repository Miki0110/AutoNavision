import tkinter as tk
from .mixins.ui_setup_mixin import UiSetupMixin
from .mixins.form_handling_mixin import FormHandlingMixin
from .mixins.event_handling_mixin import EventHandlingMixin
from .mixins.treeview_mixin import TreeViewMixin
from formHandler import FormHandler
from config.config_handler import get_config
from .forms_config import create_form_configs

class OrderForm(tk.Tk,
                UiSetupMixin,
                FormHandlingMixin,
                EventHandlingMixin,
                TreeViewMixin): # Inherit from the mixins
    def __init__(self):
        super().__init__()
        self.title("Order Entry Form")

        # Data / config
        self.formhandler = FormHandler(self)
        self.value_config = get_config()
        self.current_task = None
        
        # Shared properties needed by mixins
        self.order_numbers = self.value_config["order_numbers"]
        self.unproductive_number = self.value_config["defaults"]["unproductive_number"]
        self.order_line_mapping = self.value_config["order_line_mapping"]
        self.ctrl_pressed = False  # used by event listeners
        self.mouse_listener = None
        self.keyboard_listener = None

        self.order_name_var = tk.StringVar()

        # Min window size
        self.minsize(400, 150)

        # Create the menu bar
        self.create_menu()

        # Main frame
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill='both', expand=True)

        # Prepare a placeholder form_frame
        self.form_frame = tk.Frame(self.main_frame)
        self.form_frame.grid(row=0, column=0, sticky='nsew')

        # Create buttons frame
        self.create_buttons_frame()
        self.buttons_frame.grid(row=1, column=0, sticky='nsew')

        # Create entries frame
        self.create_entries_frame()

        # Grid weights
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=0)
        self.main_frame.grid_rowconfigure(2, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Load form configs (dictionary) 
        self.form_configs = create_form_configs(self.order_name_var)

