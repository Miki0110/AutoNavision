import pandas as pd
from config.config_handler import get_config, update_config

class FormHandler:
    def __init__(self, form):
        self.form = form
        self.config = get_config()
        self.overwork1_limit = self.config["overwork_limits"]["overwork1"]
        self.data_list = []

    def add_form(self, date, type, number, name, line, work_hours_used, driving_hours_used, plate, to_address, from_address, description):
        # Append the new row to the DataFrame
        new_row = {
            "Date": date,
            "Type": type,
            "Number": number,
            "Name": name,
            "Line": line,
            "Normal Hours": 0,
            "Overwork 1 Hours": 0,
            "Overwork 2 Hours": 0,
            "Normal Driving":0,
            "Overwork 1 Driving": 0,
            "Overwork 2 Driving": 0,
            "plate": plate,
            "to_address": to_address,
            "from_address": from_address,
            "Description": description
        }
        # Calculate the work hours and overtime
        if driving_hours_used <= 0:
            entry_hours = self.calculate_hours(date, work_hours_used)
            new_row["Normal Hours"] = entry_hours["Normal Hours"]
            new_row["Overwork 1 Hours"] = entry_hours["Overwork 1 Hours"]
            new_row["Overwork 2 Hours"] = entry_hours["Overwork 2 Hours"]
        else:
            entry_hours = self.calculate_hours(date, driving_hours_used)
            new_row["Normal Driving"] = entry_hours["Normal Hours"]
            new_row["Overwork 1 Driving"] = entry_hours["Overwork 1 Hours"]
            new_row["Overwork 2 Driving"] = entry_hours["Overwork 2 Hours"]
            
        self.data_list.append(new_row)

    def calculate_hours(self, date_entry, hours_used):
        """
        Distribute new 'work_hours_used' and 'driving_hours_used' across
        Normal, Overwork 1, and Overwork 2 so that each category receives
        the correct proportion of driving vs. non-driving hours, while 
        respecting daily normal and overwork1 limits.
        """

        # Grab existing totals for date_entry (or zero if none)
        if self.len > 0:
            filtered_data = self.data_frame[self.data_frame["Date"] == date_entry]

            # Sum up existing hours for the given date
            normal_hours = filtered_data["Normal Hours"].sum() + filtered_data["Normal Driving"].sum()
            overwork1_hours = filtered_data["Overwork 1 Hours"].sum() + filtered_data["Overwork 1 Driving"].sum()
            overwork2_hours = filtered_data["Overwork 2 Hours"].sum() + filtered_data["Overwork 2 Driving"].sum()
        else:
            normal_hours = 0
            overwork1_hours = 0
            overwork2_hours = 0

        # Determine the normal hour limits based on the day of the week
        day_of_week = pd.Timestamp(date_entry).dayofweek  # 0 = Monday, ..., 6 = Sunday
        if day_of_week in [5, 6]:  # Weekend
            normal_limit = 0
            overwork1_limit = 0
        elif day_of_week == 4:  # Friday
            normal_limit = 5
            overwork1_limit = self.overwork1_limit
        else:  # Monday to Thursday
            normal_limit = 8
            overwork1_limit = self.overwork1_limit

        # Total hours used for this date (existing + new)
        total_work_hours = hours_used + normal_hours + overwork1_hours + overwork2_hours

        # Calculate new totals for normal and overwork hours
        new_normal_hours = min(total_work_hours, normal_limit)
        remaining_work_hours = max(0, total_work_hours - normal_limit)

        # Add remaining work hours to Overwork 1 and Overwork 2
        new_overwork1_hours = min(remaining_work_hours, overwork1_limit)
        new_overwork2_hours = max(0, remaining_work_hours - overwork1_limit)

        return {
            "Normal Hours": new_normal_hours - normal_hours,
            "Overwork 1 Hours": new_overwork1_hours - overwork1_hours,
            "Overwork 2 Hours": new_overwork2_hours - overwork2_hours,
        }

    
    def remove_form(self, index):
        self.data_list.pop(index)

    def __len__(self):
        return len(self.data_list)
    
    def __iter__(self):
        return iter(self.data_list)

    @property
    def data_frame(self):
        return pd.DataFrame(self.data_list)

    @property
    def len(self):
        return len(self.data_list)
