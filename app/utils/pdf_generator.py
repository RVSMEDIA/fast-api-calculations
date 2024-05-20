# app/utils/pdf_generator.py

import pandas as pd
from bs4 import BeautifulSoup
import pdfkit
import os
from datetime import date

# config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

def generate_pdfs_from_csv(file_path: str, template_path: str, output_dir: str):
    # Read CSV file
    data = pd.read_csv(file_path)
    data.columns = [col.strip() for col in data.columns]

    # Read HTML template
    with open(template_path, 'r') as file:
        html_content = file.read()

    # Get today's date
    today_date = date.today().strftime("%Y-%m-%d")

    # Create the directory if it doesn't exist
    today_folder = os.path.join(output_dir, today_date)
    if not os.path.exists(today_folder):
        os.makedirs(today_folder)

    # Iterate over rows and fill data into HTML
    for index, row in data.iterrows():
        # Parse HTML template for each row
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find elements to fill with data
        pay_slip_for_the_month_of_element = soup.find(id='pay_slip_for_the_month_of')
        name_element = soup.find(id='name')
        joining_date_element = soup.find(id='joining_date')

        # Fill data into HTML elements
        pay_slip_for_the_month_of_element.string = row['Pay Slip for the month of']
        name_element.string = row['Name']
        joining_date_element.string = row['Joining date']

        # Generate PDF
        pdf_file_path = os.path.join(today_folder, f"{row['Name']}-{row['Pay Slip for the month of']}.pdf")
        # pdfkit.from_string(str(soup), pdf_file_path)
        pdfkit.from_string(str(soup), pdf_file_path, configuration=pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf/wkhtmltopdf.exe'))


    
    return today_folder
