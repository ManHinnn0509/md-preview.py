def read_file(p: str, encoding='utf-8'):
    try:
        with open(p, "r", encoding=encoding) as f:
            return f.read()
    except Exception as e:
        return None