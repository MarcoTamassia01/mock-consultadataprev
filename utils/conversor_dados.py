def to_int(value):
    if not value: return 0
    try:
        return int(float(str(value).replace(",", ".")))
    except:
        return 0


def to_float(value):
    if not value: return 0.0
    try:
        v = str(value).strip().replace('"', '')
        if "," in v: v = v.replace(".", "").replace(",", ".")
        return float(v)
    except:
        return 0.0