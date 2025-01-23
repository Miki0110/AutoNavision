import pyautogui
import time
from formHandler import FormHandler

class AutomationHelper:
    """
    Helper class for automating tasks in Microsoft Dynamics NAV.
    """
    def __init__(self, formhandler):
        self.formhandler = formhandler
        self.data = None
        pyautogui.FAILSAFE = False

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
        pyautogui.press('left', presses=20, interval=0.1)

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
        pyautogui.typewrite(self.data['Line'])
        time.sleep(0.1)

        # Step 6: Press Tab 5 times to reach Description
        pyautogui.press('tab', presses=5, interval=0.1)
        if self.data['Description']:
            pyautogui.typewrite(self.data['Description'])
            time.sleep(0.1)
        else:
            # Skip typing if no description
            pass

        # Step 7: Press Tab and enter normal hours
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
            pyautogui.press('tab')
            time.sleep(0.1)
            if self.data["Overwork 2 Hours"] > 0:
                self.type_hours(self.data["Overwork 2 Hours"])
        else:
            pyautogui.press('tab')
            time.sleep(0.1)
            pyautogui.press('tab')

        # Step 9: Press Tab to reach driving hours fields
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

        print("Automation completed successfully.")
        return True

    def perform_automation(self):
        # Process each order
        for item in self.formhandler:
            self.data = item
            if not self.insert_values():
                print("Could not insert values for an entry. Exiting automation.")
                return "Could not insert values for an entry."
        
        
    def float_to_string(self, input_float):
        # Format the float to a string with 2 decimal places
        formatted = f"{input_float:.2f}"
        # Replace the decimal point with a comma
        return formatted.replace(".", ",")