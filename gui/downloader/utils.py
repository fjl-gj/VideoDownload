def fomart_time(dur):
    minute = '00'
    hour = '00'
    if not dur:
        second = '00'
    else:
        second = dur % 60 if (dur % 60) >= 10 else f'0{(dur % 60)}'
    if dur >= 60:
        minute = int(dur / 60) if int(dur / 60) >= 10 else f'0{int(dur / 60)}'
        if int(minute) >= 60:
            minute = minute % 60 if minute % 60 >= 10 else f'0{minute % 60}'
            hour = int(minute / 60)
    return f'{hour}:{minute}:{second}'


def byte_to_mb(bytes):
    if type(bytes) == str:
        return bytes
    if bytes:
        if int(bytes) >= (1024*1024):
            size = bytes / (1024 * 1024)
            size = round(size, 2)
            return f'{size}MB'
        else:
            size = int(bytes / 1024) + 1
            return f'{size}KB'
    return ''


def check_proxy(text):
    http_proxy = {}
    if text:
        if ';' in text:
            list_proxy = text.split(';')
            for i in list_proxy:
                url_proxy = i.split("://")
                if url_proxy[0].strip() == "http":
                    http_proxy['http'] = url_proxy[1].strip()
                if url_proxy[0].strip() == "https":
                    http_proxy['https'] = url_proxy[1].strip()
    return http_proxy


def result_proxy(proxys):
    _proxies = {}
    if proxys == 'None':
        _proxies = {"https": None, "http": None}
    else:
        for proxy in proxys:
            _proxies[proxy] = f'http://{proxys.get(proxy)}'
    return _proxies
