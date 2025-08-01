import json
from jinja2 import Template
from datetime import datetime
import os
from util import format_date, convert_html_2_pdf, zip_folder

def get_input_data():
    with open('data.json', 'r', encoding='utf-8') as file:
        return json.load(file)

def get_template():
    with open('template.html', 'r', encoding='utf-8') as file:
        return file.read()

def save_invite(html_content, filename):
    os.makedirs("invites", exist_ok=True)
    with open(f'invites/{filename}', 'w', encoding='utf-8') as file:
        file.write(html_content)

def build_invite():
    data = get_input_data()
    html_template = get_template()
    jinja2_template = Template(html_template)

    for i, info in enumerate(data["infos"]):
        try:
            info = format_date(info)
            html_content = jinja2_template.render(**info)
            
            # Save HTML local
            filename = f"invite_{i+1}_{info['student_name'].replace(' ', '_')}.html"
            save_invite(html_content, filename)
        
            # Save PDF
            pdf_filename = f"{pdf_folder}/invite_{i+1}_{info['student_name'].replace(' ', '_')}.pdf"
            convert_html_2_pdf(html_content, pdf_filename)
        
        except Exception as e:
            print(f"Error in info: #{i+1}: {e}")

    print("All invites have been saved to 'invites/'.")
    # ZIP
    zip_folder("invites/pdf", "invites/invite_all.zip")
    print("✅ Đã tạo file nén: invites/invite_all.zip")
