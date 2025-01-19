import pandas as pd

class FormHandler:
    def __init__(self, form, overwork1_limit=4):
        self.form = form
        self.overwork1_limit = overwork1_limit
        self._data_frame = pd.DataFrame(columns=[
            "Date", "Type", "Number", "Name", "Line", 
            "Normal Hours", "Overwork 1 Hours", "Overwork 2 Hours",
            "Normal Driving", "Overwork 1 Driving", "Overwork 2 Driving", "Description"
        ])

    def add_form(self, date, type, number, name, line, work_hours_used, driving_hours_used, description):
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
            "Description": description
        }
        self._data_frame = pd.concat([self._data_frame, pd.DataFrame([new_row])], ignore_index=True)

    def calculate_hours(self, date_entry, work_hours_used, driving_hours_used):
        # Filter the DataFrame to get rows for the given date
        filtered_data = self._data_frame[self._data_frame["Date"] == date_entry]

        # Sum up existing hours for the given date
        normal_hours = filtered_data["Normal Hours"].sum()
        overwork1_hours = filtered_data["Overwork 1 Hours"].sum()
        overwork2_hours = filtered_data["Overwork 2 Hours"].sum()
        normal_driving = filtered_data["Normal Driving"].sum()
        overwork1_driving = filtered_data["Overwork 1 Driving"].sum()
        overwork2_driving = filtered_data["Overwork 2 Driving"].sum()

        # Determine the normal hour limits based on the day of the week
        day_of_week = pd.Timestamp(date_entry).dayofweek  # 0 = Monday, ..., 6 = Sunday
        if day_of_week in [5, 6]:  # Weekend
            normal_limit = 0
        elif day_of_week == 4:  # Friday
            normal_limit = 5
        else:  # Monday to Thursday
            normal_limit = 8

        # Total hours used for this date (existing + new)
        total_work_hours = normal_hours + work_hours_used
        total_driving_hours = normal_driving + driving_hours_used

        # Calculate new totals for normal and overwork hours
        new_normal_hours = min(total_work_hours, normal_limit)
        remaining_work_hours = max(0, total_work_hours - normal_limit)

        # Add remaining work hours to Overwork 1 and Overwork 2
        new_overwork1_hours = min(overwork1_hours + remaining_work_hours, self.overwork1_limit)
        new_overwork2_hours = overwork2_hours + max(0, remaining_work_hours - self.overwork1_limit)

        # Calculate new totals for driving hours
        new_normal_driving = min(total_driving_hours, normal_limit)
        remaining_driving_hours = max(0, total_driving_hours - normal_limit)

        # Add remaining driving hours to Overwork 1 and Overwork 2
        new_overwork1_driving = min(overwork1_driving + remaining_driving_hours, self.overwork1_limit)
        new_overwork2_driving = overwork2_driving + max(0, remaining_driving_hours - self.overwork1_limit)

        return {
            "Normal Hours": new_normal_hours,
            "Overwork 1 Hours": new_overwork1_hours,
            "Overwork 2 Hours": new_overwork2_hours,
            "Normal Driving": new_normal_driving,
            "Overwork 1 Driving": new_overwork1_driving,
            "Overwork 2 Driving": new_overwork2_driving,
        }


    def convert_float_to_comma_string(self, input_float):
        # Convert the float to a string and replace the decimal point with a comma
        output_str = str(input_float).replace('.', ',')
        return output_str
    
    @property
    def data_frame(self):
        return self._data_frame
