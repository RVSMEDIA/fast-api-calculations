from typing import List
import pandas as pd
import re
import numpy as np
from io import BytesIO
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse


app = FastAPI()


def process_csv(file):
    # Load CSV into DataFrame
    df = pd.read_csv(file.file, skip_blank_lines=True, skiprows=lambda x: x < 9, usecols=lambda x: x.strip() in ['SNo', 'E. Code', 'Name', 'Shift', 'S. InTime', 'S. OutTime', 'A. InTime', 'A. OutTime', 'Work Dur.', 'OT', 'Tot. Dur.', 'LateBy', 'EarlyGoingBy', 'Status', 'Punch Records'])

    # Define a function to extract 'in(ATD)' and 'out(ATD)' values from 'Punch Records' column
def extract_punch_records(row):
    punch_records = row['Punch Records']
    in_atd = re.findall(r'(\d{2}:\d{2}:in\(ATD\))', punch_records)
    out_atd = re.findall(r'(\d{2}:\d{2}:out\(ATD\))', punch_records)
    return in_atd, out_atd

# @app.post("/process_csv/")
# async def process_csv_endpoint(file: UploadFile = File(...)):
#     if not file.filename.endswith(".csv"):
#         raise HTTPException(status_code=400, detail="Only CSV files are allowed")
    
#     processed_csv = process_csv(file)
#     return {"filename": file.filename, "processed_csv": processed_csv.decode("utf-8")}
@app.post("/process_csv/")
async def process_csv_endpoint(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")
    
    # Load CSV into DataFrame
    df = pd.read_csv(file.file, skip_blank_lines=True, skiprows=lambda x: x < 9, usecols=lambda x: x.strip() in ['SNo', 'E. Code', 'Name', 'Shift', 'S. InTime', 'S. OutTime', 'A. InTime', 'A. OutTime', 'Work Dur.', 'OT', 'Tot. Dur.', 'LateBy', 'EarlyGoingBy', 'Status', 'Punch Records'])

    # Apply the function to each row to get arrays of in(ATD) and out(ATD)
    in_atd, out_atd = zip(*df.apply(extract_punch_records, axis=1))
    
    # Print lengths of in_atd and out_atd
    print("Length of in(ATD) array:", len(in_atd))
    print("Length of out(ATD) array:", len(out_atd))
    
    return {"filename": file.filename, "in(ATD)": in_atd, "out(ATD)": out_atd}