from datetime import datetime, timedelta


def get_time_range(start_time: str, end_time: str) -> tuple[datetime, datetime]:
    now = datetime.utcnow()
    one_week_ago = now - timedelta(days=7)

    start_time = datetime.fromisoformat(start_time) if start_time else one_week_ago
    end_time = datetime.fromisoformat(end_time) if end_time else now
    return start_time, end_time
