from datetime import datetime

def is_valid_fecha(fecha_str, formato="%Y-%m-%d"):

    try:
        datetime.strptime(fecha_str, formato)
        return True
    except ValueError:
        return False