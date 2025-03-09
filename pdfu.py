import PyPDF2
import base64
import json
import time
from io import BytesIO
from selenium import webdriver

print_options = {
    'landscape': False,
    'displayHeaderFooter': False,
    'printBackground': True,
    'preferCSSPageSize': True,
    'paperWidth': 10,
    'paperHeight': 14.25,
    'marginTop': 0,
    'marginBottom': 0,
    'marginLeft': 0,
    'marginRight': 0,
}

def get_body_size(driver):
    body_size = driver.execute_script(
        """
        const style = window.getComputedStyle(document.body);
        return {
            width: parseFloat(style.width) || document.body.offsetWidth,
            height: parseFloat(style.height) || document.body.offsetHeight
        };
        """
    )
    
    px_to_inch = 1 / 96
    return body_size["width"] * px_to_inch, body_size["height"] * px_to_inch

def get_pdf_from_url(driver, url: str) -> bytes:
    driver.get(url)
    time.sleep(0.3)
    
    page_width, page_height = get_body_size(driver)
    
    print_options.update({
        'paperWidth': page_width,
        'paperHeight': page_height
    })
    
    result = driver.execute_cdp_cmd("Page.printToPDF", print_options)
    return base64.b64decode(result['data'])

def generate_pdf(driver, url: str) -> BytesIO:
    pdf_data = get_pdf_from_url(driver, url)
    file = BytesIO()
    file.write(pdf_data)
    return file

def merge_pdfs(pdf_list, output_path):
    pdf_merger = PyPDF2.PdfMerger()
    
    for pdf in pdf_list:
        with open(pdf, 'rb') as f:
            pdf_merger.append(f)
    
    with open(output_path, 'wb') as output_pdf:
        pdf_merger.write(output_pdf)