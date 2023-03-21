def read_file(p: str, encoding='utf-8'):

    if (p.startswith("file:///")):
        p = p[8:]
    
    if (p.startswith("file://")):
        p = p[7:]

    try:
        with open(p, "r", encoding=encoding) as f:
            return f.read()
    except Exception as e:
        return None
