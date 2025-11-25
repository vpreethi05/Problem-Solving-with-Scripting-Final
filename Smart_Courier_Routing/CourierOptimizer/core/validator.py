# core/validator.py

# Valid priorities
VALID_PRIORITIES = {"High", "Medium", "Low"}

def is_valid_name(name):
    """
    Valid customer name: non-empty and only printable characters.
    """
    if not name:
        return False
    return all(ch.isprintable() for ch in name)


def is_valid_lat(value):
    """
    Latitude must be a float between -90 and 90.
    """
    try:
        num = float(value)
        return -90 <= num <= 90
    except:
        return False


def is_valid_lon(value):
    """
    Longitude must be a float between -180 and 180.
    """
    try:
        num = float(value)
        return -180 <= num <= 180
    except:
        return False


def is_valid_priority(p):
    """
    Priority must be exactly: High, Medium, or Low.
    """
    return p in VALID_PRIORITIES


def is_valid_weight(w):
    """
    Weight must be a float >= 0.
    """
    try:
        num = float(w)
        return num >= 0
    except:
        return False
