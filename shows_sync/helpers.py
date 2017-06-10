from datetime import datetime, timedelta

def is_watch_recently(watched):
    date = datetime.now() - timedelta(days=1)
    try:
        return watched > date
    except Exception as e:
        return False
