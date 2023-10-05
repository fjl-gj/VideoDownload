from app.common.constantx import DB_TABLE
from app.gui.downloader.setting.database_action.basics_execute import \
    init_close_sqlite


@init_close_sqlite
def select_record(cur, builder):
    """
    select single line record
    :param cur: sqlite cursor
    :param builder: select query where builder
    :return: select all record
    """
    query_all = ""
    sql = f"""SELECT * FROM {DB_TABLE};"""
    if builder:
        for number, query in enumerate(builder):
            if number == 0 and number == len(builder) - 1:
                if type(builder[query]) is str:
                    query_all += f" {query}='{builder[query]}' "
                    break
                else:
                    query_all += f" {query}={builder[query]} "
                    break
            if number == len(builder) - 1:
                if type(builder[query]) is str:
                    query_all += f" {query}='{builder[query]}'"
                    break
                if type(builder[query]) is int:
                    query_all += f" {query}={builder[query]}"
                    break
            if type(builder[query][0]) is str:
                query_all += f" {query}='{builder[query][0]}' {builder[query][1]} "
            if type(builder[query][0]) is int:
                query_all += f" {query}={builder[query][0]} {builder[query][1]} "

        sql = f"""SELECT * FROM {DB_TABLE} WHERE {query_all};"""
    result = cur.execute(sql).fetchall()

    return result
