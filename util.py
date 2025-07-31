from datetime import datetime

def format_date(info: dict) -> dict:
    try:
        dt = datetime.strptime(info["date"], "%Y-%m-%d")
        info["date_day"] = dt.day
        info["date_month"] = dt.month
        info["date_year"] = dt.year
    except Exception as e:
        raise ValueError(f"Format Error: {e}")

    return info