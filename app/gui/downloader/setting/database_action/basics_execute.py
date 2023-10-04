from app.gui.downloader.setting import lite
from functools import wraps


def init_():
    con = lite.return_databases_connect()
    cur = con.cursor()
    return cur, con


def close_(cur, con):
    con.commit()
    cur.close()
    con.close()


def init_close_sqlite(func):
    @wraps(func)
    def decorator_(*args, **kwargs):
        con = lite.return_databases_connect()
        cur = con.cursor()
        result = func(cur, *args, **kwargs)
        con.commit()
        cur.close()
        con.close()
        return result

    return decorator_


@init_close_sqlite
def basics_execute(cur, sql, is_single):
    # cur, con = init_()
    if is_single:
        result = cur.execute(sql).fetchall()
    else:
        result = cur.executescript(sql).fetchall()
    # close_(cur, con)
    return result
