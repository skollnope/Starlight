from datetime import datetime

def getLocalTime(format: str = None) -> str:
    current_time = datetime.now()
    if(format is None):
        format = "%Hh %M" #defined as default format
    return current_time.strftime(format)