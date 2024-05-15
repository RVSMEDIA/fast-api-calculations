from typing import List
import pandas as pd
import re
import numpy as np
from io import BytesIO
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from datetime import datetime


app = FastAPI()

def process_csv(file):
    # Load CSV into DataFrame
    df = pd.read_csv(file.file, skip_blank_lines=True, skiprows=lambda x: x < 9, usecols=lambda x: x.strip() in ['SNo', 'E. Code', 'Name', 'Shift', 'S. InTime', 'S. OutTime', 'A. InTime', 'A. OutTime', 'Work Dur.', 'OT', 'Tot. Dur.', 'LateBy', 'EarlyGoingBy', 'Status', 'Punch Records'])

    # Define a function to extract 'in(ATD)' and 'out(ATD)' values from 'Punch Records' column
    def extract_punch_records(row):
        punch_records = row['Punch Records']
        if pd.isna(punch_records):  # Check for NaN values
            # return pd.Series({'Out(ATD)hr': np.nan, 'In(ATD)hr': np.nan })  # Return NaN values if 'Punch Records' is NaN
            return pd.Series({'Out(ATD)hr': np.nan, 'In(ATD)hr': np.nan, 'Out(ATD)mint': np.nan, 'In(ATD)mint': np.nan})  # Return NaN values if 'Punch Records' is NaN
        # in_atd = re.findall(r'(\d{2}:\d{2}:in\(ATD\))', punch_records)
        time_differences = calculate_time_differences_in(punch_records)
        in_atd = sum(time_differences)   
        in_hrs = round(in_atd/60 , 2)
        # out_atd = re.findall(r'(\d{2}:\d{2}:out\(ATD\))', punch_records)
        time_gaps = calculate_time_gap_out(punch_records)
        out_atd = sum(time_gaps)
        out_hr = round(out_atd/60 , 2)
        # return pd.Series({'In(ATD)': ','.join(in_atd), 'Out(ATD)': ','.join(out_atd)})
        # return pd.Series({ 'Out(ATD)hr': str(out_hr) + ' hr', 'In(ATD)hr': str(in_hrs) + ' hr'})
        return pd.Series({ 'Out(ATD)hr': str(out_hr) + ' hr', 'In(ATD)hr': str(in_hrs) + ' hr', 'Out(ATD)mint': str(out_atd) + ' mint', 'In(ATD)mint': str(in_atd) + ' mint' })


    # Apply the function to each row to create new columns 'In(ATD)' and 'Out(ATD)'
    # df[['Out(ATD)hr', 'In(ATD)hr' ]] = df.apply(extract_punch_records, axis=1)
    df[['Out(ATD)hr', 'In(ATD)hr', 'Out(ATD)mint', 'In(ATD)mint' ]] = df.apply(extract_punch_records, axis=1)

    # Export DataFrame to new CSV file
    output_csv = BytesIO()
    df.to_csv(output_csv, index=False)
    return output_csv.getvalue()

@app.post("/process_csv/")
async def process_csv_endpoint(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")
    
    processed_csv = process_csv(file)
    
    # Set response headers for downloading the CSV file
    headers = {
        "Content-Disposition": f"attachment; filename={file.filename}",
        "Content-Type": "text/csv",
    }
    
    # Return the CSV file as a StreamingResponse
    return StreamingResponse(iter([processed_csv]), headers=headers)


def calculate_time_differences_in(punch_records):
    # Find all "in(ATD)" and "out(ATD)" timestamps
    in_times = re.findall(r'(\d{2}:\d{2}):in\(ATD\)', punch_records)
    out_times = re.findall(r'(\d{2}:\d{2}):out\(ATD\)', punch_records)
    
    # Convert timestamps to datetime objects
    in_times = [datetime.strptime(time, '%H:%M') for time in in_times]
    out_times = [datetime.strptime(time, '%H:%M') for time in out_times]
    
    # Calculate time differences
    time_differences = [out_time - in_time for in_time, out_time in zip(in_times, out_times)]
    
    # Convert time differences to minutes
    time_differences_minutes = [int(time_diff.total_seconds() / 60) for time_diff in time_differences]
    
    return time_differences_minutes

def calculate_time_gap_out(punch_records):
    # Find all "in(ATD)" and "out(ATD)" timestamps
    in_times = re.findall(r'(\d{2}:\d{2}):in\(ATD\)', punch_records)
    out_times = re.findall(r'(\d{2}:\d{2}):out\(ATD\)', punch_records)
    
    # Convert timestamps to datetime objects
    in_times = [datetime.strptime(time, '%H:%M') for time in in_times]
    out_times = [datetime.strptime(time, '%H:%M') for time in out_times]
    
    # Initialize variables
    first_out_time = None
    time_gaps = []
    
    # Iterate through timestamps
    for in_time, out_time in zip(in_times, out_times):
        # Check if it's an out(ATD) timestamp
        if first_out_time is None:
            first_out_time = out_time
        else:
            # Calculate time gap between first out(ATD) and second in(ATD)
            time_gap = in_time - first_out_time
            # Convert time gap to minutes
            time_gap_minutes = int(time_gap.total_seconds() / 60)
            time_gaps.append(time_gap_minutes)
            # Reset first_out_time for next calculation
            first_out_time = out_time
    
    return time_gaps


# Example usage:
# punch_records = '09:52:in(ATD),10:07:out(ATD),10:12:in(ATD),11:09:out(ATD),11:13:in(ATD),12:06:out(ATD),12:13:in(ATD),12:13:out(ATD),13:30:in(ATD),13:32:out(ATD),14:11:in(ATD),14:29:out(ATD),15:18:in(ATD),15:27:out(ATD),16:14:in(ATD),16:19:out(ATD),16:41:in(ATD),16:56:out(ATD),17:59:in(ATD),18:04:out(ATD),19:00:in(ATD),	'
# time_gaps = calculate_time_gap_out(punch_records)
# time_gaps_total = sum(time_gaps)
# print("Time out of office (in minutes):", time_gaps)
# print("Time out of office:", time_gaps_total)
# print("Time out of office:", round(time_gaps_total/60 , 2) )
# print("Time out of office:", time_gaps_total/60 )


# # Example usage:
# time_differences = calculate_time_differences_in(punch_records)
# time_sum_mint = sum(time_differences)
# print("Time in office (in minutes):", time_differences)
# print("Time in office (in total minutes):", time_sum_mint)
# print("Time in office (in hours):", round(time_sum_mint/60, 2) )
# print("Time in office (in hours):", time_sum_mint/60 )