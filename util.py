from datetime import datetime

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