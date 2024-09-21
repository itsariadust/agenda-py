from datetime import datetime, timedelta

def get_date(prompt):
    date_input = input(prompt)
    if date_input: return datetime.strptime(date_input, '%m-%d-%Y').date()
    else: return False

def get_time(prompt):
    time_input = input(prompt)
    if time_input: return datetime.strptime(time_input, '%H:%M').time()
    else: return False

def hour_rounder(t: datetime):
    return (t.replace(second=0, microsecond=0, minute=0, hour=t.hour)
            + timedelta(hours=1))