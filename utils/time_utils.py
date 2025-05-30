def is_within_time_window(current_time, time_window):
    """
    Belirli bir zaman aralığında olup olmadığını kontrol eder.
    time_window = (start_minute, end_minute)
    """
    return time_window[0] <= current_time <= time_window[1]
