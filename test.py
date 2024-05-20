import pdfkit

# Specify the path to wkhtmltopdf executable
config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')

# Now use this configuration when calling pdfkit
pdfkit.from_url('http://google.com', 'out.pdf', configuration=config)