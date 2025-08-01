from datetime import datetime
import os
import zipfile
from weasyprint import HTML

# Check and format date fields in the info 
def format_date(info: dict) -> dict:
    try:
        write_date = datetime.strptime(info["date_write"], "%Y-%m-%d")
        meeting_date = datetime.strptime(info["date_meeting"], "%Y-%m-%d")

        if meeting_date < write_date:
            raise ValueError("Ngày họp không được trước ngày viết thư.")

        info["write_day"] = write_date.day
        info["write_month"] = write_date.month
        info["write_year"] = write_date.year

        info["meeting_day"] = meeting_date.day
        info["meeting_month"] = meeting_date.month
        info["meeting_year"] = meeting_date.year

        return info
    except Exception as e:
        raise ValueError(f"Lỗi xử lý ngày: {e}")

    return info

def convert_html_2_pdf(html_str: str, output_path: str):
    HTML(string=html_str).write_pdf(output_path, stylesheets=["static/css/template.css"])

def zip_folder(folder_path: str, output_zip: str):
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, folder_path)
                zipf.write(full_path, arcname)
