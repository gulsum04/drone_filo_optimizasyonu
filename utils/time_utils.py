
def time_to_minutes(tstr):
    if isinstance(tstr, int):
        return tstr
    h, m = map(int, tstr.split(":"))
    return h * 60 + m

def is_time_valid(current_time, delivery):
    if not delivery.time_window:
        return True
    start_min = time_to_minutes(delivery.time_window[0])
    end_min = time_to_minutes(delivery.time_window[1])
    return start_min <= current_time <= end_min
