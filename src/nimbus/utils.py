import pendulum


def get_current_ist_time():
    return pendulum.now("Asia/Kolkata").replace(tzinfo=None)
