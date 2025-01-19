import pyautogui
import time
from pywinauto import Application, Desktop
import sys, os
from datetime import datetime

class AutomationHelper:
    """
    Helper class for automating tasks in Microsoft Dynamics NAV.
    """
    def __init__(self, data):
        self.orders = data['Orders']
        self.data = None
        self.app = self._connect_to_app()
        self.screen_width, self.screen_height = pyautogui.size()
        self.image_folder = self._set_image_folder()
        pyautogui.FAILSAFE = False
    
    def bring_app_to_foreground(self):
        # Bring the application window in focus
        if self.app is not None:
            try:
                self.app.top_window().set_focus()
                print("Application window is now in focus.")
                return True
            except Exception as e:
                print(f"Error bringing application to foreground: {e}")
                return False
        else:
            print("Application is not connected.")
            return False

    def _set_image_folder(self):
        # Set up the image folder path
        parent_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(parent_folder, 'images')

    def _connect_to_app(self):
        try:
            app = Application(backend='uia').connect(title_re='.*Microsoft Dynamics NAV.*')
            print("Connected to application.")
            return app
        except Exception as e:
            print(f"Could not connect to application: {e}")
            return None

    def locate_button(self, image_name, confidence=0.97):
        # Locate a button or field based on its image
        try:
            button_img = os.path.join(self.image_folder, image_name)
            button_location = pyautogui.locateCenterOnScreen(button_img, confidence=confidence)
            if button_location:
                return button_location
            else:
                return None
        except Exception as e:
            print(f"Error locating '{image_name}': {e}")
            return None

    def find_and_click_button(self, image_names, confidence=0.85):
        for image_name in image_names:
            image_path = os.path.join(self.image_folder, image_name)
            try:
                location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
                if location:
                    pyautogui.click(location)
                    print(f"Clicked {image_name}")
                    return True
            except Exception as e:
                pass
        print(f"Button not found in the list: {image_names}")
        return False


    def open_multiklade(self):
        time.sleep(0.2)
        # Go to the "Sager" menu trough shortcuts
        pyautogui.hotkey('ctrl', '5')
        time.sleep(0.2)

        # Find all images containing the word "Multiklade"
        multiklade_images = []
        for image_name in os.listdir(self.image_folder):
            if 'multiklade' in image_name.lower():
                multiklade_images.append(image_name)
        print(multiklade_images)
        # Locate and click the "Multiklade" button
        if not self.find_and_click_button(multiklade_images):
            print("Failed to click the 'Multiklade' button.")
            return False

        time.sleep(0.2)

        return True

    def type_hours(self, hours_float):
        # Convert the float hours to the required string format (1.2 -> "1,2")
        formatted_hours = self.convert_float_to_comma_string(hours_float)
        # Max 2 decimal places
        if len(formatted_hours.split(',')[1]) > 2:
            formatted_hours = formatted_hours[:formatted_hours.rfind(',') + 3]
        # Simulate typing the formatted string
        pyautogui.typewrite(formatted_hours)

    def insert_values(self):
        if not self.app:
            print("Application is not connected. Exiting automation.")
            return False

        # Step 1: Press down arrow keys
        # Press down 5 times and left 20 times to reach the date field
        for _ in range(5):
            pyautogui.press('down')
            time.sleep(0.1)
        
        for _ in range(20):
            pyautogui.press('left')
            time.sleep(0.01)
        # Step 2: Enter the date (format dd-mm-yy)
        pyautogui.typewrite(self.data['date'])
        time.sleep(0.1)

        # Step 3: Press Tab and enter order type
        pyautogui.press('tab')
        time.sleep(0.1)
        pyautogui.typewrite(self.data['order_type'])
        time.sleep(0.1)

        # Step 4: Press Tab and enter order number
        pyautogui.press('tab')
        time.sleep(0.1)
        pyautogui.typewrite(self.data['order_number'])
        time.sleep(0.1)

        # Step 5: Press Tab twice and enter order line
        pyautogui.press('tab', presses=2, interval=0.1)
        pyautogui.typewrite(self.data['order_line'])
        time.sleep(0.1)

        # Step 6: Press Tab 5 times to reach Description
        pyautogui.press('tab', presses=5, interval=0.1)
        if self.data['description']:
            pyautogui.typewrite(self.data['description'])
            time.sleep(0.1)
        else:
            # Skip typing if no description
            pass

        # Step 7: Press Tab and enter normal hours
        pyautogui.press('tab')
        time.sleep(0.1)
        if self.data['hours_input']:
            normal, overwork1, overwork2 = self.calculate_hours()
            self.type_hours(normal)
            time.sleep(0.1)

            # Step 8: Handle overwork hours
            pyautogui.press('tab')
            time.sleep(0.1)
            if overwork1 > 0:
                self.type_hours(overwork1)
            pyautogui.press('tab')
            time.sleep(0.1)
            if overwork2 > 0:
                self.type_hours(overwork2)
        else:
            pyautogui.press('tab')
            time.sleep(0.1)
            pyautogui.press('tab')

        # Step 9: Press Tab to reach driving hours fields
        pyautogui.press('tab')
        time.sleep(0.1)
        # Enter normal driving hours
        if self.data['driving_hours_input']:
            normal_driving_hours, overwork_driving_hours = self.calculate_driving_hours()
            self.type_hours(normal_driving_hours)
            time.sleep(0.1)
            # Enter overwork driving hours if any
            pyautogui.press('tab')
            time.sleep(0.1)
            if overwork_driving_hours > 0:
                self.type_hours(overwork_driving_hours)

        print("Automation completed successfully.")
        return True

    def aggregate_hours_by_date(self):
        date_hours = {}
        for order in self.orders:
            date = order['date']
            total_hours = self.parse_time_to_decimal(order.get('hours_input', '0:0:0'))
            driving_hours = self.parse_time_to_decimal(order.get('driving_hours_input', '0:0:0'))
            date_hours.setdefault(date, {'work_hours': 0, 'driving_hours': 0})
            date_hours[date]['work_hours'] += total_hours
            date_hours[date]['driving_hours'] += driving_hours
        return date_hours


    def calculate_hours(self, overwork_limit_1=4):
        date = self.data['date']
        total_hours = self.date_hours[date]['work_hours']
        total_driving_hours = self.date_hours[date]['driving_hours']

        # Determine normal hours based on the date (5 or 8 hours)
        weekday = self.check_if_friday_or_weekend(date)
        if weekday == "Friday":
            max_normal_hours = 5
        elif weekday == "Weekend":
            max_normal_hours = 0
            overwork_limit_1 = 0
        else:
            max_normal_hours = 8

        # Total hours including driving
        cumulative_hours = 0
        combined_hours = total_hours + total_driving_hours
        overwork_hours = combined_hours - max_normal_hours
        overwork_hours = max(overwork_hours, 0)  # Ensure overwork is not negative

        # Split overwork hours
        overwork_1 = min(overwork_hours, overwork_limit_1)
        overwork_2 = max(overwork_hours - overwork_limit_1, 0)

        # Distribute normal hours and overwork hours proportionally
        entry_hours = self.parse_time_to_decimal(self.data.get('hours_input', '0:0:0'))
        if combined_hours > 0:
            normal_hours = (max_normal_hours * entry_hours) / combined_hours
            overwork_1_hours = (overwork_1 * entry_hours) / combined_hours
            overwork_2_hours = (overwork_2 * entry_hours) / combined_hours
        else:
            normal_hours = overwork_1_hours = overwork_2_hours = 0

        return normal_hours, overwork_1_hours, overwork_2_hours

    
    def calculate_driving_hours(self):
        weekday = self.check_if_friday_or_weekend(self.data['date'])
        if weekday == "Friday":
            max_normal_hours = 5
        elif weekday == "Weekend":
            max_normal_hours = 0
        else:
            max_normal_hours = 8
        # Assuming driving hours are separate from work hours
        total_driving_hours = self.parse_time_to_decimal(self.data['driving_hours_input'])
        total_work_hours = self.parse_time_to_decimal(self.data['hours_input'])

        # Calculate normal driving hours
        remaining_work_hours = max(total_work_hours - max_normal_hours, 0)
        normal_hours = min(total_driving_hours, remaining_work_hours)
        overwork_hours = max(total_driving_hours - normal_hours, 0)
        
        return normal_hours, overwork_hours

    def calculate_overwork_driving_hours(self, normal_driving_hours):
        # Calculate overwork driving hours if any
        total_driving_hours = self.parse_time_to_decimal(self.data['driving_hours_input'])
        remaining_driving_hours = total_driving_hours - float(normal_driving_hours)
        return max(remaining_driving_hours, 0)

    def parse_time_to_decimal(self, time_str):
        # Convert H:M:S format to decimal hours
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
            total_hours = hours + minutes / 60 + seconds / 3600
            return total_hours
        except ValueError:
            print("Invalid time format. Please use H:M:S.")
            return 0

    def perform_automation(self):
        # Example automation steps
        if not self.app:
            print("Application is not opne. Please open Navision and try again.")
            return "Application not connected."

        if not self.bring_app_to_foreground():
            print("Error, Could not bring application to foreground. Exiting automation.")
            return "Could not bring application to foreground"
        
        # Aggregate hours by date
        self.date_hours = self.aggregate_hours_by_date()
        
        if not self.open_multiklade():
            print("Could not find the Multiklade. Exiting automation.\n To improve this feature, take a screenshot of the Multiklade and Sager buttons and place them in the 'images' folder with corresponding names.")
            return "Could not find Multiklade."
        # Process each order
        for order in self.orders:
            self.data = order  # Set current order data
            if not self.insert_values():
                print("Could not insert values for an entry. Exiting automation.")
                return "Could not insert values for an entry."
        else:
            print("Could not open Multiklade. Exiting automation.")
            return "Could not find Multiklade."
    
    @staticmethod
    def check_if_friday_or_weekend(date_str):
        # Convert the date string to a datetime
        date_obj = datetime.strptime(date_str, '%d-%m-%y')

        day_of_week = date_obj.weekday()

        # Check if it's Friday (4) or Weekend (5 or 6)
        if day_of_week == 4:
            return "Friday"
        elif day_of_week == 5 or day_of_week == 6:
            return "Weekend"
        else:
            return -1
