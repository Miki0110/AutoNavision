import pandas as pd
from config.config_handler import get_config, update_config

class FormHandler:
    def __init__(self, form):
        self.form = form
        self.config = get_config()
        self.overwork1_limit = self.config["overwork_limits"]["overwork1"]
        self.data_list = []

    def add_form(self, date, type, number, name, line, work_hours_used, driving_hours_used, plate, to_address, from_address, description):
        # Calculate the work hours and overtime
        entry_hours = self.calculate_hours(date, work_hours_used, driving_hours_used)
        # Append the new row to the DataFrame
        new_row = {
            "Date": date,
            "Type": type,
            "Number": number,
            "Name": name,
            "Line": line,
            "Normal Hours": entry_hours["Normal Hours"],
            "Overwork 1 Hours": entry_hours["Overwork 1 Hours"],
            "Overwork 2 Hours": entry_hours["Overwork 2 Hours"],
            "Normal Driving": entry_hours["Normal Driving"],
            "Overwork 1 Driving": entry_hours["Overwork 1 Driving"],
            "Overwork 2 Driving": entry_hours["Overwork 2 Driving"],
            "plate": plate,
            "to_address": to_address,
            "from_address": from_address,
            "Description": description
        }
        self.data_list.append(new_row)

    import pandas as pd

    def calculate_hours(self, date_entry, work_hours_used, driving_hours_used):
        """
        Distribute new 'work_hours_used' and 'driving_hours_used' across
        Normal, Overwork 1, and Overwork 2 so that each category receives
        the correct proportion of driving vs. non-driving hours, while 
        respecting daily normal and overwork1 limits.
        """

        # Grab existing totals for date_entry (or zero if none)
        if self.len > 0:
            filtered_data = self.data_frame[self.data_frame["Date"] == date_entry]
            
            normal_hours = filtered_data["Normal Hours"].sum()
            overwork1_hours = filtered_data["Overwork 1 Hours"].sum()
            overwork2_hours = filtered_data["Overwork 2 Hours"].sum()
            
            normal_driving = filtered_data["Normal Driving"].sum()
            overwork1_driving = filtered_data["Overwork 1 Driving"].sum()
            overwork2_driving = filtered_data["Overwork 2 Driving"].sum()
        else:
            normal_hours = 0
            overwork1_hours = 0
            overwork2_hours = 0
            
            normal_driving = 0
            overwork1_driving = 0
            overwork2_driving = 0

        # Set normal and overwork1 limits based on day of week
        day_of_week = pd.Timestamp(date_entry).dayofweek  # Monday=0, Tuesday=1, ...
        if day_of_week in [5, 6]:  # weekend
            normal_limit = 0
            overwork1_limit = 0
        elif day_of_week == 4:     # Friday
            normal_limit = 5
            overwork1_limit = self.overwork1_limit
        else:                      # Monday-Thursday
            normal_limit = 8
            overwork1_limit = self.overwork1_limit

        # Compute how many total new hours we have
        total_new_hours = work_hours_used + driving_hours_used

        # If there's nothing new to add, return zeros
        if total_new_hours <= 0:
            return {
                "Normal Hours": 0.0,
                "Overwork 1 Hours": 0.0,
                "Overwork 2 Hours": 0.0,
                "Normal Driving": 0.0,
                "Overwork 1 Driving": 0.0,
                "Overwork 2 Driving": 0.0,
            }

        # Calculate how much capacity is left in Normal and Overwork1
        existing_normal_total   = normal_hours + normal_driving
        existing_overwork1_total = overwork1_hours + overwork1_driving

        normal_capacity   = max(0, normal_limit - existing_normal_total)
        overwork1_capacity = max(0, overwork1_limit - existing_overwork1_total)

        # Figure out driving vs. work ratio among the new hours
        driving_ratio = driving_hours_used / total_new_hours
        # work_ratio is simply (1 - driving_ratio)
        work_ratio = 1.0 - driving_ratio

        # ------------------------
        # ALLOCATE INTO NORMAL
        # ------------------------
        normal_allocation = min(normal_capacity, total_new_hours)
        # Of that allocation, a portion goes to driving and a portion to work:
        normal_driving_allocation = normal_allocation * driving_ratio
        normal_work_allocation    = normal_allocation * work_ratio

        # How many new hours left to allocate after Normal
        leftover_hours     = total_new_hours - normal_allocation
        leftover_driving   = driving_hours_used - normal_driving_allocation
        leftover_work      = work_hours_used - normal_work_allocation

        # ------------------------
        # ALLOCATE INTO OVERWORK 1
        # ------------------------
        overwork1_allocation = min(overwork1_capacity, leftover_hours)

        # The ratio of leftover driving vs. leftover work can now differ
        # from the original ratio if we've exhausted e.g. all leftover driving
        # or leftover_work. So recalc the ratio for the leftover chunk:
        leftover_total = leftover_driving + leftover_work

        if leftover_total > 0:
            driving_ratio_ow1 = leftover_driving / leftover_total
            work_ratio_ow1    = leftover_work / leftover_total
        else:
            driving_ratio_ow1 = 0.0
            work_ratio_ow1    = 0.0

        overwork1_driving_allocation = overwork1_allocation * driving_ratio_ow1
        overwork1_work_allocation    = overwork1_allocation * work_ratio_ow1

        # How many hours remain for Overwork 2
        leftover_hours_2   = leftover_hours - overwork1_allocation
        leftover_driving_2 = leftover_driving - overwork1_driving_allocation
        leftover_work_2    = leftover_work - overwork1_work_allocation

        # ------------------------
        # ALLOCATE INTO OVERWORK 2
        # ------------------------
        # Overwork 2 is essentially unlimited; the remainder goes here
        overwork2_allocation = leftover_hours_2

        leftover_total_2 = leftover_driving_2 + leftover_work_2
        if leftover_total_2 > 0:
            driving_ratio_ow2 = leftover_driving_2 / leftover_total_2
            work_ratio_ow2    = leftover_work_2 / leftover_total_2
        else:
            driving_ratio_ow2 = 0.0
            work_ratio_ow2    = 0.0

        overwork2_driving_allocation = overwork2_allocation * driving_ratio_ow2
        overwork2_work_allocation    = overwork2_allocation * work_ratio_ow2

        # These allocations are the *new* hours to be added in each category
        return {
            "Normal Hours":       normal_work_allocation,
            "Overwork 1 Hours":  overwork1_work_allocation,
            "Overwork 2 Hours":  overwork2_work_allocation,
            
            "Normal Driving":     normal_driving_allocation,
            "Overwork 1 Driving": overwork1_driving_allocation,
            "Overwork 2 Driving": overwork2_driving_allocation,
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
