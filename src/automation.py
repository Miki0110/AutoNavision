import pyautogui
import time
from formHandler import FormHandler
from pynput import mouse, keyboard
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener, Key

class AutomationHelper:
    """
    Helper class for automating tasks in Microsoft Dynamics NAV.
    """
    def __init__(self, formhandler):
        self.formhandler = formhandler
        self.data = None
        pyautogui.FAILSAFE = False
        
        # Flag to control whether we should stop mid-automation
        self.stop_requested = False

        # We'll create listeners that set `stop_requested` to True if user clicks or presses a key
        self.mouse_listener = MouseListener(on_click=self.on_mouse_click)
        self.keyboard_listener = KeyboardListener(on_press=self.on_key_press)

    def on_mouse_click(self, x, y, button, pressed):
        if pressed:
            self.stop_requested = True

    def on_key_press(self, key):
        # If user presses ESC, for instance, we stop
        if key == Key.esc:
            self.stop_requested = True

    def start_listeners(self):
        """Start the mouse and keyboard listeners in non-blocking mode."""
        self.mouse_listener.start()
        self.keyboard_listener.start()

    def stop_listeners(self):
        """Stop the mouse/keyboard listeners."""
        self.mouse_listener.stop()
        self.keyboard_listener.stop()

    def perform_automation(self):
        # Start our listeners
        self.start_listeners()
        try:
            for item in self.formhandler:
                # If at any time stop is requested, break
                if self.stop_requested:
                    print("User interrupt detected. Stopping automation.")
                    return "User interrupt"

                self.data = item
                inserted = self.insert_values()

                if not inserted:
                    print("Could not insert values for an entry. Exiting automation.")
                    return "Could not insert values for an entry."

                # Again, check if user requested stop between each item
                if self.stop_requested:
                    print("User interrupt detected. Stopping automation.")
                    return "User interrupt"

        finally:
            # Always stop listeners, even if there was an exception
            self.stop_listeners()
    
    def type_hours(self, hours_str):
        # Convert the float hours to the required string format (1.2 -> "1,2")
        hours_str = self.float_to_string(hours_str)
        if len(hours_str.split(',')[1]) > 2:
            hours_str = hours_str[:hours_str.rfind(',') + 3]
        # Simulate typing the formatted string
        pyautogui.typewrite(hours_str)

    def insert_values(self):
        time.sleep(0.1)
        # Step 1: Press down arrow keys
        pyautogui.press('down', presses=3, interval=0.1)
        # Press left until it's the first field
        pyautogui.press('left', presses=30, interval=0.1)

        # Step 2: Enter the date (format dd-mm-yy)
        pyautogui.typewrite(self.data['Date'])
        time.sleep(0.1)

        # Step 3: Press Tab and enter order type
        pyautogui.press('tab')
        time.sleep(0.1)
        pyautogui.typewrite(self.data['Type'])
        time.sleep(0.1)

        # Step 4: Press Tab and enter order number
        pyautogui.press('tab')
        time.sleep(0.1)
        pyautogui.typewrite(self.data['Number'])
        time.sleep(0.1)

        # Step 5: Press Tab twice and enter order line
        pyautogui.press('tab', presses=2, interval=0.1)
        time.sleep(0.1)
        pyautogui.typewrite(self.data['Line'])
        time.sleep(0.1)

        # Step 6: Press Tab 5 times to reach Description
        pyautogui.press('tab', presses=5, interval=0.1)
        if self.data['Description']:
            pyautogui.typewrite(self.data['Description'])
        else:
            # Skip typing if no description
            pass

        # Step 7: Press Tab and enter normal hours
        time.sleep(0.1)
        pyautogui.press('tab')
        time.sleep(0.1)
        if (self.data["Normal Hours"] + self.data["Overwork 1 Hours"] + self.data["Overwork 2 Hours"]) > 0:
            if self.data["Normal Hours"] > 0:
                self.type_hours(self.data["Normal Hours"])
            time.sleep(0.1)

            # Step 8: Handle overwork hours
            pyautogui.press('tab')
            time.sleep(0.1)
            if self.data["Overwork 1 Hours"] > 0:
                self.type_hours(self.data["Overwork 1 Hours"])
            time.sleep(0.1)
            pyautogui.press('tab')
            time.sleep(0.1)
            if self.data["Overwork 2 Hours"] > 0:
                self.type_hours(self.data["Overwork 2 Hours"])
        else:
            pyautogui.press('tab', presses=2, interval=0.1)

        # Step 9: Press Tab to reach driving hours fields
        time.sleep(0.1)
        pyautogui.press('tab')
        time.sleep(0.1)
        # Enter normal driving hours
        if (self.data["Normal Driving"] + self.data["Overwork 1 Driving"] + self.data["Overwork 2 Driving"]) > 0:
            if self.data["Normal Driving"] > 0:
                self.type_hours(self.data["Normal Driving"])
            time.sleep(0.1)
            # Enter overwork driving hours if any
            pyautogui.press('tab')
            time.sleep(0.1)
            if self.data["Overwork 1 Driving"] > 0:
                self.type_hours(self.data["Overwork 1 Driving"])
            time.sleep(0.1)
            pyautogui.press('tab')
            time.sleep(0.1)
            if self.data["Overwork 2 Driving"] > 0:
                self.type_hours(self.data["Overwork 2 Driving"])
        else:
            pyautogui.press('tab', presses=2, interval=0.1)
        time.sleep(0.1)
        pyautogui.press('tab', presses=2, interval=0.1)
        time.sleep(0.1)

        # Step 10: Insert the car plate
        if self.data["plate"]:
            pyautogui.press('tab')
            time.sleep(0.1)
            pyautogui.typewrite(self.data["plate"])
        else:
            time.sleep(0.1)
            pyautogui.press('tab')
        
        # Step 11: Insert the addresses
        if self.data["to_address"]:
            time.sleep(0.1)
            pyautogui.press('tab', presses=2, interval=0.1)
            time.sleep(0.1)
            pyautogui.typewrite(self.data["to_address"])
        else:
            time.sleep(0.1)
            pyautogui.press('tab', presses=2, interval=0.1)
        
        if self.data["from_address"]:
            time.sleep(0.1)
            pyautogui.press('tab', presses=2, interval=0.1)
            time.sleep(0.1)
            pyautogui.typewrite(self.data["from_address"])

        time.sleep(0.1)
        print("Automation completed successfully.")
        return True      
        
    def float_to_string(self, input_float):
        # Format the float to a string with 2 decimal places
        formatted = f"{input_float:.2f}"
        # Replace the decimal point with a comma
        return formatted.replace(".", ",")