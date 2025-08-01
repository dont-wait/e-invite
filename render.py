import json
from jinja2 import Template
from datetime import datetime
import os
from util import format_date, convert_html_2_pdf, zip_folder

#Test 
def get_input_data():
    with open('data/data.json', 'r', encoding='utf-8') as file:
        return json.load(file)

def get_template():
    with open('templates/template.html', 'r', encoding='utf-8') as file:
        return file.read()

def save_invite(html_content, filename):
    with open(f'invites/html/{filename}', 'w', encoding='utf-8') as file:
        file.write(html_content)

def build_invite(data: dict):
    html_template = get_template()
    jinja2_template = Template(html_template)

    html_folder = "invites/html"
    pdf_folder = "invites/pdf"

    os.makedirs(html_folder, exist_ok=True)
    os.makedirs(pdf_folder, exist_ok=True)

    for i, info in enumerate(data["infos"]):
        try:
            info = format_date(info)
            html_content = jinja2_template.render(**info)

            # Save HTML
            html_filename = f"invite_{i+1}_{info['student_name'].replace(' ', '_')}.html"
            save_invite(html_content, html_filename)

            # Save PDF
            pdf_filename = os.path.join(pdf_folder, f"invite_{i+1}_{info['student_name'].replace(' ', '_')}.pdf")
            convert_html_2_pdf(html_content, pdf_filename)
            print("=======Saved PDF:", pdf_filename)

        except Exception as e:
            print(f"======Error in info #{i+1}: {e}")

    # ZIP
    zip_folder(pdf_folder, "invites/invite_all.zip")
    print("======Đã tạo file nén: invites/invite_all.zip")
