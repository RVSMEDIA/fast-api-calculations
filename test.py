from weasyprint import HTML

# Generate PDF from a URL and save it to a file
HTML('http://google.com').write_pdf('out.pdf')
