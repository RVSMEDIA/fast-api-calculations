from typing import List
import pandas as pd
import re
import numpy as np
from io import BytesIO
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse


app = FastAPI()


# @app.get("/demo")
# def hello_world():
#     return {"message": "OK"}

# @app.post("/uploadfiles/")
# async def create_upload_files(
#     files: List[UploadFile] = File(description="Multiple files as UploadFile"),
# ):
#     return {"filenames": [file.filename for file in files]}

def process_csv(file):
    # Load CSV into DataFrame
    df = pd.read_csv(file.file, skip_blank_lines=True, skiprows=lambda x: x < 9, usecols=lambda x: x.strip() in ['SNo', 'E. Code', 'Name', 'Shift', 'S. InTime', 'S. OutTime', 'A. InTime', 'A. OutTime', 'Work Dur.', 'OT', 'Tot. Dur.', 'LateBy', 'EarlyGoingBy', 'Status', 'Punch Records'])

    # Define a function to extract 'in(ATD)' and 'out(ATD)' values from 'Punch Records' column
    def extract_punch_records(row):
        punch_records = row['Punch Records']
        if pd.isna(punch_records):  # Check for NaN values
            return pd.Series({'In(ATD)': np.nan, 'Out(ATD)': np.nan})  # Return NaN values if 'Punch Records' is NaN
        in_atd = re.findall(r'(\d{2}:\d{2}:in\(ATD\))', punch_records)
        out_atd = re.findall(r'(\d{2}:\d{2}:out\(ATD\))', punch_records)
        return pd.Series({'In(ATD)': ','.join(in_atd), 'Out(ATD)': ','.join(out_atd)})

    # Apply the function to each row to create new columns 'In(ATD)' and 'Out(ATD)'
    df[['In(ATD)', 'Out(ATD)']] = df.apply(extract_punch_records, axis=1)

    # Export DataFrame to new CSV file
    output_csv = BytesIO()
    df.to_csv(output_csv, index=False)
    return output_csv.getvalue()

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
    
    processed_csv = process_csv(file)
    
    # Set response headers for downloading the CSV file
    headers = {
        "Content-Disposition": f"attachment; filename={file.filename}",
        "Content-Type": "text/csv",
    }
    
    # Return the CSV file as a StreamingResponse
    return StreamingResponse(iter([processed_csv]), headers=headers)