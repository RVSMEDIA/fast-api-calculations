import pandas as pd
from bs4 import BeautifulSoup
import pdfkit
import os
from datetime import date


# Read CSV file
data = pd.read_csv('salarysheet.csv')
print(data)

# Read HTML template
with open('template.html', 'r') as file:
    html_content = file.read()


# Get today's date
today_date = date.today().strftime("%Y-%m-%d")

# Create the directory if it doesn't exist
download_folder = os.path.join(os.path.expanduser("~"), "Downloads")
today_folder = os.path.join(download_folder, today_date)
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
    employee_id_element = soup.find(id='employee_id')
    bank_name_element = soup.find(id='bank_name')
    ifsc_code_element = soup.find(id='ifsc_code')
    account_number_element = soup.find(id='account_number')
    pan_card_no_element = soup.find(id='pan_card_no')
    designation_element = soup.find(id='designation')
    department_element = soup.find(id='department')
    office_location_element = soup.find(id='office_location')
    total_working_days_this_month_element = soup.find(id='total_working_days_this_month')
    no_of_days_worked_element = soup.find(id='no_of_days_worked')
    gross_salary_element = soup.find(id='gross_salary')
    basic_element = soup.find(id='basic')
    hra_element = soup.find(id='hra')
    da_element = soup.find(id='da')
    performance_allowance_element = soup.find(id='performance_allowance')
    conveince_allowance_element = soup.find(id='conveince_allowance')
    other_allowance_element = soup.find(id='other_allowance')
    net_pay_for_the_month_element = soup.find(id='net_pay_for_the_month')
    earning_in_words_element = soup.find(id='earning_in_words')
    cl_used_element = soup.find(id='cl_used')
    cl_opening_balance_element = soup.find(id='cl_opening_balance')
    cl_balance_element = soup.find(id='cl_balance')
    total_cl_deducted_element = soup.find(id='total_cl_deducted')
    profesinal_tax_dedcution_element = soup.find(id='profesinal_tax_dedcution')
    unpaid_leaves_deduction_element = soup.find(id='unpaid_leaves_deduction')
    other_deductions_element = soup.find(id='other_deductions')
    income_tax_element = soup.find(id='income_tax')
    esi_deduction_element = soup.find(id='esi_deduction')
    epf_deduction_element = soup.find(id='epf_deduction')
    total_deduction_this_month_element = soup.find(id='total_deduction_this_month')
    # Continue finding other elements and fill them accordingly
    
    # Fill data into HTML elements
    pay_slip_for_the_month_of_element.string = row['Pay Slip for the month of']
    name_element.string = row['Name']
    joining_date_element.string = row['Joining date']
    employee_id_element.string = row['Employee Id']
    bank_name_element.string = row['Bank Name']
    ifsc_code_element.string = row['IFSC Code']
    account_number_element.string = str(row['Account Number'])
    pan_card_no_element.string = row['Pan Card No.']
    designation_element.string = row['Designation']
    department_element.string = row['Department']
    office_location_element.string = row['Office Location']
    total_working_days_this_month_element.string = str(row['Total working days this Month'])
    no_of_days_worked_element.string = str(row['No. of Days worked'])
    gross_salary_element.string = str(row['Gross Salary'])
    basic_element.string = str(row['Basic'])
    hra_element.string = str(row['HRA'])
    da_element.string = str(row['DA'])
    performance_allowance_element.string = str(row['Performance Allowance'])
    conveince_allowance_element.string = str(row['Conveince Allowance'])
    other_allowance_element.string = str(row['Other Allowance (Bonus/Extra days)'])
    net_pay_for_the_month_element.string = str(row['Net Pay for the month: '])
    earning_in_words_element.string = str(row['Earning in words'])
    cl_used_element.string = str(row['CL used (Leaves Taken)'])
    cl_opening_balance_element.string = str(row['CL opening Balance (Leave Balance For This Month)'])
    cl_balance_element.string = str(row['CL Balance (Paid Leave Balance Remaining)'])
    total_cl_deducted_element.string = str(row['Total CL DEDUCTED (Number of Leaves to deduct)'])
    profesinal_tax_dedcution_element.string = str(row['Profesinal Tax dedcution'])
    unpaid_leaves_deduction_element.string = str(row['Unpaid Leaves Deduction'])
    other_deductions_element.string = str(row['Other Deductions (Loans/Retention)'])
    income_tax_element.string = str(row['Income TAX (TDS Deduction)'])
    esi_deduction_element.string = str(row['ESI Deduction'])
    epf_deduction_element.string = str(row['EPF Deduction'])
    total_deduction_this_month_element.string = str(row['Total Deduction this Month'])
    # Continue filling other elements
    
    # Generate PDF
    pdf_file_path = os.path.join(today_folder, f'report_{index}.pdf')
    pdfkit.from_string(str(soup), pdf_file_path)
