# app/controllers/pdf_controller.py

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import shutil
import os
from app.utils.pdf_generator import generate_pdfs_from_csv

router = APIRouter()

@router.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a CSV file.")

    temp_dir = "temp_files"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    file_path = os.path.join(temp_dir, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        output_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        template_path = "app/static/template.html"
        generated_pdfs_dir = generate_pdfs_from_csv(file_path, template_path, output_dir)
        
        return JSONResponse(content={"message": "PDFs generated successfully.", "directory": generated_pdfs_dir})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        os.remove(file_path)
